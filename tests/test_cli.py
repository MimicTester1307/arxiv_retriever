import sys
import inspect
from itertools import combinations
from collections import namedtuple
import pytest
from typer.testing import CliRunner
from arxiv_retriever.cli import app


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(autouse=True)
def mock_inspect_signature(mocker):
    original_signature = inspect.signature

    def patched_signature(func, *args, **kwargs):
        if 'eval_str' in kwargs:
            del kwargs['eval_str']
        return original_signature(func, *args, **kwargs)

    mocker.patch('inspect.signature', patched_signature)


@pytest.mark.asyncio
async def test_fetch_command_success(runner, mocker):
    mock_fetch = mocker.AsyncMock()
    mock_fetch.return_value = [
        {
            'title': 'Test Paper',
            'authors': ['John Doe'],
            'published': '2024-07-05T12:00:00Z',
            'abstract_link': 'http://arxiv.org/abs/2407.0001',
            'pdf_link': 'http://arxiv.org/pdf/2407.0001',
            'summary': 'Test paper summary.'
        }
    ]
    mocker.patch('arxiv_retriever.cli.fetch_papers', mock_fetch)

    mock_process = mocker.AsyncMock()
    mocker.patch('arxiv_retriever.cli.process_papers', mock_process)

    result = runner.invoke(app, ["fetch", "cs.AI", "--limit", "1", "--author", "John Doe"])

    assert result.exit_code == 0
    assert "Fetching up to 1 papers from categories: cs.AI" in result.stdout
    assert "Filtered by authors: John Doe (using 'OR' logic)..." in result.stdout
    mock_fetch.assert_called_once_with(["cs.AI"], 1, ["John Doe"], "OR")
    mock_process.assert_called_once()


@pytest.mark.asyncio
async def test_search_command_success(runner, mocker):
    mock_search = mocker.AsyncMock()
    mock_search.return_value = [
        {
            'title': 'Search Paper Title',
            'authors': ['John Doe'],
            'published': '2024-07-05T12:00:00Z',
            'abstract_link': 'http://arxiv.org/abs/2407.0002',
            'pdf_link': 'http://arxiv.org/pdf/2407.0002',
            'summary': 'Search paper summary.'
        }
    ]
    mocker.patch('arxiv_retriever.cli.search_paper_by_title', mock_search)
    mock_process = mocker.AsyncMock()
    mocker.patch('arxiv_retriever.cli.process_papers', mock_process)

    result = runner.invoke(app, ["search", "search paper title", "--limit", "1", "--author", "John Doe"])

    assert result.exit_code == 0
    # to create a more robust test based on output result, I will:
    # 1. split the test search query into a list
    # 2. create another list of all the possible combinations of the search query
    # 3. assert that at least one of the returned combination is in the returned result
    # I decided to take this route due to the results I was getting when
    # testing the search cli command with the query "Attention is all you need". Only one of the results returned the
    # accurate title, and it wasn't the first one. But all the results had some form of the query in them. So I basically
    # need to test that some combination of the user's search query (title) is in the title returned by the retriever
    # There's probably a better way to do this, though
    search_title_list = "search paper title".split()
    title_combinations = [' '.join(token) for i in range(len(search_title_list), 0, -1) for token in
                          combinations(search_title_list, i)]  # initial implementation was from beginning; realized
    # searching for combinations in reverse is best case
    assert any(comb.lower() in result.stdout.lower() for comb in title_combinations)  # main thing to check for
    assert "Searching for papers matching search paper title" in result.stdout
    assert "Filtered by authors: John Doe (using 'OR' logic)..." in result.stdout
    mock_search.assert_called_once_with("search paper title", 1, ["John Doe"], "OR")
    mock_process.assert_called_once()


@pytest.mark.asyncio
async def test_download_command_success(runner, mocker):
    mock_download_from_links = mocker.AsyncMock()
    mocker.patch('arxiv_retriever.cli.download_from_links', mock_download_from_links)

    result = runner.invoke(app, ["download", "http://arxiv.org/abs/2407.0001", "--download-dir", "./test_downloads"])

    assert result.exit_code == 0
    # assert "Downloading papers from links provided links..." in result.stdout
    mock_download_from_links.assert_awaited_once_with(["http://arxiv.org/abs/2407.0001"], "./test_downloads")
    assert "Download complete. Papers saved to ./test_downloads" in result.stdout


def test_version_command(runner, mocker, *args, **kwargs):
    mocker.patch('arxiv_retriever.cli.vsn', return_value="1.0.0")
    VersionInfo = namedtuple('version_info', 'major minor micro releaselevel serial')
    mock_version_info = VersionInfo(major=3, minor=8, micro=0, releaselevel='final', serial=0)
    mocker.patch('sys.version_info', mock_version_info)
    mocker.patch('typer.__version__', "1.0.0")
    mocker.patch('httpx.__version__', "1.0.0")
    mocker.patch('trio.__version__', "1.0.0")

    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0, f"Command failed with exit code {result.exit_code}. Output: {result.output}"
    assert "arxiv_retriever version: 1.0.0" in result.stdout
    assert "Python version: 3." in result.stdout
    assert "Typer version: 1.0.0" in result.stdout
    assert "Httpx version: 1.0.0" in result.stdout
    assert "Trio version: 1.0.0" in result.stdout
