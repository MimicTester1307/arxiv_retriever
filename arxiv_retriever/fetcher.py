import requests
from typing import List, Dict
import xml.etree.ElementTree as ET  # TODO: explore way to parse XML data more securely
import urllib.parse
import time

WAIT_TIME = 3  # number of seconds to wait between calls


def rate_limited_get(url: str) -> requests.Response:
    """Make a GET request with rate limiting."""
    response = requests.get(url)
    time.sleep(WAIT_TIME)
    return response


def fetch_papers(categories: List[str], total_results: int) -> List[Dict]:
    """Fetch papers from ArXiv API based on given categories and limit with pagination."""
    base_url = "http://export.arxiv.org/api/query?"
    papers = []
    start = 0  # index of the first returned result
    max_results_per_query = 100

    while start < total_results:
        query = f"search_query=cat:{'+OR+'.join(categories)}&sortBy=submittedDate&sortOrder=descending&start={start}&max_results={max_results_per_query}"
        response = rate_limited_get(base_url + query)

        if response.status_code == 200:
            papers.extend(parse_arxiv_response(response.text))
            start += max_results_per_query
        else:
            raise Exception(f"Failed to fetch papers: HTTP {response.status_code}")

    return papers[:total_results]  # Trim to the requested number of results


# TODO: add optional author parameter to refine title search by author
def search_paper_by_title(title: str, total_results: int) -> List[Dict]:
    """Fetch papers from ArXiv API based on given title with pagination."""
    base_url = "http://export.arxiv.org/api/query?"
    encoded_title = urllib.parse.quote_plus(title)
    papers = []
    start = 0
    max_results_per_query = 100

    while start < total_results:
        query = f"search_query=ti:{encoded_title}&sortBy=relevance&sortOrder=descending&start={start}&max_results={max_results_per_query}"
        response = rate_limited_get(base_url + query)

        if response.status_code == 200:
            papers.extend(parse_arxiv_response(response.text))
            start += max_results_per_query
        else:
            raise Exception(f"Failed to search papers: HTTP {response.status_code}")

    return papers[:total_results]


def parse_arxiv_response(xml_data: str) -> List[Dict]:
    """Parse arXiv XML response and extract paper information."""
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
