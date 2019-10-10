from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class Trainer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Set User model.

    This model is inherited from default user model.
    """

    COMMON, RARE = 1, 2
    USER_TYPES = ((COMMON, _("Common user")), (RARE, _("Rare")))

    email = models.EmailField(_("Email address"), unique=True)
    user_type = models.PositiveSmallIntegerField(
        _("User type"), choices=USER_TYPES, default=COMMON
    )
    user_code = models.CharField(_("User code"), max_length=10, blank=True)
    user_text = models.TextField(_("User text"), blank=True)
    trainer = models.ForeignKey(
        Trainer, related_name="users", on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        """
        Meta class of Users model.

        This class set verbose_name and verbose_name_plural.
        """

        ordering = ["date_joined"]
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        app_label = "users"

    def __str__(self):
        """
        __str__ method.

        This method return annotation of object.
        """
        return self.email
