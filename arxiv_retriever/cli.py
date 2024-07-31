from typing import List
from typing_extensions import Annotated

import typer
import trio

from arxiv_retriever.utils import process_papers
from arxiv_retriever.fetcher import fetch_papers, search_paper_by_title, download_from_links

app = typer.Typer(no_args_is_help=True)


@app.command()
def fetch(categories: Annotated[List[str], typer.Argument(help="ArXiv categories to fetch papers from")],
          limit: int = typer.Option(10, help="Maximum number of papers to fetch"),
          authors: Annotated[List[str], typer.Option(help="Author(s) to refine paper fetching by")] = None,
          ):
    """
    Fetch `limit` papers from ArXiv based on categories and optional authors.

    :param categories: List of ArXiv categories to search
    :param limit: Total number of results to fetch
    :param authors: Optional list of author names to filter results by
    :return: None
    """
    typer.echo(f"Fetching up to {limit} papers from categories: {', '.join(categories)} filtered by authors: {', '.join(authors) if authors else ''}...")
    try:
        async def run():
            papers = await fetch_papers(categories, limit, authors)
            await process_papers(papers)

        trio.run(run)
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}", err=True)


@app.command()
def search(
        title: Annotated[str, typer.Argument(help="ArXiv title to search for")],
        limit: int = typer.Option(10, help="Maximum number of papers to search"),
        authors: Annotated[List[str], typer.Option(help="Author(s) to refine paper title search by")] = None,
):
    """
    Search for papers on ArXiv using title, optionally filtered by author and return `limit` papers.
    :param title: Title of paper to search for
    :param limit: Total number of results to fetch
    :param authors: Optional list of author names to filter results by
    :return: None
    """
    typer.echo(f"Searching for papers matching {title}, filtered by authors: {', '.join(authors) if authors else ''}...")

    try:
        async def run():
            papers = await search_paper_by_title(title, limit, authors)
            await process_papers(papers)

        trio.run(run)
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}", err=True)


@app.command()
async def download(
        links: Annotated[List[str], typer.Argument(help="ArXiv links to download")],
        download_dir: str = typer.Option("./axiv_downloads", help="Directory to download papers"),
):
    """
    Download papers from ArXiv using their links (PDF or abstract links).

    :param links: ArXiv links to download from
    :param download_dir: Directory to download papers
    :return: None
    """
    typer.echo(f"Downloading papers from provided links...")

    try:
        trio.run(download_from_links, links, download_dir)
        typer.echo(f"Download complete. Papers saved to {download_dir}")
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}", err=True)


def main():
    """Entry point for arxiv_retriever"""
    app()


if __name__ == "__main__":
    main()
