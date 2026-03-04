from typing import TypedDict, Any

# Structural types for validation
class VersionMeta(TypedDict):
    id: str
    parent: str
    status: str
    dstt: dict[str, Any]

class InstanceMeta(TypedDict):
    id: str
    version: str
    parent_instance: str
    status: str

class Milestone(TypedDict):
    milestone: int
    state: dict[str, Any]
