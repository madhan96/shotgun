from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings


class UserType(models.Model):
    type = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return "the user type is %s and id is %s" % (self.type, self.id)


def get_default_usertype():
    return UserType.objects.get(type="PRODUCTION")


def get_default_artist_usertype():
    return UserType.objects.get(type="ARTIST")


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        username,
        usertype=get_default_usertype(),
        password=None,
        is_active=True,
        is_staff=False,
        is_admin=False,
    ):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(email=self.normalize_email(email), username=username)
        user_obj.usertype = usertype
        user_obj.set_password(password)  # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, username=None, password=None):
        user = self.create_user(
            email, username=username, password=password, is_staff=True
        )
        return user

    def create_superuser(self, email, username=None, password=None):
        user = self.create_user(
            email, username=username, password=password, is_staff=True, is_admin=True,
        )
        return user


class User(AbstractBaseUser):
    usertype = models.ForeignKey(
        UserType,
        related_name="users",
        on_delete=models.CASCADE,
        default=get_default_artist_usertype,
    )
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=False)  # staff user non superuser
    admin = models.BooleanField(default=False)  # superuser
    timestamp = models.DateTimeField(auto_now_add=True)
    # confirm     = models.BooleanField(default=False)
    # confirmed_date     = models.DateTimeField(default=False)

    USERNAME_FIELD = "username"  # username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = ["email"]  # ['username'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_username(self):
        if self.username:
            return self.username
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    # @property
    # def is_active(self):
    #     return self.active


# Create your models here.


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=60, unique=True)
    deadline = models.DateField()


def get_project_by_name(project_name):
    return Project.objects.get(name=project_name)


class Sequence(models.Model):
    name = models.CharField(max_length=60, unique=True)
    status = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    project = models.ForeignKey(
        Project, related_name="sequences", on_delete=models.CASCADE
    )


def get_sequence_by_name(seq_name):
    return Sequence.objects.get(name=seq_name)


class Shot(models.Model):
    shotcode = models.CharField(max_length=60, unique=True)
    status = models.CharField(max_length=60)
    cut_in = models.DecimalField(max_digits=9, decimal_places=2)
    cut_out = models.DecimalField(max_digits=9, decimal_places=2)
    cut_duration = models.DecimalField(max_digits=9, decimal_places=2)
    sequence = models.ForeignKey(
        Sequence, related_name="shots", on_delete=models.CASCADE
    )


def get_shot_by_name(code):
    return Shot.objects.get(shotcode=code)


class Task(models.Model):
    task_name = models.CharField(max_length=60, unique=True)
    pipeline_step = models.CharField(max_length=60)
    status = models.CharField(max_length=60)
    startdate = models.DateField()
    duedate = models.DateField()
    link = models.ForeignKey(Shot, related_name="tasks", on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="assignedtasks"
    )

    reviewer = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="taskstoreview",
    )
