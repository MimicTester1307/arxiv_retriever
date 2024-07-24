from arxiv_retriever.cli import app

import pytest
from typer.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_fetch(mocker):
    return mocker.patch('arxiv_retriever.cli.fetch_papers')


def test_extract_paper_metadata_output(runner, mock_fetch, mocker):
    """Test extract_paper_metadata output."""
    summary = 'This is a test paper summary that is intentionally longer than 100 characters to test the truncation functionality of `extract_paper_metadata`.'
    mock_fetch.return_value = [
        {
            'title': 'Test Paper',
            'authors': ['John Doe'],
            'published': '2024-07-05T12:00:00Z',
            'link': 'http://arxiv.org/abs/2407.0001',
            'summary': summary
        }
    ]
    mocker.patch('typer.confirm', return_value=False)  # Mock the confirm to return False
    result = runner.invoke(app, ["fetch", "cs.AI", "--limit", "1"])
    assert result.exit_code == 0
    assert "1. Test Paper" in result.stdout
    assert "Authors: John Doe" in result.stdout
    assert "Published: 2024-07-05T12:00:00Z" in result.stdout
    assert "Link: http://arxiv.org/abs/2407.0001" in result.stdout

    expected_truncated_summary = summary[:100] + "..."
    assert f"Summary: {expected_truncated_summary}" in result.stdout
    assert len(expected_truncated_summary) == 103  # 100 characters plus 3 for the ellipsis
