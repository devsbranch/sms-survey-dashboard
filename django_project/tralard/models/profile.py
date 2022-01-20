import os

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from rolepermissions.roles import get_user_roles
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from rolepermissions.roles import get_user_roles

from tralard.utils import unique_slugify, user_profile_update_form

GENDER_CHOICES = (
    ("Male", _("Male")),
    ("Female", _("Female")),
    ("Transgender", _("Transgender")),
    ("Other", _("Other"))
)

class Profile(models.Model):
    """
    A model for storing addtional imformation about User.
    """

    slug = models.SlugField(
        max_length=255,
        null=True,
        blank=True
    )
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
    )
    birth_date = models.DateField(
        _("Birth Date"), 
        null=True,
        blank=True
    )
    gender = models.CharField(
        _("Gender"), 
        max_length=100, 
        choices=GENDER_CHOICES, 
        null=True, 
        blank=True
    )
    about_me = models.CharField(
        _("About Me"), 
    max_length=300, 
    null=True, 
    blank=True
    )
   
    profile_photo = ProcessedImageField(
        upload_to="profile_photo",
        processors=[ResizeToFill(512, 512)],
        format="JPEG",
        options={"quality": 100},
        null=True,
        blank=True,
    )
    cell = models.CharField(
        _("Phone Number"), 
        max_length=15, 
        null=True, 
        blank=True
    )
    address = models.CharField(
        _("Address"), 
        max_length=300, 
        null=True, 
        blank=True
    )
    district = models.ForeignKey(
        'tralard.district', 
        on_delete=models.SET_NULL, 
        null=True, blank=True
    )
    postal_code = models.CharField(
        _("Postal Code"), 
        max_length=100, 
        null=True, 
        blank=True
    )

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(f"{self.user.username}"))
        super().save(*args, **kwargs)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}'s Profile"
        else:
            return f"{self.user.username}'s Profile"
    
    @property
    def current_user_roles(self):
        uncleaned_user_roles = get_user_roles(self.user)
        cleaned_user_roles = []
        
        for role in uncleaned_user_roles:
            cleaned_user_roles.append(role.get_name())
        user_roles = [role_name.replace("_", " ").title() for role_name in cleaned_user_roles]
        return user_roles

    @property
    def profile_form(self):
        update_form = user_profile_update_form(self)
        return update_form

    
    @property
    def profile_photo_url(self):
        if self.profile_photo:
            return self.profile_photo.url
        return os.path.join(settings.STATIC_URL, "assets/images/logos/logo.png")
