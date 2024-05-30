from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, null=True)
    domain = models.CharField(max_length=255, null=True)
    year_founded = models.CharField(max_length=255, null=True)
    industry = models.CharField(max_length=255, null=True)
    size_range = models.CharField(max_length=50, null=True)
    locality = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    linkedin_url = models.URLField(max_length=200, null=True)
    current_employee_estimate = models.IntegerField(null=True)
    total_employee_estimate = models.IntegerField(null=True)

    def __str__(self):
        return self.name
    