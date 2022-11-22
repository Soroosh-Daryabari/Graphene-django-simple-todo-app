from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


def upload_profile_image(instance, filename):
    return "{}/{}".format(instance.username, filename)


class Accounts(AbstractUser):
    profile_image = models.ImageField(
        null=True,
        blank=True,
        verbose_name=_("Profile image"),
        upload_to=upload_profile_image,
    )
    account_id = models.SlugField(
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        verbose_name=_("Account ID"),
    )
    about_user = models.TextField(null=True, blank=True, verbose_name=_("About user"))
    first_name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name=_("First name"),
    )
    last_name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name=_("Last name"),
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.get_full_name()
