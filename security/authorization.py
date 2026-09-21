"""Module for handling role-based access control.

This module provides a dependency function `required_role` that can be used
with FastAPI endpoints to enforce role-based authorization.
"""
from fastapi import Depends
from security.dependencies import get_current_user
from exceptions import AuthorizationError
from database import User
from typing import Callable, Any

def required_role(*allowed_roles: str) -> Callable[[User], User]:
    """Factory function to create a FastAPI dependency for role-based authorization.

    This dependency checks if the `current_user` has one of the `allowed_roles`.
    If the user's role is not in the allowed roles, an `AuthorizationError` is raised.

    Args:
        *allowed_roles (str): A variable number of strings representing the roles
                              that are permitted to access the resource.

    Returns:
        Callable[[User], User]: A FastAPI dependency function that, when called,
                                performs the role check and returns the current user if authorized.

    Raises:
        AuthorizationError: If the current user's role is not among the allowed roles.
    """
    def role_checker(
            current_user: User = Depends(get_current_user)
    ) -> User:
        """Internal dependency function that performs the actual role check."""
        if current_user.role not in allowed_roles:
            raise AuthorizationError(
                "You are not authorized to perform this action"
            )
        return current_user
    return role_checker
