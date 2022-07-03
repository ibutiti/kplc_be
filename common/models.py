from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True, null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True
