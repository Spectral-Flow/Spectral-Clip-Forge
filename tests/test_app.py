"""
Test Basic Application Functionality
"""
import pytest
import json


def test_index_page(client):
    """Test that index page loads"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Spectral Clip Forge" in response.data


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "operational"
    assert data["service"] == "Spectral Clip Forge"


def test_api_status(client):
    """Test API status endpoint"""
    response = client.get("/api/status")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "ready"
    assert "version" in data


def test_404_error(client):
    """Test 404 error handling"""
    response = client.get("/nonexistent-page")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data


def test_contributors_page(client):
    """Test contributors page loads"""
    response = client.get("/dashboard/contributors")
    assert response.status_code == 200
    assert b"Forge Masters" in response.data


def test_dashboard_page(client):
    """Test dashboard page loads"""
    response = client.get("/dashboard/")
    assert response.status_code == 200
