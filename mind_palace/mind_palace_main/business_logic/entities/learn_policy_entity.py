class LearnPolicyType:
    NONE = 'none'
    EXPONENTIAL = 'exponential'


class LearnPolicyEntity:
    def __init__(self, typ: str):
        self.typ = typ
        assert typ in [LearnPolicyType.NONE, LearnPolicyType.EXPONENTIAL]

    def to_json(self) -> dict:
        d = {'type': self.typ}
        return d

    @staticmethod
    def from_json(d: dict) -> 'LearnPolicyEntity':
        return LearnPolicyEntity(d['type'])
