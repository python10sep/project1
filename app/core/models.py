"""
Database models
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

#################################################
# TOPIC :customizing authentication in django   #
#################################################
"""
How to customize default django user model and authentication?
https://docs.djangoproject.com/en/4.1/topics/auth/customizing


REFER FULL EXAMPLE HERE -
https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#a-full-example

Additional notes:

"""

#################################################


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email: str, password: str = None, **extra_fields):
        """
        create, save and return a new user

        Args:
            email: will be set as new default value for `username` field.
            password: encrypted password via hashing
            **extra_fields: using this arbitrary keyword args option to
                          accommodate any additional user fields in future.

        Returns:
            user object
        """

        if not email:
            raise ValueError("User *MUST* have email address")

        # with `self.model` we are already associated with default user model
        # as we are deriving from `BaseUserManager`
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # user without email normalization
        # user = self.model(email=email, **extra_fields)

        # best practice to hash password using super class method `set_password`
        user.set_password(password)

        # best practice to use `using=self.db` when using multiple database
        # saving a new object using `UserManager`
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        when we call `python manage.py createsuperuser` command, django calls
        this method.
        So make sure you are spelling the method name correctly.

        Refer -
        https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#django.contrib.auth.models.CustomUserManager.create_superuser

        Returns:

        """

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # user active by default
    is_staff = models.BooleanField(default=False)

    # Assign `UserManager` in django to the custom user class.
    # When using ORM queries we say `objects.get()`, `objects.create()` etc.
    # All those methods come from this objects attribute.
    # We are overriding default Manager with our custom Manager here.
    objects = UserManager()

    USERNAME_FIELD = "email"  # overrides the default user field from base class
