import typer
from typing_extensions import Annotated
from arxiv_retriever.fetcher import fetch_papers, search_paper_by_title
from arxiv_retriever.utils import extract_paper_metadata
from rag.extractor import extract_essential_info

app = typer.Typer(no_args_is_help=True)


@app.command()
def fetch(categories: Annotated[list[str], typer.Argument(help="ArXiv categories to fetch papers from")],
          limit: int = typer.Option(10, help="Maximum number of papers to fetch")
          ):
    """Fetch papers from arXiv using specified categories and limit results by specified limit."""
    typer.echo(f"Fetching up to {limit} papers from categories: {', '.join(categories)}...")
    try:
        papers = fetch_papers(categories, limit)
        extract_paper_metadata(papers)

        if typer.confirm("\nWould you like to extract essential information from these papers?"):
            extracted_info = extract_essential_info(papers)
            for info in extracted_info:
                typer.echo(f"\n{info['title']}")
                typer.echo(f"Essential Information:\n{info['extracted_info']}")
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
        extract_paper_metadata(papers)

        if typer.confirm("\nWould you like to extract essential information from these papers?"):
            extracted_info = extract_essential_info(papers)
            for info in extracted_info:
                typer.echo(f"\n{info['title']}")
                typer.echo(f"Essential Information:\n{info['extracted_info']}")
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}", err=True)


if __name__ == "__main__":
    app()
