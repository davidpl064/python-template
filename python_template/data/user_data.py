from pydantic import BaseModel

from python_template.data.urls import UdpUrl


class UserEntry(BaseModel, strict=True):
    """Class model to define structure of each user entry data."""

    url: UdpUrl
    value: int


class UserData(BaseModel):
    """Class model to define collections of user data entries."""

    users: list[UserEntry]
