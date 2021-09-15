


from collections import UserList
import collections
from genericpath import exists
from papertrack.core import *
import os 

@register_downloader
class SimpleDownloader:
    name = "simple"
    params = {
        "url": {
            "type": "string",
            "description": "URL to download PDF from"
        },
        "location": {
            "type": "string",
            "default": os.path.join("/tmp", "papertrack-downloads"),
            "description": "Location where PDF are going to be downloaded at."
        }
    }
    def __init__(self, url, location):
        self.url = url
        self.download_location = location
    
    def _download(self, url, output):
        import urllib.request
        urllib.request.urlretrieve(url, output)
    
    def download(self):
        print("Downloading from %s" % self.url)
        import datetime 
        name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S.pdf")
        os.makedirs(self.download_location, exist_ok=True)
        output = os.path.join(self.download_location, name)
        self._download(self.url, output)
        return output


@register_collector
class SimpleCollector:
    name = "simple"
    params = {
        "author": {
            "type": "list",
            "description": "Specify list of authors"
        },
        "title": {
            "type": "string",
            "description": "Specify title"
        },
        "year": {
            "type": "int",
            "description": "Specify year of publication"
        },
        "category": {
            "type": "string",
            "description": "Select category (e.g. distributed systems)"
        },
        "field": {
            "type": "string",
            "description": "Select field of study (e.g. Computer Science)"
        },
        "location": {
            "type": "string",
            "description": "Path where the papers are stored (with categories as subdirs and fields as their subdirs)",
            "default": "/data/Documents/Library/Papers"
        }
    }
    def __init__(self, author: list, title: str, year: int, category, field, location):
        self.authors = author
        self.title = title 
        self.year = year
        self.field = field
        self.category = category
        self.location = location
    
    def _convert_author(self, author):
        return "".join(x[0] + ". " for x in author.split()[:-1]) + author.split()[-1]
    
    def _convert_authors(self, authors):
        return " ".join(self._convert_author(x) for x in authors)

    def collect(self, location):
        import shutil
        print("Collecting from %s" % location)
        os.makedirs(os.path.join(self.location, self.field, self.category), exist_ok=True)
        shutil.move(location, os.path.join(
            self.location,
            self.field,
            self.category,
            f"{self._convert_authors(self.authors)} - {self.title} ({self.year}).pdf"
        ))