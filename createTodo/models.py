from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Category(MPTTModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Category name")
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    slug = models.SlugField(
        verbose_name=_("Category safe URL"),
        max_length=255,
        unique=True,
        null=False,
        blank=False,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Todo(models.Model):
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )
    todo_title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
    )
    todo_description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description"),
    )
    slug = models.SlugField(
        verbose_name=_("Todo safe URL"),
        max_length=255,
        unique=True,
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    status = models.BooleanField(default=True, verbose_name=_("Status"))

    class Meta:
        verbose_name = _("Todo")
        verbose_name_plural = _("Todos")

    def __str__(self):
        return self.todo_title
