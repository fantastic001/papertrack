
from ast import Param
from papertrack .simple import * 
from papertrack.core import * 
import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="group")
get_group = subparsers.add_parser("get")
view_group = subparsers.add_parser("view")

for group_name in ["collector", "downloader", "viewer"]:
    group = subparsers.add_parser(group_name)
    group.add_argument("--list", action="store_true", help="List all instances that can be used for %s" % group_name)
    group.add_argument("--describe", metavar=group_name, help="Show available options for particular %s" % group_name)

get_group.add_argument("--downloader", choices=list(downloader.name for downloader in get_all_components("downloader")))
get_group.add_argument("--collector", choices=list(collector.name for collector in get_all_components("collector")))

args, rest = parser.parse_known_args()

def get_component_parser(name, type):
    component = get_component_class(name, type)
    parser = argparse.ArgumentParser(prog=f"papertrack ... --{type} {component.name}")
    for param, definition in component.params.items():
        arg_name = "--download-%s" % param if type == "downloader" else "--%s" % param
        parser.add_argument(arg_name, help=definition.get("description", ""), choices=definition.get("choices", None), default=definition.get("default", None))

    return parser

if args.group == "get":
    downloader_parser = get_component_parser(args.downloader, type="downloader")
    collector_parser = get_component_parser(args.collector, type = "collector")

    downloader_args, rest = downloader_parser.parse_known_args(rest)
    collector_args = collector_parser.parse_args(rest)
    downloader_config = {param: getattr(downloader_args, "download_%s" % param) for param in get_component_class(
        args.downloader, 
        "downloader"
    ).params.keys() if hasattr(downloader_args, "download_%s" % param)}

    collector_config = {param: getattr(collector_args, "%s" % param) for param in get_component_class(
        args.collector, 
        "collector"
    ).params.keys() if hasattr(collector_args, "%s" % param)}


    downloader_config = {k:v for k,v in downloader_config.items() if v is not None}
    collector_config = {k:v for k,v in collector_config.items() if v is not None}

    downloader = get_downloader_instance(args.downloader, simple_ask_fn, **downloader_config)
    collector = get_collector_instance(args.collector, simple_ask_fn, **collector_config)

    location = downloader.download()
    collector.collect(location)

elif args.group == "view":
    pass
else:
    if args.list:
        for item in get_all_components(args.group):
            print(item.name)
        exit(0)
    if args.describe is not None:
        get_component_parser(args.describe, args.group).print_help()