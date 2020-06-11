from typing import Optional

from mind_palace.mind_palace_main.business_logic.entities.contents_entity import ContentsEntity
from mind_palace.mind_palace_main.business_logic.entities.learn_policy_entity import LearnPolicyEntity, LearnPolicyType
from mind_palace.mind_palace_main.business_logic.entities.repeat_policy_entity import RepeatPolicyEntity, \
    RepeatPolicyType


class NoteEntity:
    def __init__(self, name: str, contents: ContentsEntity, repeat_policy: Optional[RepeatPolicyEntity] = None,
                 learn_policy: Optional[LearnPolicyEntity] = None, created_time: int = 0,
                 updated_time: int = 0, repeat_time: int = 0, note_id: Optional[str] = None):
        self.name = name
        self.contents = contents

        if repeat_policy is None:
            repeat_policy = RepeatPolicyEntity(RepeatPolicyType.NONE)
        self.repeat_policy = repeat_policy

        if learn_policy is None:
            learn_policy = LearnPolicyEntity(LearnPolicyType.NONE)
        self.learn_policy = learn_policy

        self.created_time = created_time
        self.updated_time = updated_time
        self.repeat_time = repeat_time

        self.note_id = note_id

    @staticmethod
    def from_json(d: dict) -> 'NoteEntity':
        return NoteEntity(
            d['name'],
            ContentsEntity.from_json(d['contents']),
            repeat_policy=RepeatPolicyEntity.from_json(d['repeat_policy']),
            learn_policy=LearnPolicyEntity.from_json(d['learn_policy']),
            note_id=d.get('note_id'),
            created_time=d.get('created_time', 0),
            updated_time=d.get('updated_time', 0),
            repeat_time=d.get('repeat_time', 0),
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'contents': self.contents.to_json(),
            'repeat_policy': self.repeat_policy.to_json(),
            'learn_policy': self.learn_policy.to_json(),
            'created_time': self.created_time,
            'updated_time': self.updated_time,
            'repeat_time': self.repeat_time,
            'note_id': self.note_id
        }
