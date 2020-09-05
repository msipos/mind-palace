import uuid

from django.db import models

from mind_palace.mind_palace_main.models import Note


class Attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    note = models.ForeignKey(Note, null=False, on_delete=models.CASCADE)
