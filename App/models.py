from django.db import models


class Configuration(models.Model):
    """
    Model representing configuration settings for the application.

    Attributes:
        total_employees (IntegerField): The total number of employees configured.
        total_units (IntegerField): The total number of units configured.
        performance_hours_offset (IntegerField): The offset in hours for performance calculations.
    """
    total_employees = models.IntegerField()
    total_units = models.IntegerField()
    performance_hours_offset = models.IntegerField()