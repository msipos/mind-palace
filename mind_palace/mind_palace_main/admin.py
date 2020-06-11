from django.contrib import admin

from mind_palace.mind_palace_main.models import Collection
from mind_palace.mind_palace_main.models.note_model import Note, SnoozeEvent

for m in [Collection, Note, SnoozeEvent]:
    admin.site.register(m)
