import ipaddress

from pydantic import ValidationError
import pytest

from python_template.data.urls import UdpUrl, UrlConstraints
from python_template.data.user_data import UserData, UserEntry


def is_valid_ipv4(ip: str) -> bool:
    """Validate format of IP address.

    Args:
        ip (str): IP address.

    Raises:
        ValueError: error when invalid IP address is passed.

    Returns:
        bool: True if IP is valid, raises ValueError otherwise.
    """
    try:
        ipaddress.IPv4Address(ip)
    except ipaddress.AddressValueError as err:
        raise ValueError("Invalid IPv4 address") from err
    else:
        return True


class TestUserData:
    @pytest.mark.parametrize(
        ("input_ip", "expected_valid", "expected_error"),
        [
            # Valid IPv4 addresses
            ("192.168.1.1", True, None),
            ("255.255.255.255", True, None),
            ("0.0.0.0", True, None),
            ("8.8.8.8", True, None),
            # Invalid IPv4 addresses
            ("999.999.999.999", False, ValueError("Invalid IPv4 address")),
            ("256.256.256.256", False, ValueError("Invalid IPv4 address")),
            ("1234.123.123.123", False, ValueError("Invalid IPv4 address")),
            ("192.168.1", False, ValueError("Invalid IPv4 address")),
            ("", False, ValueError("Invalid IPv4 address")),
            ("abc.def.ghi.jkl", False, ValueError("Invalid IPv4 address")),
        ],
    )
    def test_is_valid_ipv4(
        self, input_ip: str, expected_valid: bool, expected_error: None | ValueError
    ) -> None:
        if expected_valid:
            assert is_valid_ipv4(input_ip) is True
        else:
            with pytest.raises(ValueError, match=str(expected_error)):
                is_valid_ipv4(input_ip)

    @pytest.mark.parametrize(
        ("good_udp_urls", "bad_udp_urls"),
        [
            (
                [
                    "udp://192.168.0.0:1000",
                    "udp://192.168.0.1:2000",
                    "udp://127.0.0.1:5000",
                ],
                [
                    "udp://192.168.1.0",
                    "udp://" + UrlConstraints().max_length * "ip" + ":1000",
                    "udp://192.168:1000",
                    "udp://192.168.1.0:-5",
                    "http://192.168.1.0:1000",
                ],
            )
        ],
    )
    def test_udp_url_format(self, good_udp_urls: list[str], bad_udp_urls: list[str]) -> None:
        for good_url in good_udp_urls:
            UdpUrl(url=good_url)

        for bad_url in bad_udp_urls:
            with pytest.raises(ValidationError):
                UdpUrl(url=bad_url)

    @pytest.mark.parametrize(
        ("user_good_entries", "bad_user_entries"),
        [
            (
                [
                    ("udp://192.168.0.0:1000", 4),
                    ("udp://192.168.0.1:2000", 4),
                    ("udp://127.0.0.1:5000", 4),
                ],
                [
                    ("udp://192.168.1.0", 4),
                    ("udp://" + UrlConstraints().max_length * "ip" + ":1000", 4),
                    ("udp://192.168:1000", 4),
                    ("udp://192.168.1.0:-5", 4),
                    ("http://192.168.1.0:1000", 4),
                    ("udp://192.168.0.0:1000", "four"),
                    ("udp://192.168.0.0:1000", "4"),
                ],
            )
        ],
    )
    def test_user_entries(
        self, user_good_entries: list[tuple[str, int]], bad_user_entries: list[tuple[str, int]]
    ) -> None:
        user_entries_parsed = [
            UserEntry(
                url=UdpUrl(url=good_entry[0]),
                value=good_entry[1],
            )
            for good_entry in user_good_entries
        ]

        for bad_entry in bad_user_entries:
            with pytest.raises(ValidationError):
                UserEntry(url=UdpUrl(url=bad_entry[0]), value=bad_entry[1])

        UserData(users=user_entries_parsed)
