import base64

import pytest

from api.core.handlers.encoding import decode_text, encode_text

pytestmark = pytest.mark.unit


class TestEncodeText:
    def test_returns_valid_base64(self) -> None:
        result = encode_text("hello")
        base64.b64decode(result)  # raises if invalid

    def test_known_value(self) -> None:
        assert encode_text("hello") == "aGVsbG8="

    def test_empty_string(self) -> None:
        assert encode_text("") == ""

    def test_returns_ascii_string(self) -> None:
        result = encode_text("hello world")
        assert result.isascii()

    def test_url_encoding(self) -> None:
        assert encode_text("https://example.com") == base64.b64encode(
            b"https://example.com"
        ).decode("utf-8")


class TestDecodeText:
    def test_known_value(self) -> None:
        assert decode_text("aGVsbG8=") == "hello"

    def test_empty_string(self) -> None:
        assert decode_text("") == ""

    def test_roundtrip(self) -> None:
        original = "https://example.com/some/path?q=1&r=2"
        assert decode_text(encode_text(original)) == original

    def test_roundtrip_unicode(self) -> None:
        original = "https://example.com/café"
        assert decode_text(encode_text(original)) == original
