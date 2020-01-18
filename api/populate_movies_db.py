import sys
from db.DB import get_db_instance

if len(sys.argv) < 2:
    print("Add the path to movies data file as a program argument...")
else:
    db = get_db_instance()
    db.populate_movies_data(sys.argv[1], True)  # this will clear the DB before populating it
