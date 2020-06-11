import abc


class BaseSectionEntity(abc.ABC):
    @staticmethod
    def from_json(d: dict) -> 'BaseSectionEntity':
        typ = d['type']

        if typ == 'markdown':
            return MarkdownSectionEntity.from_json(d)
        else:
            raise ValueError(f'Invalid section type="{typ}"')

    @abc.abstractmethod
    def to_json(self) -> dict:
        pass


class MarkdownSectionEntity(BaseSectionEntity):
    def __init__(self, text: str, hidden=False):
        self.text = text
        self.hidden = hidden

    @staticmethod
    def from_json(d: dict):
        assert d['type'] == 'markdown'
        return MarkdownSectionEntity(d['text'], d.get('hidden', False))

    def to_json(self) -> dict:
        return {
            'type': 'markdown',
            'text': self.text,
            'hidden': self.hidden
        }
