# secure-time-sync
A simple python3 script that securely syncs the time to the correct UTC time.
This script connects to a variety of websites and extracts the current UTC time from the http header "date"

The website is randomly selected from a pool of carefully chosen websites.

The current websites in the pool are:

* The Tor Project
* The Tails website
* The Whonix website
* DuckDuckGo
* The EFF's website

The script can optionally connect to these websites over Tor and will connect to an onion service where possible.
If not using Tor, the script protects against https downgrade attacks by enforcing TLS with curl.

# Usage
To use the script
1. install the depencies (`pip install requests[socks]`)
2. download it (`curl https://raw.githubusercontent.com/iloveyumyumshrimpnoodles/secure-time-sync/main/secure-time-sync.py -O`)
3. make it executable (`chmod +x secure-time-sync.py`)
4. run it with sudo:
```
sudo ./secure-time-sync.py
```

To use it with Tor, run:
```
sudo ./secure-time-sync.py --use-tor
```
 
This will configure `python-requests` to use Tor as SOCKS5 proxy. Port 9050 is the default Tor SocksPort.

Debugging information (the selected website and extracted time) can be viewed by adding the `--debug` argument:
```
sudo ./secure-time-sync.py --debug
```

To view additional arguments, use the `--help` or `-h` arguments

```
sudo ./secure-time-sync.py --help
```

# Notes
The script needs to be run as root so it can set the time.

To make this script run daily, you can configure a cron job to automatically run it.

This script doesn't support any timezones other than UTC.
