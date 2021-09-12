


from collections import UserList
import collections
from papertrack.core import *

@register_downloader
class SimpleDownloader:
    name = "simple"
    params = {
        "url": {
            "type": "string"
        },
        "tool": {
            "type": "string",
            "default": "wget"
        }
    }
    def __init__(self, url, tool):
        self.url = url
        self.tool = tool
    
    def download(self):
        print("Downloading from %s" % self.url)
        print("  Tool used: %s" % self.tool)
        return "/sample/location.pdf"

@register_collector
class SimpleCollector:
    name = "simple"
    params = {
        "author": {
            "type": "list",
            "description": "Specify list of authors"
        }
    }
    def __init__(self, author):
        self.authors = author
    def collect(self, location):
        print("Collecting from %s" % location)
        print("Specified authors:")
        for author in self.authors:
            print(author)
        # operate with database here 