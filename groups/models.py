from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class VisitorGroup(models.Model):
    name = models.CharField(max_length=200)
    group_size = models.IntegerField(null=True)
    allow_group_login = models.BooleanField(null=True)

    def __str__(self):
        return self.name


class Visitor(models.Model):
    visitorgroup = models.ForeignKey(VisitorGroup, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    family_number = models.CharField(max_length=300, null=True)
    address = models.CharField(default="", max_length=100)
    number = models.CharField(default="", max_length=100)

    def __str__(self):
        return self.text


class IntervallDate(models.Model):
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)

    def __str__(self):
        return str(self.start_date)


class ChurchDayVisitorGroup(models.Model):
    visitorgroup_id = models.IntegerField(null=True)
    group_size = models.IntegerField(null=True)
    name = models.CharField(max_length=200)
    date = models.DateField(blank=True, null=True)
    visitor_list = models.JSONField(null=True)

    def __str__(self):
        return self.name



