"""
Main file to run command arguments on.

API class is in the `pysdarot` module/folder.
"""
from argparse import ArgumentParser
from json import load, dump
from typing import Dict

from pysdarot import PySdarot

if __name__ == "__main__":
    # Initialize arg parser
    parser = ArgumentParser()
    subparser = parser.add_subparsers(help="CLI commands", required=True)

    # Set up the Sdarot configuration
    config_cmd = subparser.add_parser("config", help="Set up the Sdarot TLD.")
    config_cmd.add_argument("tld", type=str, help='The currently active Sdarot TV top level domain (for example, if '
                                                  'the current website is "sdarot.tw", then you would write "tw".')

    # Set up the "search"
    search_cmd = subparser.add_parser("search", help="Search the website for shows to watch.")
    search_cmd.add_argument("query", type=str, help="The search query to run.")

    # Set up the "download" functionality
    download_cmd = subparser.add_parser("download", help="Downloads content from the website.")
    download_cmd.add_argument("show", type=int, help="The show ID to download.")
    download_cmd.add_argument("season", type=int, help="The season number to download.")
    download_cmd.add_argument("episode", type=int, help="The episode number to download. "
                                                        "If set to -1, this downloads the entire season.")

    # Finally, parse the arguments themselves
    args = vars(parser.parse_args())

    # Read config
    old_config = {}
    try:
        with open("./config.json", 'r') as f:
            config: Dict[str, str] = load(f)
    except OSError:
        config = {}

    if 'tld' in args:
        print(f"[+] Configuring the SdarotTV TLD...")
        print(f'[+] Updating TLD to "{args["tld"]}"...')

        # Update and write
        config['tld'] = args["tld"]
        with open("./config.json", 'w') as f:
            dump(config, f)

    elif 'query' in args:
        print(f'[+] Querying "{args["query"]}"...')
        if 'tld' not in config:
            print('[-] Sdarot TLD not configured, use "config" command to fix this.')
            exit(1)

        # Get shows
        sdarot = PySdarot(sdarot_tld=config['tld'])
        shows = sdarot.small_search(args["query"])

        print("[+] Found the following shows:")
        for show in shows:
            print(f"[{show.show_id}] {show.name}")
