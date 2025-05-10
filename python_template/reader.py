from loguru import logger

from python_template.data.urls import UdpUrl
from python_template.data.user_data import UserData, UserEntry


class DataReader:
    """Class to parse input data"""

    def fetch_data(self) -> UserData:
        """Simulate fetching data from an external source."""
        logger.info("Fetching data...")
        return UserData(
            **{
                "users": [
                    UserEntry(url=UdpUrl(url="udp://192.168.0.0:1000"), value=4),
                    UserEntry(url=UdpUrl(url="udp://192.168.0.1:2000"), value=9),
                ]
            }
        )
