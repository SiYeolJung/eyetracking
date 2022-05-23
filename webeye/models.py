from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser



class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Lecture(models.Model):
    lid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    teaches = models.CharField(max_length=20)
    adddate = models.DateTimeField(db_column='addDate', blank=True, null=True)  # Field name made lowercase.
    course = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lecture'


class Scrap(models.Model):
    owner = models.OneToOneField('Users', models.DO_NOTHING, db_column='owner', primary_key=True)
    lecture = models.ForeignKey(Lecture, models.DO_NOTHING, db_column='lecture')
    adddate = models.DateTimeField(db_column='addDate', blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'scrap'
        unique_together = (('owner', 'lecture'),)


class Users(models.Model):
    uid = models.IntegerField(primary_key=True)
    id = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    adddate = models.DateTimeField(db_column='addDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users'


class WebeyeLecture(models.Model):
    id = models.BigAutoField(primary_key=True)
    lecture_name = models.CharField(max_length=40)
    teacher = models.CharField(max_length=20)
    mark_count = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'webeye_lecture'


class WebeyeProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.TextField()
    nickname = models.CharField(max_length=40)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'webeye_profile'


class WebeyeProfileMarkLecture(models.Model):
    id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(WebeyeProfile, models.DO_NOTHING)
    lecture = models.ForeignKey(WebeyeLecture, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'webeye_profile_mark_lecture'
        unique_together = (('profile', 'lecture'),)
