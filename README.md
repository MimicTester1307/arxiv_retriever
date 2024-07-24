# Description
`arxiv_retriever` is a lightweight command-line tool designed to automate the retrieval of computer science papers from
[ArXiv](https://arxiv.org/). The retrieval can be done using specified ArXiv computer science archive categories or 
using the full or partial title of a specific paper, if available. Paper retrieval can be refined by author.

This tool is built using Python and leverages the Typer library for the command-line interface and the Python ElementTree
XML package for parsing XML responses from the arXiv API. It can be useful for researchers, engineers, or students who
want to quickly retrieve an ArXiv paper or keep abreast of latest research in their field without leaving their
terminal/workstation.

Although my current focus while building `arxiv_retriever` is the computer science archive, it can be easily 
used with categories from other areas on arxiv, e.g., `math.CO`.

# Features [more coming soon--see Notion page below for more info]
- Fetches the most recent papers from ArXiv by specified categories
- Fetches papers from ArXiv by title
- Refine fetch and search by author for more precise results
- Displays paper details including title, authors, publication date, and link to paper's page
- Easy-to-use command-line interface built with Typer
- Configurable number of results to fetch
- Built using only the standard library and tried and tested packages.

# Environment Setup
This program requires an environment variable (an OpenAI API key) to be set before running. This is used to authenticate
with OpenAI for the paper summarization feature.

## Required Environment Variable
- **Variable Name**: `OPENAI_API_KEY`

## Setting the Environment Variable

### On Unix-like systems (Linux, macOS)
In your terminal, run:
```shell
export OPENAI_API_KEY=<key>
```
To ensure this works across all shell instances, add the above line to your shell configuration file
(e.g., `~/.bashrc`, `~/.zshrc`, or `~/.profile`).

### On Windows
1. Open the Start menu and search for "Environment Variables"
2. Click on the "Edit system environment variables" option.
3. In the System Properties window, click on the "Environment Variables" button
4. Under "User variables", click "New"
5. Set the variable name as `OPENAI_API_KEY` and the value as your API key.

## Verifying the Environment Variable

To verify the environment variable is set correctly:

- On Unix-like systems:
  ```shell
    echo $OPENAI_API_KEY
    ```
- On Windows (command prompt):
  ```
  echo %OPENAI_API_KEY%
  ```
**Note**: Keep your API key confidential and do not share it publicly.

# Installation

## Install  from PyPI (Recommended):

```shell
pip install --upgrade arxiv-retriever
```

## Install from Source Distribution

If you need a specific version or want to install from a source distribution:

1. Download the source distribution (.tar.gz file) from PyPI or the GitHub releases page.

2. Install using pip:
   ```bash
   pip install axiv-x.y.z.tar.gz
   ```
   Replace `x.y.z` with the version number.

This method can be useful if you need a specific version or are in an environment without direct access to PyPI.

## Install for Development and Testing

To install the latest development version from source:
1. Ensure you have Poetry installed. If not, install it by following the instructions at [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation).
2. Clone the repository:
    ```shell
    git clone https://github.com/MimicTester1307/arxiv_retriever.git
    cd arxiv_retriever  
    ```
3. Install the project and its dependencies:
    ```shell
    poetry install
    ```
4. (Optional) To activate the virtual environment created by Poetry:
    ```shell
    poetry shell
    ```
5. (Optional) Run tests to ensure everything is set up correctly:
    ```shell
    poetry run pytest
    ```
6. Build the project:
    ```shell
    poetry build
    ```
7. Install the wheel file using pip:
    ```shell
    pip install dist/arxiv_retriever-1.0.0-py3-none-any.whl
    ```

# Usage

After installation, use the package via the `axiv` command:

To view available commands:
```shell
axiv --help
```

To view arguments and options for available commands:
```shell
axiv <command> --help
```

## Sample Usage

To retrieve the most recent computer science papers by categories, use the `fetch` command followed by the categories and 
options:
   ```shell
   axiv fetch <categories> [--limit]
   ```
*Outputs `limit` papers sorted by `submittedDate` in descending order*

To filter results by author(s):
```shell
  axiv fetch <categories> [--limit] [--authors]
```
*Outputs `limit` papers sorted by `submittedDate` in descending order, filtered by `authors`*


To retrieve `limit` papers matching a specified title, use the `search` command followed by a title and options:
   ```shell
   axiv search <title> [--limit]
   ```
*Outputs `limit` papers sorted by `relevance` in descending order*

To filter results by author(s):
```shell
  axiv search <title> [--limit] [--authors]
```
*Outputs `limit` papers sorted by `relevance` in descending order, filtered by authors*


## Examples
Fetch the latest 5 papers in the cs.AI and cs.GL:
   ```shell
   axiv fetch cs.AI cs.GL --limit 5
   ```

Fetch papers matching the title, "Attention is all you need":
   ```shell
   axiv search "Attention is all you need" --limit 5 --authors "Ashish"
   ```

# Note on Package and Command Names

- **Package Name**: The package is named `arxiv_retriever`. This is the name you use when installing via pip or referring to the project.
- **Command Name**: After installation, you interact with the tool using the `axiv` command in your terminal.

This distinction allows for a more concise command while maintaining a descriptive package name.

# Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any features, bug fixes, or
enhancements.

# License
This project is licensed under the MIT license. See the LICENSE file for more details.

# Acknowledgements
- [Typer](https://typer.tiangolo.com/) for the command-line interface
- [ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html) for XML parsing
- [arXiv API](https://info.arxiv.org/help/api/basics.html) for providing access to paper metadata
- [Notion](https://clover-gymnast-aeb.notion.site/ArXiv-Retriever-630d06d96edf4bfea17248cc890c021e?pvs=4) for helping me 
  track my progress and document my learning.
