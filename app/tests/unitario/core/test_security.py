import pytest
from datetime import timedelta, datetime, timezone
from jose import jwt
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)

def test_password_hashing():
    password = "minhasenhaforte"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("senhaincorreta", hashed) is False

def test_create_access_token_default_expiration():
    data = {"sub": "admin@exemplo.com"}
    token = create_access_token(data)
    
    # Decodificar o token para validar o payload
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    assert payload["sub"] == "admin@exemplo.com"
    assert "exp" in payload
    # exp default é 7 dias (ver security.py) - apenas garantindo que é um inteiro
    assert isinstance(payload["exp"], int)

def test_create_access_token_custom_expiration():
    data = {"sub": "user@exemplo.com"}
    expires = timedelta(minutes=15)
    token = create_access_token(data, expires_delta=expires)
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    assert payload["sub"] == "user@exemplo.com"
    assert "exp" in payload
    

