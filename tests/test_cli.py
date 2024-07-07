from itertools import combinations
import pytest
from typer.testing import CliRunner
from arxiv_retriever.cli import app


@pytest.fixture
def runner():
    return CliRunner()


def test_fetch_command_success(runner, mocker):
    mock_fetch = mocker.patch("arxiv_retriever.cli.fetch_papers")
    mock_fetch.return_value = [
        {
            'title': 'Test Paper',
            'authors': ['John Doe'],
            'published': '2024-07-05T12:00:00Z',
            'link': 'http://arxiv.org/abs/2407.0001',
            'summary': 'Test paper summary.'
        }
    ]
    result = runner.invoke(app, ["fetch", "cs.AI", "--limit", "1"])
    print(f"Mock called: {mock_fetch.called}")
    print(f"Mock call args: {mock_fetch.call_args}")
    print(f"Result: {result.stdout}")
    assert result.exit_code == 0
    assert "Test Paper" in result.stdout
    assert "John Doe" in result.stdout
    mock_fetch.assert_called_once_with(["cs.AI"], 1)