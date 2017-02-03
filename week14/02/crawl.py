"""
Crawls the webpages and saves information in the DB
"""
import requests
from bs4 import BeautifulSoup

from model import Server, session

servers = {}
unique_links = set()
site_url = 'http://register.start.bg'
site_response = requests.get(site_url)
servers[site_response.headers['Server']] = 1
bs = BeautifulSoup(site_response.content)
for link in bs.find_all('a'):
    unique_links.add(link.get('href'))

# read links servers
for link in unique_links:
    try:
        if link.startswith("http"):
            site_response = requests.get(site_url, verify=False)
        else:
            url = site_url + '/' + link
            site_response = requests.get(url, verify=False)
        if 'Server' not in site_response.headers:
            continue
        site_server = site_response.headers['Server']
        if site_server not in servers:
            servers[site_server] = 0
        servers[site_server] += 1
    except Exception:
        continue

to_add: [Server] = []
for serv, occ in servers.items():
    to_add.append(Server(server_name=serv, occurences=occ))
session.add_all(to_add)
session.commit()
