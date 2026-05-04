from fastapi.exceptions import HTTPException


class BaseHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(BaseHTTPException):
    def __init__(self, detail: str = "Requested resource not found"):
        super().__init__(status_code=404, detail=detail)


class ForbiddenException(BaseHTTPException):
    def __init__(self, detail: str = "You do not have permission to access this resource"):
        super().__init__(status_code=403, detail=detail)


class ConflictException(BaseHTTPException):
    def __init__(self, detail: str = "Conflict: the resource already exists or is in use"):
        super().__init__(status_code=409, detail=detail)


class NoUpdateException(BaseHTTPException):
    def __init__(self, detail: str = "No updates were made to the resource"):
        super().__init__(status_code=400, detail=detail)


class DuplicateEntryException(BaseHTTPException):
    def __init__(self, detail: str = "Duplicate entry found"):
        super().__init__(status_code=400, detail=detail)


class InvalidIdException(BaseHTTPException):
    def __init__(self, detail: str = "The provided ID is invalid"):
        super().__init__(status_code=400, detail=detail)


class UnauthorizedException(BaseHTTPException):
    def __init__(self, detail: str = "Authentication credentials were missing or invalid"):
        super().__init__(status_code=401, detail=detail)
