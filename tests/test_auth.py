"""
Test Authentication Routes
"""
import pytest
import json

def test_register_disabled_by_default(client):
    """Test that registration is disabled by default"""
    response = client.post('/api/auth/register',
                          data=json.dumps({
                              'username': 'testuser',
                              'email': 'test@example.com',
                              'password': 'testpass123'
                          }),
                          content_type='application/json')
    assert response.status_code == 403

def test_login_disabled_by_default(client):
    """Test that login is disabled by default"""
    response = client.post('/api/auth/login',
                          data=json.dumps({
                              'username': 'testuser',
                              'password': 'testpass123'
                          }),
                          content_type='application/json')
    assert response.status_code == 403

def test_logout_disabled_by_default(client):
    """Test that logout is disabled by default"""
    response = client.post('/api/auth/logout')
    assert response.status_code == 403

def test_current_user_disabled_by_default(client):
    """Test current user endpoint when auth is disabled"""
    response = client.get('/api/auth/me')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['authenticated'] is False
