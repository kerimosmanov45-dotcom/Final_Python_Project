from datetime import datetime

from formatter import format_movies, print_table
from mongo_connector import get_top_5_searches, save_search
from requests import (
    PAGE_SIZE,
    genre_year_count_query,
    genre_year_search_query,
    title_count_query,
    title_search_query,
)
from templates import (
    CATEGORIES_QUERY,
    CATEGORY_HEADERS,
    FILM_HEADERS,
    YEAR_RANGE_QUERY,
)


def _fetch_one_value(cursor, query, params=None):
    cursor.execute(query, params or {})
    return cursor.fetchone()[0]


def _show_pages(cursor, query, params, total_results):
    """Display search results 10 at a time."""
    offset = 0

    while offset < total_results:
        page_params = {**params, "limit": PAGE_SIZE, "offset": offset}
        cursor.execute(query, page_params)
        rows = cursor.fetchall()

        numbered_rows = []
        for index, row in enumerate(rows, start=offset + 1):
            numbered_rows.append((index, *row[1:]))

        print_table(format_movies(numbered_rows), FILM_HEADERS)
        shown = min(offset + PAGE_SIZE, total_results)
        print(f"Showing {offset + 1}-{shown} of {total_results} movies.")

        offset += PAGE_SIZE
        if offset >= total_results:
            break

        choice = input("Show the next 10 results? (y/n): ").strip().lower()
        if choice != "y":
            break


def search_by_title(connection):
    """Search Sakila movies by a word or part of the title."""
    keyword = input("Enter a movie title or keyword: ").strip().lower()
    if not keyword:
        print("Please enter a keyword.")
        return

    params = {"keyword": keyword}
    cursor = connection.cursor()
    try:
        total = _fetch_one_value(cursor, title_count_query(), params)
        save_search(
            {
                "timestamp": datetime.now(),
                "search_type": "keyword",
                "params": {"keyword": keyword},
                "results_count": total,
            }
        )

        print(f"\nFound {total} movie(s).")
        if total:
            _show_pages(cursor, title_search_query(), params, total)
    finally:
        cursor.close()


def _load_categories_and_years(cursor):
    cursor.execute(CATEGORIES_QUERY)
    categories = cursor.fetchall()

    cursor.execute(YEAR_RANGE_QUERY)
    min_year, max_year = cursor.fetchone()
    return categories, min_year, max_year


def _read_year(prompt, min_year, max_year):
    while True:
        try:
            year = int(input(prompt))
        except ValueError:
            print("Please enter a valid year.")
            continue

        if min_year <= year <= max_year:
            return year
        print(f"Year must be between {min_year} and {max_year}.")


def search_by_genre_and_year(connection):
    """Search movies by genre and a release-year range."""
    cursor = connection.cursor()
    try:
        categories, min_year, max_year = _load_categories_and_years(cursor)

        print("\nAvailable genres:")
        print_table(categories, CATEGORY_HEADERS)
        print(f"Available release years: {min_year}-{max_year}")

        category_map = {category_id: name for category_id, name in categories}
        while True:
            try:
                category_id = int(input("Enter genre ID: "))
            except ValueError:
                print("Please enter a number.")
                continue

            if category_id in category_map:
                break
            print("That genre ID does not exist.")

        year_from = _read_year("From year: ", min_year, max_year)
        year_to = _read_year(
            "To year (use the same year for an exact year): ", min_year, max_year
        )
        if year_from > year_to:
            year_from, year_to = year_to, year_from

        category = category_map[category_id]
        params = {
            "category": category,
            "year_from": year_from,
            "year_to": year_to,
        }
        total = _fetch_one_value(cursor, genre_year_count_query(), params)

        log_params = {"category": category}
        if year_from == year_to:
            log_params["year"] = year_from
        else:
            log_params["year_from"] = year_from
            log_params["year_to"] = year_to

        save_search(
            {
                "timestamp": datetime.now(),
                "search_type": "genre_year",
                "params": log_params,
                "results_count": total,
            }
        )

        print(f"\nFound {total} movie(s).")
        if total:
            _show_pages(cursor, genre_year_search_query(), params, total)
    finally:
        cursor.close()


def show_top_5_searches():
    """Print the five most popular search requests from MongoDB."""
    documents = get_top_5_searches()
    if not documents:
        print("No search history yet.")
        return

    rows = []
    for index, document in enumerate(documents, start=1):
        search = document["_id"]
        rows.append(
            [
                index,
                search["search_type"],
                str(search["params"]),
                document["count"],
            ]
        )

    print("\nTop 5 popular searches:")
    print_table(rows, ["#", "Search type", "Parameters", "Count"])
