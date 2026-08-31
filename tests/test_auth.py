import pytest
from app.core.rbac import Permission, RoleChecker, UserRole
from app.core.security import create_access_token, decode_token, get_password_hash, verify_password


def test_password_hashing():
    """Test bcrypt password hashing and verification logic."""
    password = "SuperSecretPassword123!"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_token_generation_and_decoding():
    """Test JWT access token generation, claims, and payload decoding."""
    user_id = "test-user-uuid-12345"
    role = UserRole.ML_ENGINEER.value
    
    token = create_access_token(subject=user_id, role=role)
    assert isinstance(token, str)
    
    payload = decode_token(token)
    assert payload["sub"] == user_id
    assert payload["role"] == role
    assert payload["type"] == "access_token"


def test_rbac_permission_matrix():
    """Test RBAC role permission enforcement across Viewer vs Admin vs ML Engineer."""
    # ML Engineer can start training job
    checker = RoleChecker(required_permissions=[Permission.START_TRAINING_JOB])
    assert checker(UserRole.ML_ENGINEER.value) is True
    
    # Viewer cannot start training job
    with pytest.raises(Exception):
        checker(UserRole.VIEWER.value)
