import logging
import os
import shutil
from datetime import datetime
from math import radians, cos, sin, asin, sqrt

from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.files.storage import FileSystemStorage

from exif import Image
from djmoney.money import Money
from rolepermissions.roles import get_user_roles, RolesManager

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (
    Spacer,
    Table,
    Paragraph,
    SimpleDocTemplate,
)

from tralard.constants import BASE_TEMP_DIR

logger = logging.getLogger(__name__)


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


def get_available_roles():
    uncleaned_user_roles = RolesManager.get_roles()
    cleaned_user_roles = []

    for role in uncleaned_user_roles:
        cleaned_user_roles.append(role.get_name())
    user_roles = [
        role_name.replace("_", " ").title() for role_name in cleaned_user_roles
    ]
    return user_roles


def current_user_roles(user):
    uncleaned_user_roles = get_user_roles(user)
    cleaned_user_roles = []

    for role in uncleaned_user_roles:
        cleaned_user_roles.append(role.get_name())
    user_roles = [
        role_name.replace("_", " ").title() for role_name in cleaned_user_roles
    ]
    return user_roles


def user_profile_update_form(user):
    try:
        from tralard.forms.profile import ProfileForm  # don't move this import on top
    except:
        pass
    user_create_form = ProfileForm(instance=user)
    return user_create_form


def new_user_create_form():
    try:
        from authentication.forms import SignUpForm
    except:
        pass
    user_update_form = SignUpForm()
    return user_update_form


def user_update_form(instance):
    try:
        from authentication.forms import UserUpdateForm
    except:
        pass
    user_update_form = UserUpdateForm(instance=instance)
    return user_update_form


def all_users():
    try:
        from django.contrib.auth.models import User  # don't move this import on top
    except:
        pass
    available_user_list = User.objects.all()
    return available_user_list


def training_update_form(training):
    try:
        from tralard.forms.training import TrainingForm  # don't move this import on top
    except:
        pass
    training_update_form = TrainingForm(instance=training)
    return training_update_form


