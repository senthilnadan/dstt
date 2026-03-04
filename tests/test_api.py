import pytest
from pathlib import Path

from dsttbooks.api import Repository
from dsttbooks.errors import *


@pytest.fixture
def repo(tmp_path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    return Repository(str(repo_dir))


def test_create_book(repo):
    repo.create_book("test_book")
    assert (repo.base_dir / "books" / "test_book").exists()
    assert (repo.base_dir / "books" / "test_book" / "versions").exists()
    assert (repo.base_dir / "books" / "test_book" / "instances").exists()


def test_add_version(repo):
    repo.create_book("book1")
    repo.add_version("book1", "v1", None, {"param": "val"})

    meta = repo.get_version("book1", "v1")
    assert meta["id"] == "v1"
    assert meta["parent"] is None
    assert meta["status"] == "active"
    assert meta["dstt"] == {"param": "val"}


def test_create_instance(repo):
    repo.create_book("book1")
    repo.add_version("book1", "v1", None, {})
    repo.create_instance("book1", "i1", "v1")

    meta = repo.get_instance_meta("book1", "i1")
    assert meta["id"] == "i1"
    assert meta["version"] == "v1"
    assert meta["parent_instance"] is None
    assert meta["status"] == "running"


def test_append_milestone(repo):
    repo.create_book("book1")
    repo.add_version("book1", "v1", None, {})
    repo.create_instance("book1", "i1", "v1")

    repo.append_milestone("book1", "i1", 1, {"step": "1"})
    repo.append_milestone("book1", "i1", 2, {"step": "2"})

    assert (repo._instances_path("book1") / "i1" / "m1.json").exists()
    assert (repo._instances_path("book1") / "i1" / "m2.json").exists()


def test_list_versions(repo):
    repo.create_book("book1")
    repo.add_version("book1", "v1", None, {})
    repo.add_version("book1", "v2", "v1", {})
    
    versions = repo.list_versions("book1")
    assert len(versions) == 2
    # Ensure DSTT body is NOT returned
    assert "dstt" not in versions[0]

def test_list_instances(repo):
    repo.create_book("book1")
    repo.add_version("book1", "v1", None, {})
    repo.create_instance("book1", "i1", "v1")
    repo.create_instance("book1", "i2", "v1", parent_instance="i1")

    instances = repo.list_instances("book1")
    assert len(instances) == 2

def test_mark_version_status_valid(repo):
    repo.create_book("book1")
    repo.add_version("book1", "v1", None, {})
    repo.mark_version_status("book1", "v1", "failed")
    
    meta = repo.get_version("book1", "v1")
    assert meta["status"] == "failed"
    
def test_mark_version_status_invalid(repo):
    repo.create_book("book1")
    repo.add_version("book1", "v1", None, {})
    with pytest.raises(ValueError):
         repo.mark_version_status("book1", "v1", "invalid_status")

def test_prune_unreferenced(repo):
    repo.create_book("book1")
    
    # v1 -> v2
    # v3
    # i1 references v2
    
    repo.add_version("book1", "v1", None, {})
    repo.add_version("book1", "v2", "v1", {})
    repo.add_version("book1", "v3", None, {})
    
    repo.create_instance("book1", "i1", "v2")
    
    pruned_count = repo.prune_unreferenced("book1")
    assert pruned_count == 1 # v3 is pruned
    
    # v1 is kept because v2 relies on it (lineage)
    # v2 is kept because i1 relies on it
    
    versions = repo.list_versions("book1")
    assert len(versions) == 2
    ids = [v["id"] for v in versions]
    assert "v3" not in ids

