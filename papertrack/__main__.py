
from papertrack .simple import * 
from papertrack.core import * 

downloader = get_downloader_instance("simple", simple_ask_fn)
collector = get_collector_instance("simple", simple_ask_fn)

location = downloader.download()
collector.collect(location)