class IndicatorReportBuild(SimpleDocTemplate):
    def __init__(self, filename, indicators, **kwargs):
        super().__init__(filename, pagesize=landscape(A4), **kwargs)
        self.leftMargin = 30
        self.rightMargin = 30
        self.doc_elements = [
            Spacer(1, 2 * inch),
            Spacer(1, 2 * inch),
            Spacer(1, 2 * inch),
        ]
        self.indicators = indicators
        self.assets_root = settings.STATIC_ROOT + "/assets"

        pdfmetrics.registerFont(
            TTFont("roboto-bold", f"{self.assets_root}/fonts/Roboto/Roboto-Bold.ttf")
        )
        pdfmetrics.registerFont(
            TTFont(
                "roboto-regular", f"{self.assets_root}/fonts/Roboto/Roboto-Regular.ttf"
            )
        )
        pdfmetrics.registerFont(
            TTFont(
                "roboto-medium", f"{self.assets_root}/fonts/Roboto/Roboto-Medium.ttf"
            )
        )

    def build_doc(self):
        data, row_column_spans, actual_values_row_colorfills = self.create_table_rows()
        style = [
            ("GRID", (0, 0), (-1, -1), 0.7, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.Color(red=(179.0 / 255), green=(231.0 / 255), blue=(115 / 255)),
            ),
        ]

        for row_to_fillcolor in actual_values_row_colorfills:
            style.append(row_to_fillcolor)

        for _tuple in row_column_spans:
            style.append(_tuple)

        t = Table(
            data,
            style=style,
            colWidths=[115, 140, 70, 50, 60, 60, 60, 60, 60],
            repeatRows=1,
        )
        self.doc_elements.append(t)

        self.build(
            self.doc_elements, onFirstPage=self.firstPage, onLaterPages=self.laterPages
        )

    def firstPage(self, canvas, doc):
        """
        Defines the fixed features of the first page of the document.
        """
        datestamp = datetime.today().strftime("%d %b %Y")

        canvas.saveState()
        canvas.setTitle(f"Think2044 Indicator Report | {datestamp}")

        canvas.drawImage(
            f"{self.assets_root}/images/logos/mgee_logo.jpeg",
            400,
            480,
            width=75,
            height=75,
        )
        canvas.drawImage(
            f"{self.assets_root}/images/partners/cif.png",
            170,
            175,
            width=115,
            height=80,
            mask="auto",
        )
        canvas.drawImage(
            f"{self.assets_root}/images/partners/adb.png",
            315,
            165,
            width=100,
            height=90,
            mask="auto",
        )
        canvas.drawImage(
            f"{self.assets_root}/images/logos/logo.png", 460, 170, width=90, height=90
        )
        canvas.drawImage(
            f"{self.assets_root}/images/partners/zima.png",
            600,
            170,
            width=90,
            height=90,
            mask="auto",
        )
        canvas.drawImage(
            f"{self.assets_root}/images/partners/wbg.png",
            320,
            100,
            width=270,
            height=50,
            mask="auto",
        )

        canvas.setFont("roboto-bold", 20)
        canvas.drawCentredString(420, 460, "MINISTRY OF GREEN ECONOMY AND ENVIRONMENT")

        canvas.setFont("roboto-medium", 15)
        canvas.drawCentredString(420, 430, "NATIONAL PROJECT COORDINATING UNIT")

        canvas.setFont("roboto-medium", 12)
        canvas.drawCentredString(
            420, 410, "TRANSFORMING LANDSCAPES FOR RESILIENCE AND DEVELOPMENT"
        )

        canvas.setFont("roboto-medium", 25)
        canvas.drawCentredString(420, 330, "Report For Indicator Results")
        canvas.line(250, 320, 580, 320)

        canvas.setFont("roboto-regular", 12)
        canvas.drawString(50, 50, datestamp)

        canvas.setFont("roboto-medium", 14)
        canvas.setFillColorRGB(0.18, 0.47, 0)  # choose your font colour
        canvas.drawString(650, 50, "Think2044.com")
        hostlink = "http://think2044.com"
        canvas.linkURL(hostlink, (650, 70, 750, 35), thickness=0)

        canvas.restoreState()

    def laterPages(self, canvas, doc):
        """
        Since we want pages after the first to look different from the first we define an alternate layout for the fixed
        features of the other pages.
        """
        canvas.saveState()
        canvas.setFont("Times-Roman", 9)
        canvas.drawString(inch, 0.75 * inch, f"Page {doc.page}")
        canvas.setFont("Times-Roman", 20)
        canvas.restoreState()

    def create_table_rows(self):
        """
        Generates lists dynamically for Indicators which are representations of table rows.
        """
        # This list is a represantation of table data. The pre-added items are table rows.
        data = [
            [
                Paragraph("<font size=13><b>Indicator</b></font>"),
                Paragraph("<font size=13><b>Unit of Measure</b></font>"),
                Paragraph("<font size=13><b>Baseline </b></font>"),
                "",
                Paragraph("<font size=13><b>Year 1</b></font>"),
                Paragraph("<font size=13><b>Year 2</b></font>"),
                Paragraph("<font size=13><b>Year 3</b></font>"),
                Paragraph("<font size=13><b>Year 4</b></font>"),
                Paragraph("<font size=13><b>Year 5</b></font>"),
            ]
        ]
        row_column_spans = []
        actual_values_row_colorfills = []

        indicator_start_column = 0
        indicator_start_row = 0
        indicator_end_column = 0
        indicator_end_row = 0
        third_column_sc = 2
        third_column_sr = 0
        third_column_ec = 2
        third_column_er = 0

        # The following 4 values are used dynamically color('grey') each Indicator target row that contains 'Indicator actual data'.
        actual_values_col_colorfill_start = 3
        actual_values_row_colorfill_start = 2
        actual_values_col_colorfill_end = -1
        actual_values_row_colorfill_end = 2

        iter_count = 0

        current_year = datetime.now().year
        for indicator_obj in self.indicators:
            indicator_targets = indicator_obj.indicatortarget_set.all()
            targets_count = indicator_targets.count()

            # This 'row' will have column data such as Indicator name, description, Baseline ,Target, Year 1, Year 2,
            # Year 3, Year 4, Year 5 The 'sub_row' is part of the row and will have column data like Unit of
            # mearsure, Actual, and the rest of values for each year.
            row = []
            sub_row = ["", ""]

            # These variables are to be used to style/set the span for the 'Indicator' column
            indicator_start_row = indicator_end_row + 1
            indicator_end_row = (targets_count * 2) + indicator_end_row

            # Example of tuple: ('SPAN', (0, 1), (0, 2)) This is to be used to style each Indicator row in the table

            if indicator_targets:
                row_column_spans.append(
                    (
                        "SPAN",
                        (indicator_start_column, indicator_start_row),
                        (indicator_end_column, indicator_end_row),
                    )
                )
                for target in indicator_targets:
                    row.append(
                        Paragraph(indicator_obj.name)
                    )  # Append Indicator name as first column)
                    row.append(Paragraph(target.description))
                    row.append(Paragraph(target.baseline_value))
                    row.append(Paragraph("<b>Targets</b>"))
                    try:
                        sub_row.insert(1, Paragraph(f"<b>{target.unit_of_measure.unit_of_measure}</b>"))
                    except AttributeError:
                        sub_row.insert(1, Paragraph(""))

                    sub_row.insert(3, Paragraph("<b>Actual</b>"))

                    sub_row_count = 5

                    # Get target values and actual values for each target in the
                    # Indicator e.g 5000 - year(2022), 8000 - year(2023), 12000 - year(2024)
                    for (yearly_target_value) in target.indicatortargetvalue_set.all().order_by("year"):
                        row.append(
                            f"year-{yearly_target_value.year.year}\n\n{yearly_target_value.target_value}"
                        )
                        if yearly_target_value.year.year <= current_year:
                            try:
                                sub_row.insert(
                                    sub_row_count, Paragraph(str(target.unit_of_measure.get_actual_data(indicator_obj)))
                                )
                            except AttributeError:
                                sub_row.insert(
                                    sub_row_count, Paragraph("")
                                )
                        else:
                            sub_row.insert(
                                sub_row_count, Paragraph("")
                            )
                        sub_row_count += 1

                    data.append(row)
                    data.append(sub_row)

                    # This iter_count is used to create a tuple for styling the Baseline column(by how much the coumn
                    # should span) in the table e.g ('SPAN', (0, 1), (0, 2))
                    if iter_count == 0:
                        third_column_sr += 1
                        third_column_er = third_column_sr + 1
                    else:
                        third_column_sr += 2
                        third_column_er = third_column_sr + 1
                    iter_count += 1

                    row_column_spans.append(
                        (
                            "SPAN",
                            (third_column_sc, third_column_sr),
                            (third_column_ec, third_column_er),
                        )
                    )

                    actual_values_row_colorfills.append(
                        (
                            "BACKGROUND",
                            (
                                actual_values_col_colorfill_start,
                                actual_values_row_colorfill_start,
                            ),
                            (
                                actual_values_col_colorfill_end,
                                actual_values_row_colorfill_end,
                            ),
                            colors.Color(
                                red=(216.0 / 255), green=(215.0 / 255), blue=(215 / 255)
                            ),
                        )
                    )
                    actual_values_row_colorfill_start += 2
                    actual_values_row_colorfill_end += 2

                    # Start over the iteration with empty list
                    row = []
                    # Start over the iteration with two empty rows
                    sub_row = ["", ""]
            else:
                continue

        return (data, row_column_spans, actual_values_row_colorfills)


