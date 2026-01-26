from loguru import logger

from python_template.data.user_data import UserData


class Processor:
    """Class to handle input data and process it."""

    def process_data(self, data: UserData) -> UserData:
        """Process data by checking its format."""
        logger.info("Processing data...")

        for data_item in data.users:
            logger.info(f"User url: {data_item.url.url}")
            data_item.value = data_item.value**2

        return data
