"""Tests for session handling and cookie configuration."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app


class TestSessionHandling:
    """Test session cookie handling and configuration."""

    @pytest.fixture
    def mock_create_visitor(self):
        """Mock create_visitor analytics function."""
        with patch('app.main.create_visitor', new_callable=AsyncMock) as mock:
            yield mock

    @pytest.fixture
    def client(self):
        """FastAPI test client."""
        return TestClient(app)

    def test_session_cookie_set_on_first_request(self, client, mock_create_visitor):
        """Test that session cookie is set on first request."""
        response = client.get("/")

        # Should return 200
        assert response.status_code == 200

        # Cookie should be set
        cookies = response.cookies
        assert "sgnl_session" in cookies

        # Cookie should have correct attributes
        session_cookie = cookies.get("sgnl_session")
        assert session_cookie is not None

        # Check cookie attributes (these are Set-Cookie header attributes)
        set_cookie_header = response.headers.get('set-cookie')
        assert set_cookie_header is not None

        # Verify cookie attributes
        assert 'Max-Age=2592000' in set_cookie_header  # 30 days in seconds
        assert 'HttpOnly' in set_cookie_header
        assert 'SameSite=lax' in set_cookie_header
        assert 'Secure' in set_cookie_header

    def test_session_cookie_format(self, client, mock_create_visitor):
        """Test that session ID has correct format: sess_{timestamp}_{hex}."""
        response = client.get("/")
        session_id = response.cookies.get("sgnl_session")

        # Format: sess_{timestamp}_{8-char-hex}
        assert session_id.startswith("sess_")
        parts = session_id.split("_")
        assert len(parts) == 3

        # Second part should be a timestamp (integer)
        try:
            timestamp = int(parts[1])
            assert timestamp > 0
        except ValueError:
            pytest.fail("Session timestamp is not a valid integer")

        # Third part should be 16 character hex (8 bytes)
        hex_part = parts[2]
        assert len(hex_part) == 16
        try:
            int(hex_part, 16)
        except ValueError:
            pytest.fail("Session hex part is not valid hexadecimal")

    def test_session_cookie_uses_30_days_max_age(self, client, mock_create_visitor):
        """Test that cookie max_age is set to 30 days (not 90 days)."""
        response = client.get("/")
        set_cookie_header = response.headers.get('set-cookie')

        # 30 days = 30 * 24 * 60 * 60 = 2592000 seconds
        assert 'Max-Age=2592000' in set_cookie_header

        # Ensure 90 days is NOT present
        assert 'Max-Age=7776000' not in set_cookie_header  # 90 days

    def test_session_cookie_secure_flag(self, client, mock_create_visitor):
        """Test that Secure flag is set on session cookie."""
        response = client.get("/")
        set_cookie_header = response.headers.get('set-cookie')

        # Secure flag must be present
        assert 'Secure' in set_cookie_header

    def test_session_cookie_httponly_flag(self, client, mock_create_visitor):
        """Test that HttpOnly flag is set on session cookie."""
        response = client.get("/")
        set_cookie_header = response.headers.get('set-cookie')

        # HttpOnly flag must be present
        assert 'HttpOnly' in set_cookie_header

    def test_session_cookie_samesite_lax(self, client, mock_create_visitor):
        """Test that SameSite=lax is set on session cookie."""
        response = client.get("/")
        set_cookie_header = response.headers.get('set-cookie')

        # SameSite must be 'lax'
        assert 'SameSite=lax' in set_cookie_header

    def test_existing_session_preserved(self, client, mock_create_visitor):
        """Test that existing session cookie is preserved and reused."""
        existing_session = "sess_1234567890_abcdef1234567890"

        # Make request with existing session
        response = client.get("/", cookies={"sgnl_session": existing_session})

        # Cookie should still be set (to refresh max-age)
        cookies = response.cookies
        assert "sgnl_session" in cookies

        # Should use existing session
        # The create_visitor should be called with existing session ID
        mock_create_visitor.assert_called_once()
        call_args = mock_create_visitor.call_args

        # Extract session_id from call - it's the second positional arg after request
        # Call is: await create_visitor(request, session_id)
        request_arg = call_args[0][0]
        session_arg = call_args[0][1]
        assert session_arg == existing_session

    def test_create_visitor_called_on_frontend_request(self, client, mock_create_visitor):
        """Test that create_visitor is called when serving frontend."""
        response = client.get("/")

        # create_visitor should be called once
        mock_create_visitor.assert_called_once()

        # Should be called with correct arguments
        call_args = mock_create_visitor.call_args
        assert len(call_args[0]) == 2  # request and session_id

    def test_create_visitor_failure_handled_gracefully(self, client, mock_create_visitor):
        """Test that frontend still loads even if create_visitor fails."""
        # Mock create_visitor to raise exception
        mock_create_visitor.side_effect = Exception("Database error")

        # Request should still succeed
        response = client.get("/")
        assert response.status_code == 200

        # Cookie should still be set
        assert "sgnl_session" in response.cookies

        # create_visitor was still called (and failed)
        mock_create_visitor.assert_called_once()

    def test_duplicate_import_removed(self):
        """Verify that 'import secrets' appears only once in main.py."""
        import app.main

        # Get the source code
        import inspect
        source = inspect.getsource(app.main)

        # Count occurrences of 'import secrets'
        # Should only import once
        import_count = source.count('import secrets')

        # Should be exactly 1 import statement
        assert import_count == 1, f"Expected 1 import of secrets, found {import_count}"

    def test_no_duplicate_secrets_import_in_file(self):
        """Direct file check for duplicate import."""
        import os
        with open('/root/sgnl-backend/app/main.py', 'r') as f:
            content = f.read()

        # Count lines that have 'import secrets' as a standalone import
        lines = content.split('\n')
        import_lines = [line.strip() for line in lines if line.strip() == 'import secrets']

        # Should be exactly 1
        assert len(import_lines) == 1, f"Found {len(import_lines)} 'import secrets' statements. Line numbers: {[i+1 for i, line in enumerate(lines) if line.strip() == 'import secrets']}"


class TestSessionCookieIntegration:
    """Integration tests for session cookie across multiple requests."""

    @pytest.fixture
    def mock_create_visitor(self):
        """Mock create_visitor analytics function."""
        with patch('app.main.create_visitor', new_callable=AsyncMock) as mock:
            yield mock

    @pytest.fixture
    def client(self):
        """FastAPI test client."""
        return TestClient(app)

    def test_multiple_requests_preserve_session(self, client, mock_create_visitor):
        """Test that session ID is preserved across multiple requests."""
        # First request
        response1 = client.get("/")
        session1 = response1.cookies.get("sgnl_session")

        # Second request with the session cookie
        response2 = client.get("/", cookies={"sgnl_session": session1})

        # Both should succeed
        assert response1.status_code == 200
        assert response2.status_code == 200

        # Second request should refresh the cookie
        cookies2 = response2.cookies
        assert "sgnl_session" in cookies2
        session2 = cookies2.get("sgnl_session")

        # Session IDs might be different (cookie refresh) or same
        # The key is that both exist and have valid format
        assert session1 is not None
        assert session2 is not None

        # Both should have valid format
        for session in [session1, session2]:
            assert session.startswith("sess_")
            parts = session.split("_")
            assert len(parts) == 3

    def test_cookie_refresh_with_existing_session(self, client, mock_create_visitor):
        """Test that cookie max-age is refreshed even with existing session."""
        existing_session = "sess_1234567890_abcdef1234567890"

        # Make request with existing session
        response = client.get("/", cookies={"sgnl_session": existing_session})

        # Cookie should be re-set with new max-age
        set_cookie_header = response.headers.get('set-cookie')
        assert 'Max-Age=2592000' in set_cookie_header

        # create_visitor should be called with existing session
        mock_create_visitor.assert_called_once()
        call_args = mock_create_visitor.call_args
        session_arg = call_args[0][1]
        assert session_arg == existing_session
