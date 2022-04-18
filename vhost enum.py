#!/usr/bin/env python3

import requests
from sys import argv, exit
from os import system as cmd

if len(argv) != 4:
	exit("[+] Use: ./vhost-enum.py http://domain.com /path/to/wordlist 'string to exclude (filter)'\nExample: ./vhost-enum.py http://tryhard.thm /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt '404'")


uri = argv[1]
wordlist = argv[2]
filter = argv[3]

if 'http://' not in uri and 'https://' not in uri:
	uri = f"http://{uri}/"

with open(wordlist) as wordlist_file:
	subdomains = [line.rstrip() for line in wordlist_file.readlines()]

domain = uri.replace('http://', '').replace('/', '')
try_n = 0

for subdomain in subdomains:
	headers = {
	"Host": f"{subdomain}.{domain}"
	}
	request = requests.get(uri, headers=headers, allow_redirects=False)
	try_n += 1
	if filter not in request.text:
		print(f"[+] Valid subdomain: {subdomain}, adding to file ./subdomains-{domain}.txt")
		cmd(f"echo {headers['Host']} >> subdomains-{domain}.txt")
		cmd("sleep 2")
	else:
		cmd("clear")
		print(f"[+] Try n. {try_n} // Trying: {headers['Host']} // Can't contain the string: {filter}")
