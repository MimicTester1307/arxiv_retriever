from typing import List
import sys
import os
from importlib.metadata import version as vsn
from typing_extensions import Annotated

import httpx
import typer
import trio

from arxiv_retriever.utils import process_papers
from arxiv_retriever.fetcher import fetch_papers, search_paper_by_title, download_from_links

app = typer.Typer(no_args_is_help=True)


@app.command()
def fetch(categories: Annotated[List[str], typer.Argument(help="ArXiv categories to fetch papers from")],
          limit: int = typer.Option(10, help="Maximum number of papers to fetch"),
          authors: Annotated[List[str], typer.Option("--author", "-a", help="Author(s) to refine paper fetching by. "
                                                                            "Can be used multiple times.")] = None,
          author_logic: str = typer.Option("OR", "--author-logic", "-l", help="Logic to use for multiple authors: "
                                                                              "'AND' or 'OR'")
          ):
    """
    Fetch papers from ArXiv based on categories, refined by options.

    :param categories: List of ArXiv categories to search
    :param limit: Total number of results to fetch
    :param authors: Optional list of author names to filter results by
    :param author_logic: Logic to use for multiple authors ('AND' or 'OR', default is 'OR')
    :return: None
    """
    author_logic = author_logic.upper()
    if author_logic not in ['AND', 'OR']:
        typer.echo(f"Invalid author_logic: {author_logic}. Using default 'OR' logic.")
        author_logic = 'OR'

    typer.echo(f"Fetching up to {limit} papers from categories: {', '.join(categories)}")
    if authors:
        typer.echo(f"Filtered by authors: {', '.join(authors)} (using '{author_logic}' logic)...")

    try:
        papers = trio.run(fetch_papers, categories, limit, authors, author_logic)
        trio.run(process_papers, papers)
    except httpx.HTTPError as e:
        typer.echo(f"HTTP error occurred: {str(e)}", err=True)
    except trio.TooSlowError:
        typer.echo(f"Operation timed out. please try again later.", err=True)
    except KeyboardInterrupt:
        typer.echo("Operation cancelled by user.", err=True)
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}", err=True)
        raise


@app.command()
def search(
        title: Annotated[str, typer.Argument(help="ArXiv title to search for")],
        limit: int = typer.Option(10, help="Maximum number of papers to search"),
        authors: Annotated[List[str], typer.Option("--author", "-a", help="Author(s) to refine paper title search "
                                                                          "by. Can be used multiple times.")] = None,
        author_logic: str = typer.Option("OR", "--author-logic", "-l", help="Logic to use for multiple authors: "
                                                                            "'AND' or 'OR'")
):
    """
    Search for papers on ArXiv using title, refined by options.

    :param title: Title of paper to search for
    :param limit: Total number of results to fetch
    :param authors: Optional list of author names to filter results by
    :param author_logic: Logic to use for multiple authors ('AND' or 'OR', default is 'OR')
    :return: None
    """
    author_logic = author_logic.upper()
    if author_logic not in ['AND', 'OR']:
        typer.echo(f"Invalid author_logic: {author_logic}. Using default 'OR' logic.")
        author_logic = 'OR'

    typer.echo(f"Searching for papers matching {title}")
    if authors:
        typer.echo(f"Filtered by authors: {', '.join(authors)} (using '{author_logic}' logic)...")

    try:

        papers = trio.run(search_paper_by_title, title, limit, authors, author_logic)
        trio.run(process_papers, papers)
    except httpx.HTTPError as e:
        typer.echo(f"HTTP error occurred: {str(e)}", err=True)
    except trio.TooSlowError:
        typer.echo(f"Operation timed out. please try again later.", err=True)
    except KeyboardInterrupt:
        typer.echo("Operation cancelled by user.", err=True)
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}", err=True)
        raise


@app.command()
def download(
        links: Annotated[List[str], typer.Argument(help="ArXiv links to download")],
        download_dir: str = typer.Option("./arxiv_downloads", "--download-dir", "-d", help="Directory to download papers"),
):
    """
    Download papers from ArXiv using their links (PDF or abstract links).

    :param links: ArXiv links to download from
    :param download_dir: Directory to download papers
    :return: None
    """
    download_dir = typer.prompt(f"Enter download directory: ", default=download_dir)
    download_dir = os.path.expanduser(download_dir)  # expand user directory if used

    typer.echo(f"Downloading papers from provided links...")
    try:
        trio.run(download_from_links, links, download_dir)
        typer.echo(f"Download complete. Papers saved to {download_dir}")
    except httpx.HTTPError as e:
        typer.echo(f"HTTP error occurred: {str(e)}", err=True)
    except trio.TooSlowError:
        typer.echo(f"Operation timed out. please try again later.", err=True)
    except KeyboardInterrupt:
        typer.echo("Operation cancelled by user.", err=True)
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}", err=True)
        raise


@app.command()
def version():
    """
    Display version information for arxiv_retriever and core dependencies.

    :return: None
    """
    arxiv_retriever_version = vsn("arxiv_retriever")
    typer.echo(f"arxiv_retriever version: {arxiv_retriever_version}\n")
    typer.echo(f"[Core Dependencies]")
    typer.echo(f"Python version: {sys.version_info.major}.{sys.version_info.minor}")
    typer.echo(f"Typer version: {vsn('typer')}")
    typer.echo(f"Httpx version: {vsn('httpx')}")
    typer.echo(f"Trio version: {vsn('trio')}")


def main():
    """Entry point for arxiv_retriever"""
    app()


if __name__ == "__main__":
    main()
