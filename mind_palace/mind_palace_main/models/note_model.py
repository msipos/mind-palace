import json
import uuid
from datetime import datetime
from typing import List, Optional

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet

from mind_palace.mind_palace_main.business_logic.entities.contents_entity import ContentsEntity
from mind_palace.mind_palace_main.business_logic.entities.learn_policy_entity import LearnPolicyEntity
from mind_palace.mind_palace_main.business_logic.entities.note_entity import NoteEntity
from mind_palace.mind_palace_main.business_logic.entities.repeat_policy_entity import RepeatPolicyEntity
from mind_palace.mind_palace_main.business_logic.timestamps import timestamp_now, timestamp_to_localtime
from mind_palace.mind_palace_main.models import Collection
from mind_palace.mind_palace_main.utils import AuthorizationError


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    collection = models.ForeignKey(Collection, null=False, on_delete=models.CASCADE,
                                   help_text='Collection this note belongs to.')

    # Basics, title and contents
    name = models.TextField(null=False, help_text='Name/title of the note. Always unencrypted.')
    json_contents = models.TextField(null=True, help_text='Contents of the note in JSON format.')

    # Whether it has been deleted or archived
    archived = models.BooleanField(null=False, default=False, help_text='Has the note been archived?')

    # Metadata contains repeat_policy, learn_policy and optional data_gather_policy
    json_metadata = models.TextField(null=True, help_text='Note metadata in JSON format.')

    # Timestamps (kept in UTC time)
    updated_time = models.BigIntegerField(null=False, default=0, help_text='When was note last updated')
    created_time = models.BigIntegerField(null=False, default=0, help_text='When was note created')
    repeat_time = models.BigIntegerField(null=False, default=0, help_text='When will note be repeated')
    last_repeat_time = models.BigIntegerField(null=False, default=0, help_text='When was note last repeated')

    def get_snooze_events(self) -> List['SnoozeEvent']:
        return SnoozeEvent.objects.filter(note=self)

    @property
    def name_or_untitled(self) -> str:
        """ Returns the name of the note or 'Untitled' in case of it is an empty string.  Useful for the view layer. """
        name = self.name.strip()
        if name == '':
            return 'Untitled'
        return name

    @property
    def created_time_local(self) -> datetime:
        return timestamp_to_localtime(self.created_time)

    @property
    def updated_time_local(self) -> datetime:
        return timestamp_to_localtime(self.updated_time)

    @property
    def repeat_time_local(self) -> datetime:
        return timestamp_to_localtime(self.repeat_time)

    @property
    def last_repeat_time_local(self) -> Optional[datetime]:
        if self.last_repeat_time == 0:
            return None
        return timestamp_to_localtime(self.last_repeat_time)

    @staticmethod
    def get_active_notes(collection: Collection, reference_time: Optional[int] = None) -> QuerySet:
        """
        Authorization-safe getter for notes. Gets all active notes for a collection.
        :param collection: Collection to query.
        :param reference_time: Reference time. If not passed, it is now.
        """
        if reference_time is None:
            reference_time = timestamp_now()
        return Note.objects.filter(
            collection=collection, archived=False, repeat_time__lt=reference_time
        ).order_by('repeat_time')

    @staticmethod
    def get_note_by_id(user: User, n: str):
        """
        Authorization-safe getter for notes.
        """

        note = Note.objects.get(id=n)
        if user not in note.collection.users.all():
            raise AuthorizationError('User %r not authorized.' % user)
        return note

    def __str__(self):
        return '%s (%s)' % (self.name, self.id)

    def to_entity(self) -> NoteEntity:
        contents_dict = json.loads(self.json_contents)
        metadata_dict = json.loads(self.json_metadata)
        return NoteEntity(
            self.name, ContentsEntity.from_json(contents_dict),
            repeat_policy=RepeatPolicyEntity.from_json(metadata_dict['repeat_policy']),
            learn_policy=LearnPolicyEntity.from_json(metadata_dict['learn_policy']),
            created_time=self.created_time,
            updated_time=self.updated_time,
            repeat_time=self.repeat_time,
            note_id=str(self.id),
            collection_id=str(self.collection_id),
            collection_name=self.collection.name,
            archived=self.archived
        )

    def from_entity(self, entity: NoteEntity, load_name=True, load_contents=True, load_metadata=True):
        """ Load the model from the entity. """
        if load_name:
            self.name = entity.name
        if load_contents:
            self.json_contents = json.dumps(entity.contents.to_json())
        if load_metadata:
            self.json_metadata = json.dumps({
                'repeat_policy': entity.repeat_policy.to_json(),
                'learn_policy': entity.learn_policy.to_json()
            })


class SnoozeEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    note = models.ForeignKey(Note, null=False, on_delete=models.CASCADE)
    dt = models.DateTimeField(null=False)
    int_payload = models.IntegerField(null=True)

    class Meta:
        ordering = ['dt']
