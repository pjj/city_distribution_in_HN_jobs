#!/usr/bin/python


"""
This hack prints the number of jobs at select cities from HN who-is-hiring pages.
The examples below show the 2 use cases in action.
(Notice the systematic increase in the number of jobs in Cambridge MA.)

bash-3.2$ ./city_distribution_in_HN_jobs.py http://news.ycombinator.com/item?id=2831646
52 jobs in Silicon Valley
23 jobs in New York
17 jobs in London
16 jobs in Cambridge MA
5 jobs in Chicago

bash-3.2$ ./city_distribution_in_HN_jobs.py 
##############################
August 2011
52 jobs in Silicon Valley
23 jobs in New York
17 jobs in London
16 jobs in Cambridge MA
5 jobs in Chicago
##############################
July 2011
75 jobs in Silicon Valley
27 jobs in New York
17 jobs in Cambridge MA
8 jobs in London
5 jobs in Chicago
##############################
June 2011
58 jobs in Silicon Valley
32 jobs in New York
15 jobs in London
13 jobs in Cambridge MA
5 jobs in Chicago
##############################
May 2011
67 jobs in Silicon Valley
14 jobs in New York
11 jobs in Cambridge MA
11 jobs in London
5 jobs in Chicago
##############################
April 2011
58 jobs in Silicon Valley
20 jobs in New York
11 jobs in London
6 jobs in Cambridge MA
6 jobs in Chicago

Questions: pama @ hacker news
"""


import sys
import re
import urllib2
import collections
import operator
from BeautifulSoup import BeautifulSoup


cities = {
    "New York": r"New York|NYC",
    "Silicon Valley": r"San Francisco|Mountain View|Palo Alto",
    "Cambridge MA": r"Cambridge, MA|Cambridge MA|Boston",
    "Chicago": r"Chicago",
    # added London, as per transient request of prolepunk in http://news.ycombinator.com/item?id=2837153    
    "London": r"London" 
}


def city_stats_in_thread(url, cities=cities):
    "Return a dict of city: tally counting how many top-level threads mention a city"
    # Wait for up to 2 minutes before giving up with urlopen
    soup = BeautifulSoup(urllib2.urlopen(url, timeout=120).read())
    stats = collections.defaultdict(int)

    for comment in soup.findAll("span", "comment"):
        for city, regexp in cities.items():
            if re.search(regexp, str(comment)) is not None:
                stats[city] += 1
    return stats


def print_stats(url):
    stats = city_stats_in_thread(url)
    for city, tally in sorted(stats.items(), key=operator.itemgetter(1), reverse=True):
        print tally, "jobs in", city


def history():
    data = [
        ("September 2011", "http://news.ycombinator.com/item?id=2949787"),
        ("August 2011", "http://news.ycombinator.com/item?id=2831646"),
        ("July 2011", "http://news.ycombinator.com/item?id=2719028"),
        ("June 2011", "http://news.ycombinator.com/item?id=2607052"),
        ("May 2011", "http://news.ycombinator.com/item?id=2503204"),
        ("April 2011", "http://news.ycombinator.com/item?id=2396027")
        ]

    for month, url in data:
        print "#" * 30
        print month
        print_stats(url)


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "history":
        history()
        sys.exit(0)
        
    print_stats(sys.argv[1])
