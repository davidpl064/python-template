import re
from urllib.parse import urlparse

from pydantic import BaseModel, model_validator


class UrlConstraints(BaseModel):
    """Class model to define generic URLs format parameters."""

    max_length: int = 2083
    allowed_schemes: list[str] = ["udp", "rtmp"]


class UdpUrl(BaseModel):
    """Class model to define UDP URLs."""

    url: str
    ip: str | None = None
    port: int | None = None

    @model_validator(mode="before")
    @classmethod
    def _validate_format(cls, values: dict[str, str]) -> dict[str, str | int]:
        url = values.get("url", "")

        constraints = UrlConstraints(max_length=2083, allowed_schemes=["udp"])
        if len(url) > constraints.max_length:
            raise ValueError("URL length exceeds max. limit.")

        # Parse the URL to get components
        parsed_url = urlparse(url)

        if parsed_url.scheme not in constraints.allowed_schemes:
            raise ValueError("URL header is incorrect. Must be udp://.")

        # Check if there's an IP and port in the netloc
        if ":" in parsed_url.netloc:
            ip, port = parsed_url.netloc.split(":")
            # Validate IP
            ip = ip.strip()
            ip_pattern = re.compile(
                r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
            )
            flag_valid_ip = bool(ip_pattern.match(ip))

            if not flag_valid_ip:
                raise ValueError("Invalid IP format.")

            # Validate port
            port_parsed = int(port)
            if not (0 <= port_parsed <= 65535):
                raise ValueError("Port must be between 0 and 65535.")

            return {"url": url, "ip": ip, "port": port_parsed}

        # If no IP and port are found, raise an error
        raise ValueError("Invalid IP or port.")
