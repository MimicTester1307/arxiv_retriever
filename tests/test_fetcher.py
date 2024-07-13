import urllib.parse
from typing import List, Dict

from arxiv_retriever.fetcher import fetch_papers, search_paper_by_title, parse_arxiv_response

from pytest_mock import MockerFixture
import pytest


@pytest.fixture
def mock_requests(mocker: MockerFixture):
    return mocker.patch('arxiv_retriever.fetcher.requests.get')


@pytest.fixture
def mock_parse_arxiv_response(mocker: MockerFixture):
    return mocker.patch('arxiv_retriever.fetcher.parse_arxiv_response')


def test_parse_arxiv_response():
    """Test parse_arxiv_response function."""
    # mock xml data gotten & modified from section 4.1 of https://info.arxiv.org/help/api/user-manual.html
    mock_xml = """
    <feed xmlns="http://www.w3.org/2005/Atom" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/" xmlns:arxiv="http://arxiv.org/schemas/atom">
      <link xmlns="http://www.w3.org/2005/Atom" href="http://arxiv.org/api/query?search_query=all:electron&amp;id_list=&amp;start=0&amp;max_results=1" rel="self" type="application/atom+xml"/>
      <title xmlns="http://www.w3.org/2005/Atom">ArXiv Query: search_query=all:electron&amp;id_list=&amp;start=0&amp;max_results=1</title>
      <updated xmlns="http://www.w3.org/2005/Atom">2007-10-08T00:00:00-04:00</updated>
      <opensearch:totalResults xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">1000</opensearch:totalResults>
      <entry xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
        <id xmlns="http://www.w3.org/2005/Atom">http://arxiv.org/abs/hep-ex/0307015</id>
        <published xmlns="http://www.w3.org/2005/Atom">2003-07-07T13:46:39-04:00</published>
        <title xmlns="http://www.w3.org/2005/Atom">Multi-Electron Production at High Transverse Momenta in ep Collisions at HERA</title>
        <summary xmlns="http://www.w3.org/2005/Atom">Test Summary</summary>
        <author xmlns="http://www.w3.org/2005/Atom">
          <name xmlns="http://www.w3.org/2005/Atom">H1 Collaboration</name>
        </author>
      </entry>
    </feed>
    """

    expected_result_features = ['title', 'authors', 'summary', 'published', 'link']
    result = parse_arxiv_response(mock_xml)
    assert len(result) == 1
    assert isinstance(result, List) and isinstance(result[0], Dict)  # returns expected type
    assert all(feature in result[0] for feature in expected_result_features)
    assert result[0]['title'] == 'Multi-Electron Production at High Transverse Momenta in ep Collisions at HERA'
    assert result[0]['authors'] == ['H1 Collaboration']
    assert result[0]['summary'] == 'Test Summary'
    assert result[0]['published'] == '2003-07-07T13:46:39-04:00'
    assert result[0]['link'] == 'http://arxiv.org/abs/hep-ex/0307015'


def test_fetch_papers_success(mock_requests, mock_parse_arxiv_response, mocker: MockerFixture):
    """Test fetch_papers function."""
    # Arrange
    categories = ['cs.AI', 'math.CO']
    limit = 5
    expected_url = ("http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+math.CO&sortBy=submittedDate"
                    "&sortOrder=descending&max_results=5")
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = '<fake_xml>Fake ArXiv response</fake_xml>'
    mock_requests.return_value = mock_response

    expected_parsed_result = [{'title': 'Test paper', 'authors': ['John Doe']}]
    mock_parse_arxiv_response.return_value = expected_parsed_result

    # Act
    result = fetch_papers(categories, limit)

    # Assert
    mock_requests.assert_called_once_with(expected_url)
    mock_parse_arxiv_response(mock_response.text)
    assert result == expected_parsed_result


def test_search_paper_by_title_success(mock_requests, mock_parse_arxiv_response, mocker: MockerFixture):
    # Arrange
    title = "Attention Is All You Need"
    limit = 5
    encoded_title = urllib.parse.quote_plus(title)
    query = (f"http://export.arxiv.org/api/query?search_query=ti:{encoded_title}&sortBy=relevance&sortOrder=descending"
             f"&max_results={limit}")

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = '<fake_xml>Fake ArXiv response</fake_xml>'
    mock_requests.return_value = mock_response

    expected_parsed_result = [{'title': 'Attention Is All You Need', 'authors': ['John Doe']}]
    mock_parse_arxiv_response.return_value = expected_parsed_result

    # Act
    result = search_paper_by_title(title, limit)

    # Assert
    assert encoded_title == "Attention+Is+All+You+Need"
    assert query == (f"http://export.arxiv.org/api/query?search_query=ti:Attention+Is+All+You+Need&sortBy=relevance"
                     f"&sortOrder=descending&max_results=5")
    mock_requests.assert_called_once_with(query)
    mock_parse_arxiv_response.assert_called_once_with(mock_response.text)
    assert result == expected_parsed_result
