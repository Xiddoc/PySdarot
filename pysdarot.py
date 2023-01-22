"""
Main file to run command arguments on.

API class is in the `pysdarot` module/folder.
"""
from argparse import ArgumentParser
from json import load, dump
from typing import Dict

from pysdarot import PySdarot, Show

if __name__ == "__main__":
    # Initialize arg parser
    parser = ArgumentParser()
    subparser = parser.add_subparsers(help="CLI commands", required=True)

    # Set up the Sdarot configuration
    config_cmd = subparser.add_parser("config", help="Set up the command line app configuration.")
    config_cmd.add_argument("--tld", type=str, help='The currently active Sdarot TV top level domain (for example, if '
                                                    'the current website is "sdarot.tw", then you would write "tw".')
    config_cmd.add_argument("--username", type=str, help='Your SdarotTV USERNAME to use for downloading episodes.')
    config_cmd.add_argument("--password", type=str, help='Your SdarotTV PASSWORD to use for downloading episodes.')

    # Set up the "search"
    search_cmd = subparser.add_parser("search", help="Search the website for shows to watch.")
    search_cmd.add_argument("query", type=str, nargs='+', help="The search query to run.")

    # Set up the "download" functionality
    download_cmd = subparser.add_parser("download", help="Downloads content from the website.")
    download_cmd.add_argument("show", type=int, help="The show ID to download.")
    download_cmd.add_argument("season", type=int, help="The season number to download.")
    download_cmd.add_argument("episode", type=int, help="The episode number to download. "
                                                        "If set to -1, this downloads the entire season.")

    # Finally, parse the arguments themselves
    args = vars(parser.parse_args())

    """
    Get the Sdarot CMD-line config.
    """
    old_config = {}
    try:
        with open("./config.json", 'r') as f:
            config: Dict[str, str] = load(f)
    except OSError:
        config = {'tld': None, 'username': None, 'password': None}

    # Operate for 'config' command
    if 'tld' in args:
        print(f"[+] Configuring the settings...")

        # Update and write
        for key, val in args.items():
            # Only write if not None
            config[key] = val or config[key]

        with open("./config.json", 'w') as f:
            dump(config, f)

        print(f"[+] New settings saved!")

    # Operate for 'search' command
    elif 'query' in args:
        q = ' '.join(args["query"])
        print(f'[+] Querying "{q}"...')

        # Check that TLD exists
        if not config['tld']:
            print('[-] Sdarot TLD not configured, use "config" command to fix this.')
            exit(1)

        # Get shows
        sdarot = PySdarot(sdarot_tld=config['tld'])
        shows = sdarot.small_search(q)

        print("[+] Found the following shows:")
        for show in shows:
            print(f"[{show.show_id}] {show.name}")

    # Operate for 'download' command
    elif 'show' in args:
        print(f"[+] Identifying show with ID {args['show']}...")

        # Check that TLD, username, and password exist
        if not config['tld']:
            print('[-] Sdarot TLD not configured, use "config" command to fix this.')
            exit(1)
        elif not config['username'] or not config['password']:
            print('[-] Sdarot username/password not configured, use "config" command to fix this.')
            exit(1)

        # Log in to Sdarot for downloading
        PySdarot(sdarot_tld=config['tld'], username=config['username'], password=config['password'])
        # Get the show name before downloading
        show = Show(args['show'])
        show.populate_show_data()
        print(f"[+] Show found: \n"
              f"[EN] {show.en_name}\n"
              f"[HE] {show.he_name}\n"
              f"[Season #] {show.get_season_count()}\n")

        # Start download
        download_season = args["episode"] == -1
        print(f'[+] Downloading season {args["season"]}, '
              f'{"ALL EPISODES" if download_season else "episode " + str(args["episode"])}...')

        # Create base filename for episodes
        base_name = ''.join([char for char in show.en_name if char.isalpha()])

        # Download entire season
        if download_season:
            print("[+] Loading episode information...")
            ep_count = show.get_episode_count(args["season"])

            print(f"[+] Found {ep_count} episodes in this season...")
            for episode in range(1, ep_count + 1):
                # Create filename and download
                fpath = f"{base_name}_S{args['season']}_E{episode}.mp4"
                print(f'[+] Downloading episode #{episode} to "{fpath}"...')

                show.download_episode(
                    season=args['season'],
                    episode=episode,
                    file_path=fpath
                )
        else:
            # Download 1 episode
            fpath = f"{base_name}_S{args['season']}_E{args['episode']}.mp4"
            print(f'[+] Downloading episode #{args["episode"]} to "{fpath}"...')

            show.download_episode(
                season=args['season'],
                episode=args['episode'],
                file_path=fpath
            )

    else:
        print("[-] Error with command parsing...")
        exit(1)
