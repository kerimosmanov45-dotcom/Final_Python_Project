MAIN_MENU = """
========================================
          SAKILA MOVIE FINDER
========================================
1. Search movies by title
2. Search movies by genre and year
3. Show top 5 popular searches
4. Show top 5 last uniq searches
q. Quit
----------------------------------------
Choose an option: """

FILM_HEADERS = ["#", "Title", "Description", "Year", "Length", "Genres"]
CATEGORY_HEADERS = ["ID", "Genre"]

CATEGORIES_QUERY = """
SELECT c.category_id, c.name
FROM sakila.category AS c
ORDER BY c.category_id
"""

YEAR_RANGE_QUERY = """
SELECT MIN(release_year), MAX(release_year)
FROM sakila.film
"""

GOODBYE_TEXT = "Thank you for using Sakila Movie Finder!"
