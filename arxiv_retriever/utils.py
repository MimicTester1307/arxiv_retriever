from typing import List, Dict
import typer


def extract_paper_metadata(papers: List[Dict]):
    for i, paper in enumerate(papers, 1):
        typer.echo(f"\n{i}. {paper['title']}")
        typer.echo(f"    Authors: {', '.join(paper['authors'])}")
        typer.echo(f"    Published: {paper['published']}")
        typer.echo(f"    Link: {paper['link']}")
        typer.echo(f"    Summary: {paper['summary'][:100]}...")  # truncate summary # TODO: possibly update to find index of first period character in summary then use for truncation. makes summary more complete.
