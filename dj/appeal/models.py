# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admins(models.Model):
    access = models.IntegerField()
    login = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    id_imns = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admins'


class Appeals(models.Model):
    date = models.DateField(blank=True, null=True)
    done = models.TextField(blank=True, null=True)
    result = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)
    what = models.TextField(blank=True, null=True)
    who = models.CharField(max_length=255, blank=True, null=True)
    id_imns = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    imns = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appeals'


class Departments(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'departments'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Imns(models.Model):
    address = models.CharField(max_length=255, blank=True, null=True)
    mail = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    number = models.IntegerField()
    post = models.CharField(max_length=255, blank=True, null=True)
    shot_name = models.CharField(max_length=255, blank=True, null=True)
    unp = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imns'