def sub_project_form(training):
    try:
        from tralard.forms.sub_project import (
            SubProjectForm,
        )  # don't move this import on top
    except:
        pass
    subproject_update_form = SubProjectForm(instance=training)
    return subproject_update_form


def save_image(dirname=None, filename=None, binary_file=None):
    file_system_storage = FileSystemStorage()

    path_name = f"{settings.MEDIA_ROOT}/{dirname}"

    if not os.path.exists(path_name):
        os.makedirs(path_name)

    clean_image_name = filename.lower().replace(' ', '_')

    file_system_storage.save(f"{path_name}/{clean_image_name}", binary_file)

    return f"{dirname}/{clean_image_name}"


def delete_temp_dir(base_dir):
    path_name = f"{BASE_TEMP_DIR}{base_dir}"
    if os.path.exists(path_name):
        shutil.rmtree(path_name)


def delete_temp_file(file_obj):
    clean_image_name = file_obj.name.lower().replace(' ', '_')
    if os.path.exists(clean_image_name):
        os.remove(clean_image_name)


def sub_project_update_form(instance):
    try:
        from tralard.forms.sub_project import SubProjectForm  # don't move this import on top
    except:
        pass
    subproject_update_form = SubProjectForm(instance=instance)
    return subproject_update_form


def sub_project_create_form():
    try:
        from tralard.forms.sub_project import SubProjectForm  # don't move this import on top
    except:
        pass
    subproject_update_form = SubProjectForm()
    return subproject_update_form


