import pytest
from dsttbooks.api import Repository
from dsttbooks.errors import *

@pytest.fixture
def repo(tmp_path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    return Repository(str(repo_dir))

def test_missing_book(repo):
    with pytest.raises(BookNotFoundError):
        repo.add_version("missing", "v1", None, {})

def test_duplicate_book(repo):
    repo.create_book("book1")
    with pytest.raises(BookExistsError):
        repo.create_book("book1")

def test_duplicate_version(repo):
    repo.create_book("book1")
    repo.add_version("book1", "v1", None, {})
    with pytest.raises(VersionExistsError):
        repo.add_version("book1", "v1", None, {})

def test_missing_parent_version(repo):
    repo.create_book("book1")
    with pytest.raises(VersionNotFoundError):
        repo.add_version("book1", "v2", "missing_v1", {})

def test_invalid_milestone_sequence(repo):
    repo.create_book("book1")
    repo.add_version("book1", "v1", None, {})
    repo.create_instance("book1", "i1", "v1")
    
    with pytest.raises(InvalidMilestoneSequenceError):
        repo.append_milestone("book1", "i1", 2, {}) # Missing milestone 1

def test_duplicate_milestone(repo):
    repo.create_book("book1")
    repo.add_version("book1", "v1", None, {})
    repo.create_instance("book1", "i1", "v1")
    
    repo.append_milestone("book1", "i1", 1, {})
    with pytest.raises(MilestoneExistsError):
        repo.append_milestone("book1", "i1", 1, {})
