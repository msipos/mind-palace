from typing import Optional

from mind_palace.mind_palace_main.business_logic.entities.repeat_policy_entity import RepeatPolicyEntity


class ChoiceEntity:
    def __init__(self, repeat_policy: Optional[RepeatPolicyEntity] = None, skip_5_min=False,
                 overwrite_repeat_policy=False, choice_html: Optional[str] = None, choice_index: Optional[int] = None,
                 keyboard_shortcut: Optional[str] = None):
        """ This represents a choice provided to the user by the repeater. """
        self.repeat_policy = repeat_policy
        self.skip_5_min = skip_5_min
        self.overwrite_repeat_policy = overwrite_repeat_policy

        if repeat_policy is not None:
            assert skip_5_min is False
        if overwrite_repeat_policy:
            assert repeat_policy is not None

        # Text of the choice
        self.choice_html = choice_html
        # Sort order of the choice in the UI
        self.choice_index = choice_index
        # Keyboard shortcut
        self.keyboard_shortcut = keyboard_shortcut

    def to_json(self) -> dict:
        rp = None
        if self.repeat_policy is not None:
            rp = self.repeat_policy.to_json()
        return {
            'repeat_policy': rp,
            'skip_5_min': self.skip_5_min,
            'overwrite_repeat_policy': self.overwrite_repeat_policy,
            'choice_html': self.choice_html,
            'choice_index': self.choice_index,
            'keyboard_shortcut': self.keyboard_shortcut
        }

    @staticmethod
    def from_json(d: dict) -> 'ChoiceEntity':
        rp = None
        if d.get('repeat_policy') is not None:
            rp = RepeatPolicyEntity.from_json(d['repeat_policy'])
        return ChoiceEntity(
            rp,
            skip_5_min=d.get('skip_5_min', False),
            overwrite_repeat_policy=d.get('overwrite_repeat_policy', False),
            choice_html=d.get('choice_html'),
            choice_index=d.get('choice_index'),
            keyboard_shortcut=d.get('keyboard_shortcut')
        )
