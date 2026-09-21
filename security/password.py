"""Module for handling password hashing and verification.

This module utilizes `pwdlib` to securely hash and verify user passwords.
"""
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
  """Hashes a plain-text password using the recommended password hashing algorithm.

  Args:
      password (str): The plain-text password to hash.

  Returns:
      str: The securely hashed password string.
  """
  return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
  """Verifies a plain-text password against a hashed password.

  Args:
      password (str): The plain-text password to verify.
      hashed_password (str): The hashed password to compare against.

  Returns:
      bool: True if the password matches the hashed password, False otherwise.
  """
  return password_hash.verify(password, hashed_password)
