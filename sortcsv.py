#!/usr/bin/python
#
# Note : For some reason this has to run using the Apple version of Python not the Brew version
#
# Read two CSV files and generate an output showing the differences
#
from __future__ import print_function
import os
import csv

folder = "/Users/bwilson/Google Drive/CEG_GIS/NexusSolutions"

current="willamette_sites_20170217.csv"
old="willamette_sites_20170210.csv"
diff="output.csv"

os.chdir(folder)


def read_csv(csvfile):
    d = {}
    with open(csvfile, "r") as fp:
        rdr = csv.DictReader(fp, delimiter=',',quotechar='"')
        for row in rdr:
            taxlot = row['TAXLOT']
            d[taxlot] = row
    return d


d_current = read_csv(current)
d_old = read_csv(old)

squelched = {}
added = {}

numbers = ['subtype', 'acres', 'hvf', 'ara', 'nonarable']

def compare(da, db):
    d_changed = {}

    for k in da:
        msg = ''
        arow = da[k]
        try:
            changed = False
            brow = db[k]
            # compare, how did they change?
            if arow['subtype'] != brow['subtype']:
                msg = "taxlot '%s'\n" % k
                for n in numbers:
                    if arow[n] != brow[n]:
                        msg += '\t%s %s %s\n' % (n, arow[n], brow[n])
                print(msg)
        except KeyError:
            d_changed[k] = arow
            pass

    return d_changed

print(len(d_current), len(d_old))
print(len(added))

compare(d_current, d_old)
compare(d_old, d_current)

