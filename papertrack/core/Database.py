
import io
import os 
from collections import namedtuple
import json
from typing import List 

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
    
    def _read_metadata(self):
        os.makedirs(os.path.dirname(self.location), exist_ok=True)
        data = [] 
        try:
            f = open(self.location, "r")
            data = json.loads(f.read())
            f.close()
        except FileNotFoundError:
            data = []
        return data

    def _write_metadata(self,data):
        with open(self.location, "w") as f:
            f.write(json.dumps(data))
    def delete(self, path):
        self._write_metadata(list(e for e in self._read_metadata() if e["path"] != path))


    def save(self, entry: DatabaseEntry):
        data = self._read_metadata()
        entry_exists = False
        for i in range(0, len(data)):
            if entry.path == data[i]["path"]:
                entry_exists = True
                data[i] = dict(
                    title = entry.title,
                    authors = entry.authors,
                    publicationYear = entry.publicationYear,
                    path = entry.path,
                    url = entry.url,
                    status = entry.status,
                    field = entry.field,
                    category = entry.category    
                )
        if not entry_exists:
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
        self._write_metadata(data)
    def list(self) -> List[DatabaseEntry]:
        os.makedirs(os.path.dirname(self.location), exist_ok=True)
        try:
            with open(self.location) as f:
                try:
                    data = json.loads(f.read())
                except io.UnsupportedOperation:
                    data = []
                finally:
                    return list(DatabaseEntry(
                        title = x["title"],
                        authors = x["authors"],
                        publicationYear = x["publicationYear"],
                        path = x["path"],
                        url = x["url"],
                        status = x["status"],
                        field = x["field"],
                        category = x["category"]
                    ) for x in data)
        except FileNotFoundError:
            return []
    def verify_and_fix(self, journal_location):
        journal_data = [] 
        try:
            with open(journal_location) as f:
                journal_data = json.loads(f.read())
        except Exception as e:
            print("Error occured while reading journal data %s" % str(e))
        collected_entries = {}
        for entry in journal_data:
            if entry["operation"] == "collect" and "result" in entry.keys():
                e = eval(entry["result"])
                if e.path in collected_entries.keys():
                    print("WARNING: %s present multiple times in journal" % e.path)
                collected_entries[e.path] = e
        for entry in self.list():
            if not os.path.exists(entry.path):
                print("Path for entry %s does not exist anymore, delete entry? (y/n)" % str(entry))
                choice = input("> ")
                if choice == "y":
                    self.delete(entry.path)
            if entry != collected_entries.get(entry.path, entry):
                print("Entry: %s is not equal to what is found in journal, correct it (y/n)?" % str(entry))
                choice =  input("> ")
                if choice == "y":
                    entry = collected_entries.get(entry.path, entry)
                    self.save(entry)
        for collected_entry in collected_entries.values():
            if collected_entry.path not in list(e.path for e in self.list()):
                print("Entry %s not in database, add it? (y/n)" % str(collected_entry))
                choice = input("> ")
                if choice == "y":
                    self.save(collected_entry)
        downloads = list((d["object_data"]["url"], d["result"]) for d in journal_data if "result" in d and d["operation"] == "download")
        collections = list((d["data"]["location"], eval(d["result"])) for d in journal_data if "result" in d and d["operation"] == "collect")
        print("___________")
        print("these are steps to reproduce database manually from journal:")
        print()
        for url, location in downloads:
            for collected_location, collected_entry in collections:
                if location == collected_location:
                    authors = " ".join(list("--author %s" % author for author in collected_entry.authors))
                    command = f"""
papertrack get --downloader simple --collector simple \\
    --title "{collected_entry.title}" \\
    --year {collected_entry.publicationYear} \\
    {authors} \\
    --download-url {url} \\
    --field "{collected_entry.field}/{collected_entry.category}"

                    """
                    print(command)