from typing import List, Dict
import typer
from arxiv_retriever.rag.extractor import extract_essential_info


def extract_paper_metadata(papers: List[Dict]):
    """Extract metadata from papers in paper list."""
    for i, paper in enumerate(papers, 1):
        typer.echo(f"\n{i}. {paper['title']}")
        typer.echo(f"    Authors: {', '.join(paper['authors'])}")
        typer.echo(f"    Published: {paper['published']}")
        typer.echo(f"    Link: {paper['link']}")
        typer.echo(f"    Summary: {paper['summary'][:100]}...")  # truncate summary # TODO: possibly update to find index of first period character in summary then use for truncation. makes summary more complete.


def summarize_papers(papers: List[Dict]):
    """Summarize papers in paper list from their abstracts"""
    extracted_info = extract_essential_info(papers)
    for info in extracted_info:
        typer.echo(f"\n{info['title']}")
        typer.echo(f"Essential Information:\n{info['extracted_info']}")