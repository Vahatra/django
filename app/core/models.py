from model_utils.fields import UUIDField
from model_utils.models import TimeStampedModel
from rest_framework.exceptions import ValidationError

from django.core.cache import cache
from django.db import IntegrityError, models
from django.db.models.signals import post_delete, post_save

from ..utils.utils import slugify


class CoreModel(TimeStampedModel):
    """
    Model to use as a base.
    """

    uuid = UUIDField(primary_key=True, version=4, editable=False)

    class Meta:
        abstract = True
        default_permissions = ()

    def __str__(self):
        return str(self.pk)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"


class EntityMixin(CoreModel):
    """
    Model to use as a base for label/codename models.
    """

    label = models.CharField("label", max_length=255)

    codename = models.SlugField(
        "codename",
        max_length=255,
        unique=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        abstract = True
        ordering = ("label",)

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        try:
            self.codename = slugify(self.label)
            super().save(*args, **kwargs)
        except IntegrityError:
            raise ValidationError("codename for that label already exists.")

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        post_save.connect(entity_cache_handler, cls)
        post_delete.connect(entity_cache_handler, cls)


# if the enetity is cached then delete cache when the entity is deleted, comment this otherwise.
def entity_cache_handler(sender, **kwargs):
    cache.delete_pattern(f"{sender.__name__.lower()}_*")
