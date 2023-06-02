#!/usr/bin/env -S python3

#    Secure Time Synchronization
#    Copyright (C) 20223 iloveyumyumshrimpnoodles
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Inspired by https://gitlab.com/madaidan/secure-time-sync

import os, sys, requests
from random import SystemRandom, Random

if "-h" in sys.argv or "--help" in sys.argv:
    print(f"Usage: ./{sys.argv[0]}")

    print("Extra arguments:")
    print(" --use-tor    : use Tor as SOCKS5 proxy, and connect to hidden services when available")
    print(" -y | --yes   : ignore prompts, and just continue")
    print(" --no-ssl     : Don't use https, useful for fixing invalid datetime settings")
    print(" --debug      : Print selected URL and parsed time")
    print(" --use-hw-rng : Use the hardware RNG, rather than the default python one")

    exit()

if os.getuid() != 0:
    sys.exit("ERROR: This program needs to be run as root.")

use_tor = "--use-tor" in sys.argv
yes_to_all = "-y" in sys.argv or "--yes" in sys.argv
no_ssl = "--no-ssl" in sys.argv
debug = "--debug" in sys.argv

proxy = ""
if use_tor:
    proxy = "socks5h://localhost:9050"

if "--use-hw-rng" in sys.argv:
    rng = SystemRandom()
else:
    rng = Random()

if no_ssl:
    print("WARNING: Your connection is not secured, and can be monitored!")

    if not yes_to_all:
        input("Press [ENTER] to continue")

pool = [
    ("www.torproject.org", "2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion"),
    ("duckduckgo.com", "duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion"),
    ("www.whonix.org", "dds6qkxpwdeubwucdiaord2xgbbeyds25rbsgr73tbfpqpt4a6vjwsyd.onion"),
    ("eff.org", None),
    ("tails.boum.org", None)
]

def select_pool() -> str:
    """
    Selects a random URL from the pool

    Returns:
        str: Randomly picked URL
    """

    url, hs = rng.choice(pool)

    if use_tor and hs != None:
        url = hs

    if no_ssl or use_tor:
        proto = "http"
    else:
        proto = "https"

    return f"{proto}://{url}"

def fetch_time(url: str) -> str:
    """
    Fetches the URL, and returns the time

    Args:
        url str: URL to fetch
    
    Returns:
        str: Parsed time
    """

    try:
        req = requests.head(
            url,
            proxies={"http": proxy, "https": proxy}
        )

    except Exception as exc:
        if debug:
            print(f"Stacktrace: {exc}")

        sys.exit(f"ERROR: Failed to fetch '{url}'")
    
    date = req.headers.get("date")
    if not date:
        sys.exit("ERROR: Couldn't find 'date' header")
    
    return date

if __name__ == "__main__":
    url = select_pool()
    time = fetch_time(url)

    if debug:
        print(f"DEBUG: Picked url '{url}'")
        print(f"DEBUG: Time: {time}")

    # set the time
    os.system(f"date -s '{time}'")