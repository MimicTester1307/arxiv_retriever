import requests
from typing import List, Dict
import xml.etree.ElementTree as ET  # TODO: explore way to parse XML more securely


def fetch_papers(categories: List[str], limit: int) -> List[Dict]:
    """Fetch papers from ArXiv API based on given categories and limit."""
    base_url = "http://export.arxiv.org/api/query?"
    query = f"search_query=cat:{'+OR+'.join(categories)}&sortBy=submittedDate&sortOrder=descending&max_results={limit}"

    response = requests.get(base_url + query)
    if response.status_code == 200:
        return parse_arxiv_response(response.text)
    else:
        raise Exception(f"Failed to fetch papers: HTTP {response.status_code}")


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
