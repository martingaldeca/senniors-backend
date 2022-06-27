"""
Create here only abstract models that could be used along all the modules of the application.
"""
import uuid

from django.db import models
from model_utils.models import TimeStampedModel


class UUIDModel(models.Model):
    """
    Abstract model to add uuid to the objects in the database
    """
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class TimeStampedUUIDModel(UUIDModel, TimeStampedModel):
    """
    Abstract model tha add uuid, created and modified to the objects in the database
    """
    class Meta:
        abstract = True
