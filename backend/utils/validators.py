from typing import Union
from uuid import UUID
import re

def is_valid_uuid(uuid_string: str) -> bool:
    """
    Check if the provided string is a valid UUID
    """
    try:
        UUID(uuid_string)
        return True
    except ValueError:
        return False

def is_valid_email(email: str) -> bool:
    """
    Check if the provided string is a valid email address
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input by removing potentially harmful characters
    """
    # Remove potentially dangerous characters but keep basic punctuation
    sanitized = input_str.replace('<', '&lt;').replace('>', '&gt;')
    return sanitized.strip()

def validate_task_title(title: str) -> tuple[bool, str]:
    """
    Validate task title length and content
    Returns (is_valid, error_message)
    """
    if not title or len(title.strip()) == 0:
        return False, "Task title cannot be empty"

    if len(title) > 255:
        return False, "Task title must be 255 characters or less"

    return True, ""

def validate_task_description(description: str) -> tuple[bool, str]:
    """
    Validate task description length
    Returns (is_valid, error_message)
    """
    if description and len(description) > 1000:
        return False, "Task description must be 1000 characters or less"

    return True, ""