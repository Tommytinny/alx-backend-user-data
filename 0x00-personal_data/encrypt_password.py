#!/usr/bin/env python3
"""encrypt password module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Hashing a password using bcrypt """
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ checking valid password """
    password_bytes = password.encode('utf-8')
    if bcrypt.checkpw(password_bytes, hashed_password):
        return True
    else:
        return False
