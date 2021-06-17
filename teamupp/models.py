import hashlib

import requests

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

# Create your models here.
from app.utils import generate_animal_name


class Placements(models.Model):
    placement = ArrayField(
        ArrayField(
            models.IntegerField()
        )
    )


class Company(models.Model):
    name = models.CharField(max_length=400, unique=True)

    def __str__(self):
        return self.name


class TeamUppUser(AbstractUser):
    profile_picture_url = models.URLField(null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        has_email_changed: bool = False
        if self.id:
            current_user_information = TeamUppUser.objects.get(pk=self.id)
            has_email_changed = current_user_information.email != self.email

        if self.profile_picture_url is None or has_email_changed:
            email = self.email.lower().encode('utf-8')
            hashed_email = hashlib.md5(email).hexdigest()
            self.profile_picture_url = f"https://www.gravatar.com/avatar/{hashed_email}?f=y&default=retro"

        if self.company is None:
            default_company_name = '[Default Company]'

            if (company := Company.objects.filter(name=default_company_name)).exists():
                company = company.first()
            else:
                company = Company(name=default_company_name)
                company.save()

            self.company = company

        return super().save(*args, **kwargs)


class Project(models.Model):
    name = models.CharField(max_length=400, null=True, blank=True)
    start_date = models.DateField(auto_now_add=True)
    duration = models.IntegerField()
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        self.name = generate_animal_name(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"The {self.name} Project"


class Group(models.Model):
    name = models.CharField(max_length=400, null=True)
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user2', null=True,
                              blank=True)

    def save(self, *args, **kwargs):
        self.name = generate_animal_name(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Week(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return F"Week {self.start} - {self.end} ({self.project})"

