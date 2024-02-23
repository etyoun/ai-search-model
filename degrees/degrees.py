import csv
import sys

from util import Node, StackFrontier, QueueFrontier

from tqdm.auto import tqdm


# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, starts (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }

            name_key = row["name"].lower()
            id_value = row["id"]

            if name_key in names:
                names[name_key].add(id_value)
            else:
                names[name_key] = {id_value}

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def person_id_for_name(name):
    """
    Return the person_id for a given name.
    """
    # Get the person
    person_ids = [names.get(name.lower())]

    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Multiple people with name '{name}'. Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")

        try:
            perdon_id = input("Intended person ID: ")
            if perdon_id in person_ids:
                return perdon_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "small"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Enter name: "))


if __name__ == "__main__":
    main()
