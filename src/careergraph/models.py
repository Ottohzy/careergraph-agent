from dataclasses import dataclass

@dataclass
class Skill:
    name: str

@dataclass
class Experience:
    title: str
    description: str
    skills: list[Skill]

@dataclass
class Candidate:
    name: str
    skills: list[Skill]
    experiences: list[Experience]

@dataclass
class JobSkill:
    name: str
    required: bool = True

@dataclass
class JobDescription:
    title: str
    company: str
    raw_text: str
    skills: list[JobSkill]