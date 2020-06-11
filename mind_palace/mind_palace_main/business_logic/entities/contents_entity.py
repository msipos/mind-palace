from typing import List

from mind_palace.mind_palace_main.business_logic.entities.section_entity import BaseSectionEntity


class ContentsEntity:
    def __init__(self, sections: List[BaseSectionEntity]):
        self.sections = sections

    @staticmethod
    def from_json(d: dict):
        sections = []
        sections_json = d['sections']
        for section_json in sections_json:
            sections.append(BaseSectionEntity.from_json(section_json))
        return ContentsEntity(sections)

    def to_json(self) -> dict:
        return {
            'sections': [s.to_json() for s in self.sections]
        }
