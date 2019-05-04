from __future__ import print_function, division
import eventlet
eventlet.monkey_patch()
import requests
import json
import glob
import os
import math
import sys

if sys.version_info[0] < 3:
	import timeit
	timer = timeit.default_timer
else:
	import time
	timer = time.process_time

def settings(config):
	try:
		with open(config, 'r') as myfile:
			return json.load(myfile)
	except IOError:
		with open(config, 'w') as myfile:
			json.dump({}, myfile)
		return {}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
config = settings('config.json')
sites = config['sites']
timeout = config['timeout']
width = config['width']
site_names = [site.split('.')[-2].replace('https://', '').replace('http://', '').title() for site in sites]
files = [item for item in glob.glob('./*.txt') if all(site not in item for site in site_names)]
proxies = []

def center(text, spacer=' ', length=width, clear=False):
	if clear:
		os.system('cls' if os.name == 'nt' else 'clear')
	count = int(math.ceil((length - len(text)) / 2))
	if count > 0:
		print(spacer * count + text + spacer * count)
	else:
		print(text)

def test_proxy(proxy, site):
	try:
		proxy_parts = proxy.split(':')
		ip, port, username, password = proxy_parts[0], proxy_parts[1], proxy_parts[2], proxy_parts[3]
		proxies = {
			'http': 'http://{}:{}@{}:{}'.format(username, password, ip, port),
			'https': 'https://{}:{}@{}:{}'.format(username, password, ip, port)
		}
	except IndexError:
		proxies = {'http': 'http://' + proxy, 'https': 'https://' + proxy}
	start = int(round(timer() * 1000))
	try:
		with eventlet.Timeout(timeout / 1000):
			try:
				response = requests.get(site, headers=headers, proxies=proxies)
				if response.status_code != 200:
					center('{} is a bad proxy.'.format(proxy))
					return False
				else:
					center('{} - {} ms'.format(proxy, str(int(round(timer() * 1000)) - start)))
					return True
			except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError):
				center('{} is a bad proxy.'.format(proxy))
				return False
	except eventlet.timeout.Timeout:
		center('{} timed out.'.format(proxy))
		return False
center(' ', clear=True)
center('Proxy Tester by @DefNotAvg')
center('-', '-', width)
if files:
	for file in files:
		with open(file, 'r') as myfile:
			proxies += myfile.read().splitlines()
else:
	center('No text files found in current folder.')
	quit()
if proxies:
	for i in range(0, len(sites)):
		site = sites[i]
		site_name = site_names[i]
		if i != 0:
			center('-', '-')
		center(site_name)
		center('-', '-', width)
		passed = []
		failed = []
		for proxy in proxies:
			if test_proxy(proxy, site):
				passed.append(proxy)
			else:
				failed.append(proxy)
		with open('{}.txt'.format(site_name), 'w') as myfile:
			myfile.write('Passed\n------\n{}\n\nFailed\n------\n{}'.format('\n'.join(passed), '\n'.join(failed)))
		print('')
		center('{}/{} proxies are valid.'.format(str(len(passed)), str(len(proxies))))
else:
	center('No proxies found in text files in current folder.')
	quit()