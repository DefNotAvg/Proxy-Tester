# Proxy Tester

A simple program to test proxies from multiple text files on multiple sites.

## Getting Started

Edit config.json to your liking, make sure text files containing proxies are in the same folder as this program, then run main.py.

## config.json

* testNum - Number of proxies from each file to test (any number less than 1 will test all proxies)
* sites - Websites to test each proxy on
* timeout - Number of ms to wait before aborting a request
* width - Number of characters to center the program output around

## Prerequisites

* Working on Python 2.7.16 or Python 3.6.8
* [requests](http://docs.python-requests.org/en/master/)
* [eventlet](https://eventlet.net/)

## To-Do

- [ ] Update README with examples