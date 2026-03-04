class BookException(Exception):
    """Base exception for dsttbooks failures."""
    pass


class StructuralViolationError(BookException):
    """Base exception for operations violating strict append-only rules."""
    pass


class BookExistsError(StructuralViolationError):
    pass


class BookNotFoundError(StructuralViolationError):
    pass


class VersionExistsError(StructuralViolationError):
    pass


class VersionNotFoundError(StructuralViolationError):
    pass


class InstanceExistsError(StructuralViolationError):
    pass


class InstanceNotFoundError(StructuralViolationError):
    pass


class InvalidMilestoneSequenceError(StructuralViolationError):
    pass


class MilestoneExistsError(StructuralViolationError):
    pass


class VersionReferencedError(StructuralViolationError):
    pass


class CoreOperationError(StructuralViolationError):
    pass
