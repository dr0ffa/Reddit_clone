from pydantic import BaseModel, field_validator
import re

class RegisterUserRequest(BaseModel):
    username: str
    email: str
    passsword: str
    repeat_password: str

    @field_validator("email")
    def validate_email(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 5:
            raise ValueError("Password must be at least 5 characters")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain a digit")
        return v
