from fastapi import HTTPException


class UsernameAlreadyExists(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Username already exists")


class UsernameNotExist(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Username does not exist")


class WrongPassword(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Password is not correct")
