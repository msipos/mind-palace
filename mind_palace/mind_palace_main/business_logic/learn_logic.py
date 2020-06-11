from typing import List

from mind_palace.mind_palace_main.business_logic.entities.choice_entity import ChoiceEntity
from mind_palace.mind_palace_main.business_logic.entities.learn_policy_entity import LearnPolicyEntity, LearnPolicyType
from mind_palace.mind_palace_main.business_logic.entities.repeat_policy_entity import RepeatPolicyEntity


def _choice_text(repeat_policy: RepeatPolicyEntity, shortcut: int) -> str:
    return f'Repeat in <b>{repeat_policy.to_human_readable()}</b> ({shortcut})'


def create_note_choices(repeat_policy: RepeatPolicyEntity, learn_policy: LearnPolicyEntity) -> List[ChoiceEntity]:
    out = [
        ChoiceEntity(skip_to_end=True,
                     choice_html='Skip to end (1)',
                     choice_index=1),
    ]
    if learn_policy.typ == LearnPolicyType.NONE:
        out.append(ChoiceEntity(repeat_policy=repeat_policy,
                                choice_html=_choice_text(repeat_policy, 3),
                                choice_index=3))
    elif learn_policy.typ == LearnPolicyType.EXPONENTIAL:
        rep = repeat_policy.copy(0.5)
        out.append(ChoiceEntity(rep,
                                overwrite_repeat_policy=True,
                                choice_html=_choice_text(rep, 2),
                                choice_index=2))
        out.append(ChoiceEntity(repeat_policy=repeat_policy,
                                choice_html=_choice_text(repeat_policy, 3),
                                choice_index=3))
        rep = repeat_policy.copy(1.5)
        out.append(ChoiceEntity(rep,
                                overwrite_repeat_policy=True,
                                choice_html=_choice_text(rep, 4),
                                choice_index=4))
        rep = repeat_policy.copy(2)
        out.append(ChoiceEntity(rep,
                                overwrite_repeat_policy=True,
                                choice_html=_choice_text(rep, 5),
                                choice_index=5))
    return out
