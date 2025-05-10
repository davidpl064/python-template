import subprocess
import sys
from unittest import mock

from python_template.data.urls import UdpUrl
from python_template.data.user_data import UserData, UserEntry
from python_template.main import main
from python_template.output import Reporter
from python_template.reader import DataReader


class TestIntegration:
    @mock.patch.object(DataReader, "fetch_data")
    @mock.patch.object(Reporter, "save_results")
    def test_full_pipeline_with_mocked_io(
        self, mock_reporter: mock.Mock, mock_data_reader: mock.Mock
    ) -> None:
        """Test the entire pipeline with mocked input/output blocks."""
        # Mock "DataReader" to return custom data instead of real execution
        mock_data_reader.return_value = UserData(
            **{
                "users": [
                    UserEntry(url=UdpUrl(url="udp://192.168.0.0:1000"), value=4),
                    UserEntry(url=UdpUrl(url="udp://192.168.0.1:2000"), value=9),
                ]
            }
        )

        # Run the main pipeline
        main()

        # Verify "DataReader" `fetch_data()` was called once
        mock_data_reader.assert_called_once()

        # Verify `process_data()` is called with mock's return value
        expected_processed_data = UserData(
            **{
                "users": [
                    UserEntry(url=UdpUrl(url="udp://192.168.0.0:1000"), value=16),
                    UserEntry(url=UdpUrl(url="udp://192.168.0.1:2000"), value=81),
                ]
            }
        )
        for index, data_item in enumerate(mock_data_reader.return_value.users):
            assert data_item.value == expected_processed_data.users[index].value

        # Verify "Reporter" `save_results()` was called with expected processed data
        mock_reporter.assert_called_once_with(expected_processed_data)

    def test_full_pipeline(self) -> None:
        """Test the entire pipeline without mocks."""
        # Run the main pipeline
        main()

    def test_full_pipeline_fire_exec(self) -> None:
        """Execute entire pipeline using the CLI behaviour of fire library."""
        result = subprocess.run(
            [sys.executable, "python_template/main.py"], capture_output=True, text=True
        )

        assert "Pipeline completed." in result.stderr  # Adjust based on your expected output
        assert result.returncode == 0
