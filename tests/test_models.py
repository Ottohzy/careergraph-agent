import pytest
from careergraph.models import (Candidate, Experience, JobDescription, JobSkill, Skill)

def test_create_skill():
    skill =Skill(name="Python")
    assert skill.name == "Python"

def test_create_experience():
    skill1 = Skill(name="Python")
    skill2 = Skill(name="Java")
    experience = Experience(title="Software Engineer", description="Developed software", skills=[skill1, skill2])
    assert experience.title == "Software Engineer"
    assert experience.description == "Developed software"
    assert len(experience.skills) == 2
    assert experience.skills[0].name == "Python"
    assert experience.skills[1].name == "Java"

def test_create_candidate():
    skill1 = Skill(name="Python")
    skill2 = Skill(name="Java")
    experience = Experience(title="Software Engineer", description="Developed software", skills=[skill1, skill2])
    candidate = Candidate(name="John Doe", skills=[skill1, skill2], experiences=[experience])
    assert candidate.name == "John Doe"
    assert len(candidate.skills) == 2
    assert candidate.skills[0].name == "Python"
    assert candidate.skills[1].name == "Java"
    assert len(candidate.experiences) == 1
    assert candidate.experiences[0].title == "Software Engineer"

def test_create_job_skill():
    job_skill = JobSkill(name="Python", required=True)
    assert job_skill.name == "Python"
    assert job_skill.required is True

def test_create_job_description():
    job_skill1 = JobSkill(name="Python", required=True)
    job_skill2 = JobSkill(name="Java", required=False)
    job_description = JobDescription(title="Software Engineer", company="Tech Corp", raw_text="Job description text", skills=[job_skill1, job_skill2])
    assert job_description.title == "Software Engineer"
    assert job_description.company == "Tech Corp"
    assert job_description.raw_text == "Job description text"
    assert len(job_description.skills) == 2
    assert job_description.skills[0].name == "Python"
    assert job_description.skills[0].required is True
    assert job_description.skills[1].name == "Java"
    assert job_description.skills[1].required is False
