import json
import uuid
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import VersionMeta, InstanceMeta, Milestone
from .errors import (
    BookExistsError, BookNotFoundError,
    VersionExistsError, VersionNotFoundError,
    InstanceExistsError, InstanceNotFoundError,
    InvalidMilestoneSequenceError, MilestoneExistsError,
    VersionReferencedError
)
class Repository:
    """Manages DSTT Books append-only state logic on the filesystem."""

    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)

    def _book_path(self, book_id: str) -> Path:
        return self.base_dir / "books" / book_id

    def _versions_path(self, book_id: str) -> Path:
        return self._book_path(book_id) / "versions"
        
    def _instances_path(self, book_id: str) -> Path:
        return self._book_path(book_id) / "instances"
        
    def _ensure_book(self, book_id: str):
        if not self._book_path(book_id).exists():
            raise BookNotFoundError(book_id)

    def _write_json(self, path: Path, data: dict):
        # Write to temp file then rename for atomic creation
        tmp_path = path.with_suffix('.tmp')
        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        tmp_path.rename(path)
        
    def _read_json(self, path: Path) -> dict:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def create_book(self, book_id: str):
        book_path = self._book_path(book_id)
        if book_path.exists():
            raise BookExistsError(book_id)
            
        self._versions_path(book_id).mkdir(parents=True)
        self._instances_path(book_id).mkdir(parents=True)

    def add_version(self, book_id: str, version_id: str, parent_id: Optional[str], dstt: Dict[str, Any]):
        self._ensure_book(book_id)
        ver_path = self._versions_path(book_id) / f"{version_id}.json"
        
        if ver_path.exists():
            raise VersionExistsError(version_id)
        
        if parent_id is not None:
            parent_path = self._versions_path(book_id) / f"{parent_id}.json"
            if not parent_path.exists():
                raise VersionNotFoundError(parent_id)

        meta: VersionMeta = {
            "id": version_id,
            "parent": parent_id,
            "status": "active",
            "dstt": dstt
        }
        
        self._write_json(ver_path, meta)

    def get_version(self, book_id: str, version_id: str) -> VersionMeta:
        self._ensure_book(book_id)
        ver_path = self._versions_path(book_id) / f"{version_id}.json"
        if not ver_path.exists():
            raise VersionNotFoundError(version_id)
            
        return self._read_json(ver_path)

    def create_instance(self, book_id: str, instance_id: str, version_id: str, parent_instance: Optional[str] = None):
        self._ensure_book(book_id)
        
        ver_path = self._versions_path(book_id) / f"{version_id}.json"
        if not ver_path.exists():
            raise VersionNotFoundError(version_id)
            
        inst_dir = self._instances_path(book_id) / instance_id
        if inst_dir.exists():
            raise InstanceExistsError(instance_id)
            
        if parent_instance is not None:
            parent_inst_path = self._instances_path(book_id) / parent_instance
            if not parent_inst_path.exists():
                raise InstanceNotFoundError(parent_instance)

        inst_dir.mkdir(parents=True)
        meta_path = inst_dir / "meta.json"
        
        meta: InstanceMeta = {
            "id": instance_id,
            "version": version_id,
            "parent_instance": parent_instance,
            "status": "running"
        }
        
        self._write_json(meta_path, meta)

    def append_milestone(self, book_id: str, instance_id: str, milestone_number: int, state_dict: Dict[str, Any]):
        self._ensure_book(book_id)
        
        inst_dir = self._instances_path(book_id) / instance_id
        if not inst_dir.exists():
            raise InstanceNotFoundError(instance_id)
            
        m_path = inst_dir / f"m{milestone_number}.json"
        if m_path.exists():
            raise MilestoneExistsError(f"{instance_id}/m{milestone_number}")
            
        # Ensure sequentiality
        if milestone_number > 1:
            prev_m_path = inst_dir / f"m{milestone_number - 1}.json"
            if not prev_m_path.exists():
                raise InvalidMilestoneSequenceError(f"Missing milestone {milestone_number - 1}")

        meta: Milestone = {
            "milestone": milestone_number,
            "state": state_dict
        }
        
        self._write_json(m_path, meta)

    def get_instance_meta(self, book_id: str, instance_id: str) -> InstanceMeta:
        self._ensure_book(book_id)
        inst_dir = self._instances_path(book_id) / instance_id
        if not inst_dir.exists():
            raise InstanceNotFoundError(instance_id)
            
        return self._read_json(inst_dir / "meta.json")

    def list_versions(self, book_id: str) -> List[VersionMeta]:
        self._ensure_book(book_id)
        ver_dir = self._versions_path(book_id)
        versions = []
        for p in ver_dir.glob("*.json"):
            data = self._read_json(p)
            data.pop("dstt", None) # Do not return full body
            versions.append(data)
        return versions

    def list_instances(self, book_id: str) -> List[InstanceMeta]:
        self._ensure_book(book_id)
        inst_dir = self._instances_path(book_id)
        instances = []
        for p in inst_dir.iterdir():
            if p.is_dir():
                meta_path = p / "meta.json"
                if meta_path.exists():
                    instances.append(self._read_json(meta_path))
        return instances

    def mark_version_status(self, book_id: str, version_id: str, status: str):
        self._ensure_book(book_id)
        if status not in {"active", "failed", "deprecated", "experimental"}:
            raise ValueError(f"Invalid status: {status}")
            
        ver_path = self._versions_path(book_id) / f"{version_id}.json"
        if not ver_path.exists():
            raise VersionNotFoundError(version_id)
            
        data = self._read_json(ver_path)
        data["status"] = status
        self._write_json(ver_path, data)

    def prune_unreferenced(self, book_id: str):
        self._ensure_book(book_id)
        
        # 1. Gather all versions referenced by instances
        referenced_versions = set()
        for inst in self.list_instances(book_id):
            referenced_versions.add(inst["version"])
            
        # 2. Gather all parent dependencies
        # Build map of (parent -> set of children)
        ver_dir = self._versions_path(book_id)
        parent_map = {}
        all_versions = set()
        
        for p in ver_dir.glob("*.json"):
            v_id = p.stem
            all_versions.add(v_id)
            data = self._read_json(p)
            parent = data.get("parent")
            if parent:
                parent_map.setdefault(parent, set()).add(v_id)

        # 3. Find prunable versions
        # A version is prunable if:
        # - not in referenced_versions
        # - has no children (or its children are also prunable)
        
        prunable = set()
        
        # Bottom-up approach: keep removing unreferenced leaf nodes until stable
        while True:
            newly_pruned = False
            for v_id in all_versions - prunable:
                if v_id in referenced_versions:
                    continue
                    
                # A node is a leaf if it has no children, or all its children are already going to be pruned
                is_leaf = True
                children = parent_map.get(v_id, set())
                for child in children:
                    if child not in prunable:
                        is_leaf = False
                        break
                        
                if is_leaf:
                    prunable.add(v_id)
                    newly_pruned = True
                    
            if not newly_pruned:
                break
                
        # 4. Perform pruning
        for v_id in prunable:
            p = ver_dir / f"{v_id}.json"
            p.unlink()
            
        return len(prunable)
