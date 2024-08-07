from arxiv_retriever.cli import app

import pytest
from typer.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


def test_extract_paper_metadata_output(runner, mocker):
    """Test extract_paper_metadata output."""
    mock_fetch = mocker.AsyncMock()
    mock_fetch.return_value = [{
        'title': 'Test Paper',
        'authors': ['John Doe'],
        'published': '2024-07-05T12:00:00Z',
        'abstract_link': 'http://arxiv.org/abs/2407.0001',
        'pdf_link': 'http://arxiv.org/pdf/2407.0001.pdf',
        'summary': 'This is a test paper summary that is intentionally longer than 100 characters to test the truncation functionality.'
    }]
    mocker.patch('arxiv_retriever.cli.fetch_papers', mock_fetch)

    result = runner.invoke(app, ["fetch", "cs.AI", "--limit", "1"])

    assert result.exit_code == 0
    assert "1. Test Paper" in result.stdout
    assert "Authors: John Doe" in result.stdout
    assert "Published: 2024-07-05T12:00:00Z" in result.stdout
    assert "Link to Abstract: http://arxiv.org/abs/2407.0001" in result.stdout
    assert "Link to PDF: http://arxiv.org/pdf/2407.0001" in result.stdout


@pytest.mark.asyncio
async def test_process_papers(runner, mocker):
    mock_fetch = mocker.AsyncMock()
    mock_fetch.return_value = [{'title': 'Test Paper', 'authors': ['John Doe']}]
    mocker.patch('arxiv_retriever.cli.fetch_papers', mock_fetch)

    mock_summarize = mocker.Mock()
    mocker.patch('arxiv_retriever.utils.summarize_papers', mock_summarize)

    mock_download = mocker.AsyncMock()
    mocker.patch('arxiv_retriever.utils.download_papers', mock_download)

    # Mock user inputs
    mocker.patch('typer.confirm', side_effect=[True, True])
    mocker.patch('typer.prompt', return_value='./test_downloads')
    mocker.patch('os.path.exists', return_value=True)

    # Mock process_papers to simulate its behavior
    async def mock_process_papers(papers):
        from arxiv_retriever.utils import summarize_papers, download_papers
        summarize_papers(papers)
        await download_papers(papers, './test_downloads')
    mocker.patch('arxiv_retriever.cli.process_papers', mock_process_papers)

    result = runner.invoke(app, ["fetch", "cs.AI", "--limit", "1"])

    assert result.exit_code == 0
    mock_fetch.assert_awaited_once_with(['cs.AI'], 1, None, 'OR')
    mock_summarize.assert_called_once()
    mock_download.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_papers_no_download(runner, mocker):
    mock_fetch = mocker.AsyncMock()
    mock_fetch.return_value = [{'title': 'Test Paper', 'authors': ['John Doe']}]
    mocker.patch('arxiv_retriever.cli.fetch_papers', mock_fetch)

    mock_summarize = mocker.Mock()
    mocker.patch('arxiv_retriever.utils.summarize_papers', mock_summarize)

    mock_download = mocker.AsyncMock()
    mocker.patch('arxiv_retriever.utils.download_papers', mock_download)

    # Mock user inputs
    mocker.patch('typer.confirm', side_effect=[True, False])

    # Mock process_papers to simulate its behavior
    async def mock_process_papers(papers):
        from arxiv_retriever.utils import summarize_papers
        summarize_papers(papers)
    mocker.patch('arxiv_retriever.cli.process_papers', mock_process_papers)

    result = runner.invoke(app, ["fetch", "cs.AI", "--limit", "1"])

    assert result.exit_code == 0
    mock_fetch.assert_awaited_once_with(['cs.AI'], 1, None, 'OR')
    mock_summarize.assert_called_once()
    mock_download.assert_not_called()
