
import string
from django.utils.crypto import get_random_string

from djmoney.money import Money

from rolepermissions.roles import get_user_roles

def unique_slugify(instance, slug):
    """
    Generate slug and ensure it is unique,

    Parameters
    ----------
    instance : (django.db.models.Mode) This is a model instance the slug is generated for.
    slug : (string) a unique string that serves as a unique id for the object.

    Returns
    -------
    slug: (string): a unique string of type slug. 
    i.e >>> 'project-tralard-unique-entry-1245-live'

    """
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + get_random_string(length=4)
    return unique_slug

def compute_total_amount(model_name, object_id: int, action: str) -> Money:
    """
    Compute the total amount of either disburesment or expenditure.

    Parameters
    ----------
    model_name : Model.model
        The model name.
    object_id : int
        The object id.
    action : str
        The action to be performed, either disburesment or expenditure.

    Returns
    -------
    float
        The total amount.

    """
    all_amount_values = []
    if action.lower() == "disbursement":
        all_amount_objects = model_name.objects.filter(fund__id=object_id)
    elif action.lower() == "expenditure":
        all_amount_objects = model_name.objects.filter(disbursment__id=object_id)

    for amount in all_amount_objects:
        amount_value = amount.amount
        all_amount_values.append(amount_value)
    total_amount = sum(all_amount_values)
    return total_amount


def get_balance(initial_amount: float, total_amount: float) -> Money:
    """
    Get the balance of the fund.

    Parameters
    ----------
    initial_amount : float
        The initial amount of the fund.
    total_amount : float
        The total amount of the disbursement.
    """
    difference = initial_amount - total_amount
    return difference


def check_requested_deduction_against_balance(
    balance, requested_amount, requested_semantic, balance_semantic
) -> Money:
    """
    Check if the requested amount is greater than the balance.

    Parameters
    ----------
    balance : float
        The balance of the fund or disbursment.
    requested_amount : float
        The requested amount.
    requested_semantic : str
        The requested semantic.
    balance_semantic : str
        The balance semantic.

    Returns
    -------
    float
    """
    if requested_amount > balance:
        raise ValueError(
            f"Requested {requested_semantic} amount can not be more than the remaining {balance_semantic} balance."
        )
    return requested_amount

def current_user_roles(user):
    uncleaned_user_roles = get_user_roles(user)
    cleaned_user_roles = []
    
    for role in uncleaned_user_roles:
        cleaned_user_roles.append(role.get_name())
    user_roles = [role_name.replace("_", " ").title() for role_name in cleaned_user_roles]
    return user_roles

def user_profile_update_form_validator(method, user):
    try:
        from django.shortcuts import get_object_or_404
        from tralard.models.profile import Profile
        from tralard.forms.profile import ProfileForm
    except:
        pass
    user_profile = get_object_or_404(Profile, user=user)
    user_roles = current_user_roles(user_profile.user)
    profile_form = ProfileForm(method or None, instance=user_profile)
    return user_roles, user_profile, profile_form
    