import requests
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET  # TODO: explore way to parse XML data more securely
import urllib.parse
import time

WAIT_TIME = 3  # number of seconds to wait between calls


def rate_limited_get(url: str) -> requests.Response:
    """Make a GET request with rate limiting."""
    response = requests.get(url)
    time.sleep(WAIT_TIME)
    return response


def fetch_papers(categories: List[str], limit: int, authors: Optional[List[str]] = None) -> List[Dict]:
    """
    Fetch papers from ArXiv using given categories and limit, with optional author filter.

    :param categories: List of ArXiv categories to search
    :param limit: Total number of results to fetch
    :param authors: Optional list of author names to filter results by
    :return: List of dictionaries containing paper information
    """
    base_url = "http://export.arxiv.org/api/query?"
    papers = []
    start = 0  # index of the first returned result
    max_results_per_query = 100

    category_query = '+OR+'.join(f'cat:{cat}' for cat in categories)
    author_query = '+AND+(' + '+OR+'.join(f'au:"{urllib.parse.quote_plus(author)}"' for author in authors) + ')' if authors else ''

    while start < limit:
        query = f"search_query={category_query}{author_query}&sortBy=submittedDate&sortOrder=descending&start={start}&max_results={max_results_per_query}"
        response = rate_limited_get(base_url + query)

        if response.status_code == 200:
            papers.extend(parse_arxiv_response(response.text))
            start += max_results_per_query
        else:
            raise Exception(f"Failed to fetch papers: HTTP {response.status_code}")

    return papers[:limit]  # Trim to the requested number of results


# TODO: add optional author parameter to refine title search by author
def search_paper_by_title(title: str, limit: int, authors: Optional[List[str]] = None) -> List[Dict]:
    """
    Search for papers on ArXiv using title, optionally filtered by author and return `limit` papers.

    :param title: Title of paper to search for
    :param limit: Total number of results to fetch
    :param authors: Optional list of author names to filter results by
    :return: List of dictionaries containing paper information
    """
    base_url = "http://export.arxiv.org/api/query?"
    encoded_title = urllib.parse.quote_plus(title)
    papers = []
    start = 0
    max_results_per_query = 100

    title_query = f'ti:"{encoded_title}"'
    author_query = '+AND+(' + '+OR+'.join(f'au:"{urllib.parse.quote_plus(author)}"' for author in authors) + ')' if authors else ''

    while start < limit:
        query = f"search_query={title_query}{author_query}&sortBy=relevance&sortOrder=descending&start={start}&max_results={max_results_per_query}" if authors else f"search_query={title_query}&sortBy=relevance&sortOrder=descending&start={start}&max_results={max_results_per_query}"
        response = rate_limited_get(base_url + query)

        if response.status_code == 200:
            papers.extend(parse_arxiv_response(response.text))
            start += max_results_per_query
        else:
            raise Exception(f"Failed to search papers: HTTP {response.status_code}")

    return papers[:limit]


def parse_arxiv_response(xml_data: str) -> List[Dict]:
    """
    Parse arXiv XML response and return paper information
    :param xml_data: XML response from arXiv API
    :return: List of dictionaries containing paper information
    """
    root = ET.fromstring(xml_data)
    namespace = {'atom': 'http://www.w3.org/2005/Atom'}

    papers = []
    for entry in root.findall('atom:entry', namespace):
        paper = {
            'title': entry.find('atom:title', namespace).text.strip(),
            'authors': [author.find('atom:name', namespace).text for author in entry.findall('atom:author', namespace)],
            'summary': entry.find('atom:summary', namespace).text.strip(),
            'published': entry.find('atom:published', namespace).text.strip(),
            'link': entry.find('atom:id', namespace).text.strip()
        }
        papers.append(paper)

    return papers
