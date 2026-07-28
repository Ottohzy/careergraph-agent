import pytest
from pydantic import ValidationError
from careergraph.schema import Job, Analysis, LearningTask, JobSkill, Candidate, Skill, Experience

def test_job_skill_validation():
    # Test valid JobSkill
    skill = JobSkill(name="Python", required=True)
    assert skill.name == "Python"
    assert skill.required is True

    # Test empty name
    with pytest.raises(ValidationError):
        JobSkill(name="", required=True)

    # Test name with only whitespace
    with pytest.raises(ValidationError):
        JobSkill(name="   ", required=True)

def test_candidate_validation():
    # Test valid Candidate
    candidate = Candidate(candidate_id="123", name="John Doe")
    assert candidate.candidate_id == "123"
    assert candidate.name == "John Doe"

    # Test empty candidate_id
    with pytest.raises(ValidationError):
        Candidate(candidate_id="", name="John Doe")

    # Test empty name
    with pytest.raises(ValidationError):
        Candidate(candidate_id="123", name="")

def test_experience_validation():
    # Test valid Experience
    experience = Experience(title="Software Engineer", description="Developed software applications.")
    assert experience.title == "Software Engineer"
    assert experience.description == "Developed software applications."

    # Test empty title
    with pytest.raises(ValidationError):
        Experience(title="", description="Developed software applications.")

    # Test empty description
    with pytest.raises(ValidationError):
        Experience(title="Software Engineer", description="")

def test_skill_validation():
    # Test valid Skill
    skill = Skill(name="Python")
    assert skill.name == "Python"

    # Test empty name
    with pytest.raises(ValidationError):
        Skill(name="")

    # Test name with only whitespace
    with pytest.raises(ValidationError):
        Skill(name="   ")

def test_job_validation():
    # Test valid Job
    job = Job(job_id="job123", title="Software Engineer", description="Develop software applications.")
    assert job.job_id == "job123"
    assert job.title == "Software Engineer"
    assert job.description == "Develop software applications."

    # Test empty job_id
    with pytest.raises(ValidationError):
        Job(job_id="", title="Software Engineer", description="Develop software applications.")

    # Test empty title
    with pytest.raises(ValidationError):
        Job(job_id="job123", title="", description="Develop software applications.")

    # Test empty description
    with pytest.raises(ValidationError):
        Job(job_id="job123", title="Software Engineer", description="")

def test_analysis_validation():
    # Test valid Analysis
    analysis = Analysis(analysis_id="analysis123", job_id="job123", candidate_id="candidate123")
    assert analysis.analysis_id == "analysis123"
    assert analysis.job_id == "job123"
    assert analysis.candidate_id == "candidate123"

    # Test empty analysis_id
    with pytest.raises(ValidationError):
        Analysis(analysis_id="", job_id="job123", candidate_id="candidate123")

    # Test empty job_id
    with pytest.raises(ValidationError):
        Analysis(analysis_id="analysis123", job_id="", candidate_id="candidate123")

    # Test empty candidate_id
    with pytest.raises(ValidationError):
        Analysis(analysis_id="analysis123", job_id="job123", candidate_id="")

def test_learning_task_validation():
    # Test valid LearningTask
    task = LearningTask(task_id="task123", skill_name="Python", description="Learn Python programming.")
    assert task.task_id == "task123"
    assert task.skill_name == "Python"
    assert task.description == "Learn Python programming."

    # Test empty task_id
    with pytest.raises(ValidationError):
        LearningTask(task_id="", skill_name="Python", description="Learn Python programming.")

    # Test empty skill_name
    with pytest.raises(ValidationError):
        LearningTask(task_id="task123", skill_name="", description="Learn Python programming.")

    # Test empty description
    with pytest.raises(ValidationError):
        LearningTask(task_id="task123", skill_name="Python", description="")

def test_learning_task_priority_validation():
    # Test valid priority
    task = LearningTask(task_id="task123", skill_name="Python", description="Learn Python programming.", priority=3)
    assert task.priority == 3

    # Test priority less than 1
    with pytest.raises(ValidationError):
        LearningTask(task_id="task123", skill_name="Python", description="Learn Python programming.", priority=0)

    # Test priority greater than 5
    with pytest.raises(ValidationError):
        LearningTask(task_id="task123", skill_name="Python", description="Learn Python programming.", priority=6)

def test_learning_task_completed_validation():
    # Test valid completed status
    task = LearningTask(task_id="task123", skill_name="Python", description="Learn Python programming.", completed=True)
    assert task.completed is True

    # Test default completed status
    task_default = LearningTask(task_id="task123", skill_name="Python", description="Learn Python programming.")
    assert task_default.completed is False

def test_analysis_match_rate_validation():
    # Test valid match_rate
    analysis = Analysis(analysis_id="analysis123", job_id="job123", candidate_id="candidate123", match_rate=0.75)
    assert analysis.match_rate == 0.75

    # Test match_rate less than 0.0
    with pytest.raises(ValidationError):
        Analysis(analysis_id="analysis123", job_id="job123", candidate_id="candidate123", match_rate=-0.1)

    # Test match_rate greater than 1.0
    with pytest.raises(ValidationError):
        Analysis(analysis_id="analysis123", job_id="job123", candidate_id="candidate123", match_rate=1.1)