import textwrap

from tabulate import tabulate


def print_table(rows, headers):
    """Print rows as a simple console table."""
    if not rows:
        return
    print(tabulate(rows, headers=headers, tablefmt="rounded_grid"))


def format_movies(rows):
    """Wrap long movie descriptions so the table stays readable."""
    formatted = []
    for row in rows:
        number, title, description, year, length, genres = row
        formatted.append(
            (
                number,
                title,
                textwrap.fill(description or "", width=42),
                year,
                length,
                genres,
            )
        )
    return formatted
