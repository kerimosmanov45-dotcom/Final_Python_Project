import mysql.connector

from functions import (
    search_by_genre_and_year,
    search_by_title,
    show_top_5_searches,
)
from local_settings import dbconfig
from templates import GOODBYE_TEXT, MAIN_MENU


def main():
    """Run the console application."""
    try:
        with mysql.connector.connect(**dbconfig) as connection:
            while True:
                choice = input(MAIN_MENU).strip().lower()

                if choice == "1":
                    search_by_title(connection)
                elif choice == "2":
                    search_by_genre_and_year(connection)
                elif choice == "3":
                    show_top_5_searches()
                elif choice == "q":
                    print(GOODBYE_TEXT)
                    break
                else:
                    print("Please choose 1, 2, 3, or q.")
    except mysql.connector.Error as error:
        print(f"MySQL connection error: {error}")


if __name__ == "__main__":
    main()