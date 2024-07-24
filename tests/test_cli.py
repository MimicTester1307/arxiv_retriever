from itertools import combinations
import pytest
from typer.testing import CliRunner
from arxiv_retriever.cli import app


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_fetch(mocker):
    return mocker.patch('arxiv_retriever.cli.fetch_papers')


@pytest.fixture
def mock_search(mocker):
    return mocker.patch('arxiv_retriever.cli.search_paper_by_title')


@pytest.fixture
def mock_extract_paper_metadata(mocker):
    return mocker.patch('arxiv_retriever.cli.extract_paper_metadata')


def test_fetch_command_success(runner, mock_fetch, mock_extract_paper_metadata, mocker):
    mock_fetch.return_value = [
        {
            'title': 'Test Paper',
            'authors': ['John Doe'],
            'published': '2024-07-05T12:00:00Z',
            'link': 'http://arxiv.org/abs/2407.0001',
            'summary': 'Test paper summary.'
        }
    ]
    mocker.patch('typer.confirm', return_value=False)  # mock the confirm to return False, i.e. no summarization
    result = runner.invoke(app, ["fetch", "cs.AI", "--limit", "1", "--authors", "John Doe"])
    assert result.exit_code == 0
    assert "Fetching up to 1 papers from categories: cs.AI filtered by authors: John Doe" in result.stdout
    mock_fetch.assert_called_once_with(["cs.AI"], 1, ["John Doe"])
    mock_extract_paper_metadata.assert_called_once_with(mock_fetch.return_value)


def test_search_command_success(runner, mock_search, mock_extract_paper_metadata, mocker):
    mock_search.return_value = [
        {
            'title': 'Search Paper Title',
            'authors': ['John Doe'],
            'published': '2024-07-05T12:00:00Z',
            'link': 'http://arxiv.org/abs/2407.0002',
            'summary': 'Search paper summary.'
        }
    ]
    mocker.patch('typer.confirm', return_value=False)  # mock the confirm to return False, i.e. no summarization
    result = runner.invoke(app, ["search", "search paper title", "--limit", "1", "--authors", "John Doe"])
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
    assert "John Doe" in result.stdout
    mock_search.assert_called_once_with("search paper title", 1, ["John Doe"])
    mock_extract_paper_metadata.assert_called_once_with(mock_search.return_value)
