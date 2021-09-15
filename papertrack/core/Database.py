
import io
import os 
from collections import namedtuple
import json 

DatabaseEntry = namedtuple("DatabaseEntry", [
    "title",
    "authors",
    "publicationYear",
    "path",
    "url",
    "status",
    "field", 
    "category"
])

class Database:
    def __init__(self, location = os.path.join(os.environ["HOME"], ".papertrack/metadata.json")):
        self.location = location
    
    def save(self, entry: DatabaseEntry):
        os.makedirs(os.path.dirname(self.location), exist_ok=True)
        with open(self.location, "w") as f:
            try:
                data = json.loads(f.read())
            except io.UnsupportedOperation:
                data = []
            finally:
                data.append(dict(
                    title = entry.title,
                    authors = entry.authors,
                    publicationYear = entry.publicationYear,
                    path = entry.path,
                    url = entry.url,
                    status = entry.status,
                    field = entry.field,
                    category = entry.category
                ))
                f.write(json.dumps(data))