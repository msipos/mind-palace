from django.conf import settings
from django.test import TestCase
from jinja2 import Environment

from mind_palace.mind_palace_main.business_logic.entities.choice_entity import ChoiceEntity
from mind_palace.mind_palace_main.business_logic.entities.repeat_policy_entity import RepeatPolicyEntity, RepeatPolicyType
from mind_palace.mind_palace_main.business_logic.repeat_logic import repeat_note, FAR_FUTURE
from mind_palace.mind_palace_main.business_logic.timestamps import timestamp_now, timestamp_to_localtime, localtime_to_timestamp, \
    make_localtime


class TestTime(TestCase):
    def test_time(self):
        now = timestamp_now()
        dt = timestamp_to_localtime(now)
        now2 = localtime_to_timestamp(dt)
        assert now == now2

    def test_repeat_logic(self):
        reference_time = localtime_to_timestamp(make_localtime(2020, 1, 1, 13))
        repeat_policy = RepeatPolicyEntity(RepeatPolicyType.NONE)
        assert repeat_note(repeat_policy, reference_time=reference_time) == FAR_FUTURE

        choice = ChoiceEntity(skip_5_min=True)
        assert repeat_note(repeat_policy, choice, reference_time) - reference_time == 5*60

        # Check hourly
        repeat_policy = RepeatPolicyEntity.from_json({
            'type': 'hourly',
            'hours': 36
        })
        t2 = repeat_note(repeat_policy, reference_time=reference_time)
        assert t2 - reference_time == (36 * 3600)

        # Check daily
        repeat_policy = RepeatPolicyEntity.from_json({
            'type': 'daily',
            'days': 3,
            'timeOfDay': 'morning'
        })
        t2 = repeat_note(repeat_policy, reference_time=reference_time)
        hours_between = (t2 - reference_time) / 3600
        self.assertEqual(hours_between, 3 * 24 - (13 - settings.MORNING_HOURS))


class TestVarious(TestCase):
    def test_jinja(self):
        env = Environment()
        env.globals.update({
            'hi': 5,
            'foo': lambda x: x + 5
        })
        t = env.from_string('Test render {{hi}}, {{foo(hi)}}')
        self.assertEqual(t.render(), 'Test render 5, 10')
