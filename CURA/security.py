import hashlib
import re

def hash_password(password):
    """
    this secure password in secure hash instead of plain text so no one can see it.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def is_strong_password(password):
    """
    check if passsword is strong or not.
    """
    if len(password) < 8:
        return False, "Password must be 8 characters long."
    if not re.search("[0-9]", password):
        return False, "Password must contain a number."
    if not re.search("[!@#$%^&*]", password):
        return False, "Password must contain a special character (!@#$)."
    return True, "Strong Password"

def verify_password(stored_password, provided_password):
    """
    checks the users correct password if it is wrong or right.
    """
    return stored_password == hash_password(provided_password)