import typer
from typing_extensions import Annotated

app = typer.Typer(no_args_is_help=True)


@app.command()
def fetch(categories: Annotated[list[str], typer.Argument(help="ArXiv categories to fetch papers from")],
          limit: int = typer.Option(10, help="Maximum number of papers to fetch")
          ):
    """Fetch papers from arXiv using specified categories and limit results by specified limit."""
    typer.echo(f"Fetching up to {limit} papers from categories: {', '.join(categories)}")
    # TODO: implement paper fetching logic

if __name__ == "__main__":
    app()