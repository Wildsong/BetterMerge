#!/usr/bin/python
#
# Note : For some reason this has to run using the Apple version of Python not the Brew version
#


# Edit the CSV file to fix up the OWNER and SITUS columns, splitting them out so they are more usable.
#

from __future__ import print_function
import os
import csv

folder = "/Users/bwilson/Google Drive/CEG_GIS/NexusSolutions"
csvfile = "willamette_sites_BR.csv"
outputcsvfile = "willamette_sites.csv"

csvfile = 'willamette_sites_powerlines_BR.csv'
outputcsvfile = 'willamette_sites_powerlines.csv'

os.chdir(folder)

def split(str):
    return str.split('<br />')

def unit_test():
    print(split(""))
    print(split("one token"))
    print(split("two<br />tokens"))
    print(split("three<br />tokens<br />"))
    exit(0)
    
unwantedfieldnames = ['Join_Count', 'TARGET_FID', 'Shape_Area', 'Shape_Leng']

reprocessed_rows = []
ocol = scol = 1
cnt = 0
with open(csvfile, "r") as fp:
    rdr = csv.DictReader(fp, delimiter=',',quotechar='"')

    for row in rdr:
        owner = split(row['OWNER'])
        situs = split(row['SITUS'])
        ocol = max(ocol,len(owner))
        scol = max(scol,len(situs))
#        print(owner, ocol, situs, scol)

        ocnt = 1
        for o in owner:
            row['OWNER'+str(ocnt)]=o
            ocnt+=1
        del row['OWNER']
        
        scnt = 1
        for s in situs:
            row['SITUS'+str(scnt)]=s
            scnt+=1
        del row['SITUS']
        
        for col in unwantedfieldnames:
            try:
                del row[col]
            except KeyError:
                pass
        
        reprocessed_rows.append(row)
#        print(row)
        cnt += 1
        
colowner = ['OWNER'+str(x+1) for x in range(0,ocol)]
colsitus = ['SITUS'+str(x+1) for x in range(0,scol)]

print(cnt, ocol, scol)

fieldnames = ['OID', 'TAXLOT'] + colowner + colsitus + ['COUNTY', 'PROP_CODE', 'subtype', 'acres', 'hvf', 'ara', 'nonarable']

#fieldnames.append('Substn') # sites near substations
fieldnames.append('pwrline')
fieldnames.append('pwrdist') # sites near powerlines

print(fieldnames)

#for row in reprocessed_rows:
#    print(row)
#    exit(0)
#exit(0)

# Write the finished CSV file

with open(outputcsvfile,"w") as fp:
    wrtr = csv.DictWriter(fp, fieldnames=fieldnames)
    wrtr.writeheader()
    for row in reprocessed_rows:
        try:
            del row['Shape_Length']
        except:
            pass
        for k in ['acres', 'hvf', 'ara', 'nonarable']:
            row[k] = str(round(float(row[k]),2)) # fix stupid floaty doubles
        try:
            wrtr.writerow(row)
        except ValueError as e:
            print("ValueError means you probably got the fieldnames wrong.", e)
print("all done!")
        

