import typer
from typing_extensions import Annotated
from arxiv_retriever.fetcher import fetch_papers, search_paper_by_title

app = typer.Typer(no_args_is_help=True)


@app.command()
def fetch(categories: Annotated[list[str], typer.Argument(help="ArXiv categories to fetch papers from")],
          limit: int = typer.Option(10, help="Maximum number of papers to fetch")
          ):
    """Fetch papers from arXiv using specified categories and limit results by specified limit."""
    typer.echo(f"Fetching up to {limit} papers from categories: {', '.join(categories)}...")
    try:
        papers = fetch_papers(categories, limit)
        for i, paper in enumerate(papers, 1):
            typer.echo(f"\n{i}. {paper['title']}")
            typer.echo(f"    Authors: {', '.join(paper['authors'])}")
            typer.echo(f"    Published: {paper['published']}")
            typer.echo(f"    Link: {paper['link']}")
            typer.echo(
                f"    Summary: {paper['summary'][:100]}...")  # truncate summary # TODO: possibly update to find index of first period character in summary then use for truncation. makes summary more complete.
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}", err=True)


@app.command()
def search(
        title: Annotated[str, typer.Argument(help="ArXiv title to search for")],
        limit: int = typer.Option(10, help="Maximum number of papers to search")
):
    """Search papers by title."""
    typer.echo(f"Searching for papers matching {title}...")

    try:
        papers = search_paper_by_title(title, limit)
        for i, paper in enumerate(papers, 1):  # TODO: extract this into helper function to eliminate duplicate
            typer.echo(f"\n{i}. {paper['title']}")
            typer.echo(f"    Authors: {', '.join(paper['authors'])}")
            typer.echo(f"    Published: {paper['published']}")
            typer.echo(f"    Link: {paper['link']}")
            typer.echo(f"    Summary: {paper['summary'][:100]}...")
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}", err=True)


if __name__ == "__main__":
    app()
