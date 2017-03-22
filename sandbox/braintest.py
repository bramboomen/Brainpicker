#! python3

from crawler import *
from indexer import *
import sys


bp = "https://www.brainpickings.org/2017/03/01/mary-ruefle-madness-rack-and-honey-prayer/"


def crawltest():
    print("visiting: " + bp)
    crawler = Crawler()
    links = crawler.get_internal_links(bp)
    for l in links:
        print(l)


def indextest():
    indexer = Indexer(2017, 3, 1, local=False, save=False)
    index = indexer.bp_index()
    print("-----------------------------------------------")
    print("-------------------- index --------------------")
    print("-----------------------------------------------")
    for i in index:
        print(i)


# crawltest()
indextest()
