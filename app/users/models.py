# import os
# from pathlib import Path

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from ..core.models import CoreModel

# from imagekit.models import ProcessedImageField
# from imagekit.processors import ResizeToFill


# from ..utils.storage import OverwriteStorage


class UserManager(BaseUserManager):
    """
    Customized manager that creates new users only with a password and a
    username.
    """

    def create_user(self, username, password, **kwargs):
        """
        Creates a new user only with a password and a username.
        """
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password, **kwargs):
        user = self.create_user(username, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def generate_username(self, first_name, last_name):
        """
        Generates a username from first name and last name.
        """
        first_name = first_name.strip()
        last_name = last_name.strip()

        if first_name and last_name:
            base_name = " ".join((first_name, last_name))
        else:
            base_name = first_name or last_name
            if not base_name:
                raise ValueError(
                    "Either 'first_name' or 'last_name' must not be empty."
                )

        if not self.filter(username=base_name).exists():
            generated_username = base_name
        else:
            counter = 0
            while True:
                counter += 1
                test_name = f"{base_name} {counter}"
                if not self.filter(username=test_name).exists():
                    generated_username = test_name
                    break

        return generated_username


# def avatar_path(instance, filename):
#     return f"avatar_{str(instance.pk)}.jpg"


class User(PermissionsMixin, AbstractBaseUser, CoreModel):

    USERNAME_FIELD = "username"

    username = models.CharField(max_length=255, unique=True)

    first_name = models.CharField(max_length=255, blank=True)

    last_name = models.CharField(max_length=255, blank=True)

    email = models.EmailField()

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    # avatar = ProcessedImageField(
    #     upload_to=avatar_path,
    #     storage=OverwriteStorage(),
    #     processors=[ResizeToFill(200, 200)],
    #     format="JPEG",
    #     options={"quality": 100},
    #     blank=True,
    #     null=True,
    # )

    # reverse: profile

    objects = UserManager()

    def __str__(self):
        # Strip white spaces from the name parts
        first_name = self.first_name.strip()
        last_name = self.last_name.strip()

        if first_name and last_name:
            name = " ".join((self.first_name, self.last_name))
        else:
            name = first_name or last_name or self.username

        return name

    # def delete(self, *args, **kwargs):
    #     file_path = os.path.join(settings.MEDIA_ROOT, self.avatar.name)
    #     avatar_file = Path(file_path)
    #     if avatar_file.is_file():
    #         os.remove(file_path)
    #     super(User, self).delete(*args, **kwargs)

    @property
    def full_name(self) -> str:
        return self.__str__()


class Profile(CoreModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        on_delete=models.CASCADE,
    )

    address_1 = models.CharField(max_length=256, blank=True)

    address_2 = models.CharField(max_length=256, blank=True)

    zip_code = models.CharField(max_length=20, blank=True)

    city = models.CharField(max_length=256, blank=True)

    state = models.CharField(max_length=128, blank=True)

    country = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
