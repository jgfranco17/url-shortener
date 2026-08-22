import base64


def encode_text(original_string: str) -> str:
    """Encode text to a base64 string.

    Args:
        original_string (str): Base string to be encoded

    Returns:
        str: ASCII-readable base64 encoded string.
    """
    text_bytes = original_string.encode("utf-8")
    encoded_bytes = base64.b64encode(text_bytes)
    encoded_string = encoded_bytes.decode("utf-8")
    return encoded_string


def decode_text(encoded_string: str) -> str:
    """Decode a base64 string back to text.

    Args:
        encoded_string (str): ASCII-readable base64 encoded string.

    Returns:
        str: Decoded original text.
    """
    decoded_bytes = base64.b64decode(encoded_string)
    original_text = decoded_bytes.decode("utf-8")
    return original_text
