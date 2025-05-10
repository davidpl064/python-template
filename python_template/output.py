import json
import tempfile
from pathlib import Path

from loguru import logger

from python_template.data.user_data import UserData


class Reporter:
    """Class to write processed data to output files."""

    def save_results(self, results: UserData) -> None:
        """Save results and print them to file."""
        logger.info("Saving results...")

        for data_item in results.users:
            data_item.url.url = data_item.url.url

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = Path(temp_dir).resolve() / "results.json"
            with open(temp_file, "w") as f:
                json.dump(results.model_dump(), f)

        logger.info("Results saved.")
