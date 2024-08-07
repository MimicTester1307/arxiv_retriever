# ArXiv Retriever

## Status: Maintenance Mode

**Note:** This project is currently in maintenance mode. While I am not actively developing new features, I will continue
to address critical issues and security vulnerabilities as time permits. Users are welcome to fork the repository if 
they wish to extend its functionality. Please refer to [Maintenance Policy](#maintenance-policy) for more information.

---

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Environment Setup](#environment-setup)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Maintenance Policy](#maintenance-policy)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Introduction
`arxiv_retriever` is a lightweight command-line tool designed to automate the retrieval of computer science papers from
[ArXiv](https://arxiv.org/). The retrieval can be done using specified ArXiv computer science archive categories, full or partial 
titles of papers, if available, or links to the papers. Paper retrieval can be refined by author.

**NOTE:** My tests indicate that when searching for a really long title, using the partial title and then refining by author
yields better results, as opposed to searching with the full title or even searching with the full title and refining by
author. However, the tests are not exhaustive.

This tool is built using Python and leverages the Typer library for the command-line interface and the Python ElementTree
XML package for parsing XML responses from the arXiv API. It can be useful for researchers, engineers, or students who
want to quickly retrieve an ArXiv paper or keep abreast of latest research in their field without leaving their
terminal/workstation.

Although my current focus while building `arxiv_retriever` is the computer science archive, it can be easily 
used with categories from other areas on arxiv, e.g., `math.CO`.

## Features
- Fetch the most recent papers specified ArXiv categories
- Search for papers on ArXiv using full or partial title
- Refine fetch and search by author (s) for more precise results
- Specify logic for combination of multiple authors ('AND' or 'OR') during retrieval
- Download papers after they are retrieved
- View paper details including title, authors, abstract, publication date, and links to paper's abstract and pdf pages
- Easy-to-use command-line interface built with Typer
- Configurable number of results to fetch
- Built using only the standard library and tried and tested packages.

## Environment Setup
You can optionally set an environment variable (an OpenAI API key) before using the program. This is used to authenticate
with OpenAI for the paper summarization feature. If you do not want your papers summarized, you will not need to set the
environment variable. Specify your choice when asked by the CLI. Specifying 'y' without the KEY set will lead to an error.

### Optional Environment Variable
- **Variable Name**: `OPENAI_API_KEY`

### Setting the Environment Variable

#### On Unix-like systems (Linux, macOS)
In your terminal, run:
```shell
export OPENAI_API_KEY=<key>
```
To ensure this works across all shell instances, add the above line to your shell configuration file
(e.g., `~/.bashrc`, `~/.zshrc`, or `~/.profile`).

#### On Windows
1. Open the Start menu and search for "Environment Variables"
2. Click on the "Edit system environment variables" option.
3. In the System Properties window, click on the "Environment Variables" button
4. Under "User variables", click "New"
5. Set the variable name as `OPENAI_API_KEY` and the value as your API key.

### Verifying the Environment Variable

To verify the environment variable is set correctly:

- On Unix-like systems:
    ```shell
    echo $OPENAI_API_KEY
    ```
- On Windows (command prompt):
  ```shell
  echo %OPENAI_API_KEY%
  ```
**NOTE:** Keep your API key confidential and do not share it publicly.

## Installation

### Install  from PyPI (Recommended):

```shell
pip install --upgrade arxiv-retriever
```

### Install from Source Distribution

If you need a specific version or want to install from a source distribution:

1. Download the source distribution (.tar.gz file) from PyPI or the GitHub releases page.

2. Install using pip:
   ```bash
   pip install axiv-x.y.z.tar.gz
   ```
   Replace `x.y.z` with the version number.

This method can be useful if you need a specific version or are in an environment without direct access to PyPI.

### Install for Development and Testing

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
    pip install dist/arxiv_retriever-<version>-py3-none-any.whl
    ```

## Usage

After installation, use the package via the `axiv` command. To view available commands: `axiv --help` or `axiv`

### Note on Package and Command Names

- **Package Name**: The package is named `arxiv_retriever`. This is the name you use when installing via pip or referring to the project.
- **Command Name**: After installation, you interact with the tool using the `axiv` command in your terminal.

This distinction allows for a more concise command while maintaining a descriptive package name.

### Basic Commands

- `fetch`: Fetch papers from ArXiv based on categories, refined by options.
- `search`: Search for papers on ArXiv using title, refined by options.
- `download`: Download papers from ArXiv using their links (PDF or abstract links).
- `version`: Display version information for arxiv_retriever and core dependencies.

### Sample Usage

#### Fetch
To retrieve the most recent computer science papers by categories, use the `fetch` command followed by the categories and 
options:
```shell
axiv fetch [OPTIONS] CATEGORIES...
```

#### Search
To search for a paper by title, use the `search` command followed by the title and options:
```shell 
axiv search [OPTIONS] TITLE
```

#### CLI Options
Due to how most CLI frameworks (including Typer) handle arguments vs options, if you want to specify multiple options (in this case, authors)
to refine your `search` or `fetch` command by, you will have to call the option multiple times. That is,
`--author <author> --author <author>` as opposed to `--author <author> <author>`. Alternatively, you can use `-a` rather
than `--author`

#### Downloading your research papers
There are multiple ways to download your research paper using `axiv`:
- use `axiv download [OPTIONS] LINKS...` to download the paper directly from the link
- confirm if you want to download the retrieved papers using `fetch` or `search` when asked by the CLI

With option 1, the file is named using the URL's basename, e.g. `2407.09298v1.pdf`.

With options 2, the file is named using the title retrieved from the XML data when parsing.

**NOTE:** If the file name exists, it is overwritten.


### Examples
Fetch the latest 5 papers in the cs.AI OR cs.GL categories:
```shell
axiv fetch cs.AI cs.GL --limit 5
```
*Outputs `limit` papers sorted by `submittedDate` in descending order, filtered by `authors`*

Refine fetch using multiple authors
```shell
axiv fetch cs.AI -a omar -a matei
```

Add logic for creating query when multiple authors are supplied using `--author-logic` or `-l`:
```shell
axiv fetch cs.AI math.CO -a "John Doe" -a "Jane Smith" --author-logic AND
```

Fetch papers matching the title, "Attention is all you need", refined by author "Ashish":
```shell
axiv search "Attention is all you need" --limit 5 --author "Ashish"
```

Download papers using links:

- download using link to abstract:
    ```shell
    axiv download https://arxiv.org/abs/2407.20214v1
    ```
- download using link to pdf:
    ```shell
    axiv download https://arxiv.org/pdf/2407.20214v1
    ```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any features, bug fixes, or
enhancements.

### Note on Testing

Currently, all 12 tests pass, but that required a bit of magic. Refactoring the tests for asynchrony was
an interesting challenge. Discussions and contributions regarding the asynchronous implementation are particularly
welcome.

Contact me via email or leave a comment on the [Notion project tracker](https://clover-gymnast-aeb.notion.site/ArXiv-Retriever-630d06d96edf4bfea17248cc890c021e?pvs=4).

## Maintenance Policy
This project is currently in maintenance mode. Here is what you can expect:
- Security vulnerabilities and bugs will be addressed as time permits.
- Pull requests for bug fixes will be considered. 
- Feature requested are unlikely to be implemented by the maintainer, but forks and extensions are encouraged.

For any questions, concerns, or comments, please open an issue in the GitHub repository.

## License
This project is licensed under the MIT license. See the LICENSE file for more details.

## Acknowledgements
- [Typer](https://typer.tiangolo.com/) for the command-line interface
- [ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html) for XML parsing
- [arXiv API](https://info.arxiv.org/help/api/basics.html) for providing access to paper metadata via a well-designed API
- [Trio](https://trio.readthedocs.io/en/stable/index.html) and [HTTPx](https://www.python-httpx.org/) for the asynchronous features
- [Dead Simple Python](https://www.amazon.de/-/en/Jason-C-McDonald/dp/1718500920) for helping me advance my knowledge of Python