import fire
from loguru import logger

from python_template.output import Reporter
from python_template.processor import Processor
from python_template.reader import DataReader


def main() -> None:
    """Initialize pipeline blocks and execute it."""
    data_reader = DataReader()
    processor = Processor()
    reporter = Reporter()

    data = data_reader.fetch_data()
    data_processed = processor.process_data(data)
    reporter.save_results(data_processed)
    logger.info("Pipeline completed.")


if __name__ == "__main__":
    fire.Fire(main)
