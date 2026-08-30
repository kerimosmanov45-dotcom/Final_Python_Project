PAGE_SIZE = 10

BASE_QUERY = """
WITH film_genres AS (
    SELECT fc.film_id,
           GROUP_CONCAT(c.name ORDER BY c.name SEPARATOR ', ') AS genres
    FROM sakila.film_category AS fc
    JOIN sakila.category AS c ON c.category_id = fc.category_id
    GROUP BY fc.film_id
)
SELECT f.film_id,
       f.title,
       f.description,
       f.release_year,
       f.length,
       COALESCE(fg.genres, 'Unknown') AS genres
FROM sakila.film AS f
LEFT JOIN film_genres AS fg ON fg.film_id = f.film_id
"""


def title_search_query():
    return BASE_QUERY + """
WHERE LOWER(f.title) LIKE CONCAT('%', %(keyword)s, '%')
ORDER BY f.title
LIMIT %(limit)s OFFSET %(offset)s
"""


def title_count_query():
    return """
SELECT COUNT(*)
FROM sakila.film
WHERE LOWER(title) LIKE CONCAT('%', %(keyword)s, '%')
"""


def genre_year_search_query():
    return BASE_QUERY + """
WHERE f.release_year BETWEEN %(year_from)s AND %(year_to)s
  AND EXISTS (
      SELECT 1
      FROM sakila.film_category AS fc
      JOIN sakila.category AS c ON c.category_id = fc.category_id
      WHERE fc.film_id = f.film_id
        AND c.name = %(category)s
  )
ORDER BY f.title
LIMIT %(limit)s OFFSET %(offset)s
"""


def genre_year_count_query():
    return """
SELECT COUNT(*)
FROM sakila.film AS f
WHERE f.release_year BETWEEN %(year_from)s AND %(year_to)s
  AND EXISTS (
      SELECT 1
      FROM sakila.film_category AS fc
      JOIN sakila.category AS c ON c.category_id = fc.category_id
      WHERE fc.film_id = f.film_id
        AND c.name = %(category)s
  )
"""
