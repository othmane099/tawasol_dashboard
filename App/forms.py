from django import forms
from django.core.validators import MinValueValidator


# config form to init the app
class ConfigForm(forms.Form):
    """
    Form for configuring the dashboard settings.

    The form includes fields for specifying the total number of employees, total number of units, and performance
    hours offset. All fields are required, and the 'MinValueValidator' is used to ensure that the entered values are
    greater than or equal to 1.
    """

    total_employees_number = forms.IntegerField(
        required=True,
        validators=[MinValueValidator(1)]
    )
    total_unities_number = forms.IntegerField(
        required=True,
        validators=[MinValueValidator(1)]
    )
    performance_hours_offset = forms.IntegerField(
        required=True,
        validators=[MinValueValidator(1)]
    )
