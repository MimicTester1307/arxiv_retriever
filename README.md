# Description
`arxiv_retriever` is a command-line tool designed to automatically retrieve the most recent computer science papers from
[arxiv.org](https://arxiv.org/) based on categories specified as command-line arguments. This tool is built using Python
and leverages the Typer library for the command-line interface and the Python ElementTree XML package for parsing XML 
responses from the arXiv API.

# Features
- Fetches the most recent papers from ArXiv by specified categories
- Fetches papers from ArXiv by title
- Displays paper details including title, authors, publication date, and link to paper's page
- Easy-to-use command-line interface built with Typer
- Configurable number of results to fetch

# Installation
1. Clone the repository:
   ```shell
   git clone https://github.com/MimicTester1307/arxiv_retriever.git
   cd arxiv_retriever  
   ```
2. Install the package and dependencies
   ```shell
   pip install .
   ```

# Usage
To retrieve the most recent computer science papers by categories, use the `fetch` command followed by the categories and 
options:
   ```shell
   arxiv_retriever fetch <categories> [--limit]
   ```
*Outputs `limit` papers sorted by `submittedDate` in descending order*

To retrieve `limit` papers matching a specified title, use the `search` command followed by a title and options:
   ```shell
   arxiv_retriever search <title> [--limit]
   ```
*Outputs `limit` papers sorted by `relevance` in descending order*


## Example
Fetch the latest 5 papers in the cs.AI and cs.GL:
   ```shell
   arxiv_retriever fetch cs.AI cs.GL --limit 5
   ```

Fetch papers matching the title, "Attention is all you need":
   ```shell
   arxiv_retriever search "Attention is all you need" --limit 5
   ```

# Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any features, bug fixes, or
enhancements.

# License
This project is licensed under the MIT license. See the LICENSE file for more details.

# Acknowledgements
- [Typer](https://typer.tiangolo.com/) for the command-line interface
- [ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html) for XML parsing
- [arXiv API](https://info.arxiv.org/help/api/basics.html) for providing access to paper metadata
- [Notion](https://clover-gymnast-aeb.notion.site/ArXiv-Retriever-630d06d96edf4bfea17248cc890c021e?pvs=4) for helping me track and document my progress and learning.
