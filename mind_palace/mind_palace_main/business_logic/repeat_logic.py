from datetime import timedelta
from typing import Optional

from django.conf import settings

from mind_palace.mind_palace_main.business_logic.entities.choice_entity import ChoiceEntity
from mind_palace.mind_palace_main.business_logic.entities.repeat_policy_entity import RepeatPolicyEntity, RepeatPolicyType, TimeOfDay
from mind_palace.mind_palace_main.business_logic.timestamps import timestamp_to_localtime, make_localtime, localtime_to_timestamp, \
    timestamp_now

# Used as repeat time for NONE
FAR_FUTURE = localtime_to_timestamp(make_localtime(2100, 1, 1, 0))


def repeat_note(repeat_policy: RepeatPolicyEntity, choice: Optional[ChoiceEntity] = None,
                reference_time: Optional[int] = None) -> int:
    """ Returns the next repeat time.
      :param repeat_policy: Existing repeat_policy_entity for the note.
      :param choice: Potentially a choice made by the user.
      :param reference_time: Present time.
    """
    if reference_time is None:
        reference_time = timestamp_now()

    if choice is not None:
        if choice.repeat_policy is not None:
            repeat_policy = choice.repeat_policy
        elif choice.skip_to_end:
            # User chose to skip to the end.
            return reference_time - 1

    if repeat_policy.typ == RepeatPolicyType.HOURLY:
        hours = repeat_policy.hours
        assert isinstance(hours, int) and hours > 0
        return reference_time + hours * 3600
    elif repeat_policy.typ == RepeatPolicyType.DAILY:
        days = repeat_policy.days
        assert isinstance(days, int) and days > 0
        localtime = timestamp_to_localtime(reference_time)
        localtime += timedelta(days=days)
        if repeat_policy.time_of_day == TimeOfDay.MORNING:
            hour = settings.MORNING_HOURS
        else:
            hour = settings.EVENING_HOURS
        localtime = make_localtime(localtime.year, localtime.month, localtime.day, hour)
        return localtime_to_timestamp(localtime)
    elif repeat_policy.typ == RepeatPolicyType.NONE:
        return FAR_FUTURE
    else:
        raise ValueError(f'Invalid repeat policy: {repeat_policy.to_json()}')
