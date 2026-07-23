import pytest

from careergraph.data_loader import (get_candidate_skills, load_candidate_profile, load_jd_text)

def test_load_candidate_profile_valid_json(tmp_path):
    # Create a temporary JSON file with valid content
    candidate_data = {"name": "John Doe", "skills": ["Python", "Java"]}
    file_path = tmp_path / "candidate_profile.json"
    file_path.write_text('{"name": "John Doe", "skills": ["Python", "Java"]}', encoding="utf-8")

    result = load_candidate_profile(file_path)
    assert result == candidate_data

def test_load_candidate_profile_invalid_json(tmp_path):
    # Create a temporary JSON file with invalid content (not a JSON object)
    file_path = tmp_path / "invalid_profile.json"
    file_path.write_text('["Python", "Java"]', encoding="utf-8")

    with pytest.raises(ValueError, match="Candidate profile must be a JSON object."):
        load_candidate_profile(file_path)

def test_get_candidate_skills_valid_input():
    candidate_profile = {"name": "John Doe", "skills": ["Python", "Java", "C++"]}
    result = get_candidate_skills(candidate_profile)
    assert result == {"python", "java", "c++"}

def test_get_candidate_skills_invalid_input():
    candidate_profile = {"name": "John Doe", "skills": "Python, Java, C++"}  # skills should be a list
    with pytest.raises(ValueError, match="Candidate skills must be a list."):
        get_candidate_skills(candidate_profile)

def test_load_jd_text_valid_input(tmp_path):
    # Create a temporary text file with valid content
    jd_content = "This is a sample job description."
    file_path = tmp_path / "sample_jd.txt"
    file_path.write_text(jd_content, encoding="utf-8")

    result = load_jd_text(file_path)
    assert result == jd_content

def test_load_jd_text_empty_input(tmp_path):
    # Create a temporary text file with empty content
    file_path = tmp_path / "empty_jd.txt"
    file_path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="Job description cannot be empty."):
        load_jd_text(file_path)

def test_load_jd_text_whitespace_input(tmp_path):
    # Create a temporary text file with whitespace content
    file_path = tmp_path / "whitespace_jd.txt"
    file_path.write_text("   \n   ", encoding="utf-8")

    with pytest.raises(ValueError, match="Job description cannot be empty."):
        load_jd_text(file_path)

def test_load_jd_text_strip_whitespace(tmp_path):
    # Create a temporary text file with leading and trailing whitespace
    jd_content = "   This is a sample job description.   "
    file_path = tmp_path / "whitespace_jd.txt"
    file_path.write_text(jd_content, encoding="utf-8")

    result = load_jd_text(file_path)
    assert result == "This is a sample job description."  # Ensure whitespace is stripped

def test_load_jd_text_nonexistent_file():
    # Test loading a non-existent file
    file_path = "nonexistent_file.txt"
    with pytest.raises(FileNotFoundError):
        load_jd_text(file_path)
