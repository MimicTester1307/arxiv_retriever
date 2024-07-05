import requests
from typing import List, Dict


def fetch_papers(categories: List[str], limit: int) -> List[Dict]:
    """Fetch papers from ArXiv API based on given categories and limit."""
    base_url = "http://export.arxiv.org/api/query?"
    query = f"search_query=cat:{'+OR+'.join(categories)}&sortBy=submittedDate&sortOrder=descending&max_results={limit}"

    response = requests.get(base_url + query)
    if response.status_code == 200:
        # TODO: Parse XML response and extract paper information
        return []
    else:
        raise Exception(f"Failed to fetch papers: HTTP {response.status_code}")