def get_subproject_coordinates(subproject_query_obj):
    try:
        subproject_coordinates = subproject_query_obj.ward.location.coords
        return True, subproject_coordinates
    except AttributeError:
        latitude = subproject_query_obj.latitude
        longitude = subproject_query_obj.longitude

        if latitude and longitude:
            subproject_coordinates = (latitude, longitude)
            return True, subproject_coordinates
    return False, ""


def check_image_format_valid(image_path=None, binary_image_file=None, required_format=None):
    """
    Checks if the image of the required format.

    Parameters
    ----------
    image_path: str
        A path to the image
    binary_image_file: bytes
        An in-memory image object

    required_format: str
        A format the image should have.

    Returns
    -------
    bool
    """
    from PIL import Image

    try:
        pil_image_obj = Image.open(image_path or binary_image_file)
        pil_image_obj.verify()
        image_format =  pil_image_obj.format

        if image_format == required_format:
            return True
        return False
    except IOError as err:
        logger.error(f"This image could not be opened due to: {err}")
        return False


def images_pass_checks(images_list, location_point=(-0, 0)):
    """
    Perfoms checks on the images, ensure the image has location data and
    they are within range.

    Parameters
    ----------
    images_list: list
        A list of images, which can be image paths or in-memory binary objects.

    location_point: tuple
        A tuple with latitude and longitude.

    Returns
    -------
    tuple (bool, str)
    """
    for image in images_list:
        image_exif = ExtractImageExif(image_binary=image.open())

        has_location_data = image_exif.has_location_data()
        if not has_location_data:
            return False, f"The uploaded Images have no location data"

        point1 = (image_exif.get_latitude(), image_exif.get_longitude())
        distance = DistanceCalculator(
            point1=point1,
            point2=location_point,
            range_in_kilometers=4
        )

        is_within_range, distance_in_km = distance.is_within_range()
        if not is_within_range:
            return False, f"The uploaded Images are not within range of 4 KM,\
            Distance {distance.round_distance(distance_in_km, num_of_decimals=2)} KM exceeds 4 KM"

    return True, "Valid"



class ExtractImageExif:
    def __init__(self, image_path=None, image_binary=None):
        """
        Sets the initial attributes.

        Parameters
        ----------
        image_path: string
            A path to the image file
        image_binary: bytes
            A bytes-like object e.g An opened in-memory uploaded file.
        """
        self.image = Image(image_path or image_binary)

    def has_exif(self):
        """
        Checks if an iamges has exif meta data.

        Returns
        -------
        bool

        """
        return self.image.has_exif

    def has_location_data(self):
        """
        Checks if the image has location data like GPS Coordinates.k

        Returns
        -------
        bool

        """
        try:
            if all([self.get_latitude(), self.get_longitude()]):
                return True
            return False
        except (KeyError, AttributeError):
            return False

    def get_latitude(self):
        """
        Gets the latitude from the image object.

        Returns
        -------
        None or latitude : float
        """
        try:
            gps_latitude = self.image.gps_latitude
            gps_latitude_ref = self.image.gps_latitude_ref

            converted_coords = self._convert_dms_coordinates_to_dd(gps_latitude, gps_latitude_ref)
            return converted_coords
        except KeyError:
            return None

    def get_longitude(self):
        """
        Gets the latitude from the image object.

        Returns
        -------
        None or longitude : float
        """
        try:
            gps_longitude = self.image.gps_longitude
            gps_longitude_ref = self.image.gps_longitude_ref

            converted_coords = self._convert_dms_coordinates_to_dd(gps_longitude, gps_longitude_ref)
            return converted_coords
        except KeyError:
            return None

    def _convert_dms_coordinates_to_dd(self, coordinate_dms, coordinate_ref):
        """
        Converts the given coordinates in Degree, Minutes, Seconds(DMS) to Decimal Degrees(DD).

        Parameters
        ----------
        coordinates_dms : tuple
            A tuple containing 3 elements, Degrees, Minutes, Seconds
            e.g (27, 21, 3000)

        coordinate_ref: string
            A letter representing a coordinate reference. e.g 'N', 'E', 'S', 'W'

        Returns
        -------
        float

        Example
        -------
        self.__convert_dms_coordinates_to_dd((23, 43, 2322), 'W') returns -15.2343455
        """
        degrees, minutes, seconds = coordinate_dms
        decimal_degrees = degrees + (minutes / 60) + (seconds / 3600)
        if coordinate_ref == "W" or coordinate_ref == "S":
            return -decimal_degrees
        return decimal_degrees


class DistanceCalculator:
    """
    A class for calculating distance from the given cooordinates.
    """
    AVG_EARTH_RADIUS_METERS = 6371000

    def __init__(self, point1=None, point2=None, range_in_kilometers=0):
        """
        Set the initial attributes.

        Parameters
        ----------
        point1: tuoke
            A tuple with two elements representing latitude and longitude respectively
        point2: tuple
             A tuple with two elements representing latitude and longitude respectively

        """
        self.point1 = point1
        self.point2 = point2
        self.range = range_in_kilometers

    def _haversine(self):
        """
        Determines the `great-circle` distance between two points on a given sphere.
        """
        lat1, long1 = self.point1
        lat2, long2 = self.point2

        lat1_in_radians = radians(lat1)
        lat2_in_radians = radians(lat2)
        long1_in_radians = radians(long1)
        long2_in_radians = radians(long2)

        lat_diff = lat2_in_radians - lat1_in_radians
        long_diff = long2_in_radians - long1_in_radians

        haversine = sin(lat_diff * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(long_diff * 0.5) ** 2

        return haversine

    def calculate_distance(self):
        """
        Calcutates the distance between points.
        """
        haversine = self._haversine()
        distance = 2 * self.AVG_EARTH_RADIUS_METERS * asin(sqrt(haversine))
        return distance

    def to_kilometers(self, distance):
        """
        Converts the distance from Meters to Kilometers.

        parameters
        ----------
        distance: float

        Returns
        -------
        distance: float
        """
        return distance / 1000

    def is_within_range(self):
        """
        Calculates the distance between to points is within a given range.
        """
        distance = self.to_kilometers(self.calculate_distance())
        if distance <= self.range:
            return True, distance
        return False, distance

    def round_distance(self, distance, num_of_decimals=0):
        """
        Rounds the distance to a specified number of decimal places.

        Parameters
        ----------
        distance: float
        number_of_decimals: int

        Returns
        -------
        distance: float
        """
        return round(distance, num_of_decimals)
