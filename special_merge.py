#!/usr/bin/env python
#
#
#   Originally this was going to be a wrapper for arcpy.Merge_management
#   but I gave up on that.
from __future__ import print_function
import arcpy
import os

def badtaxlot(taxlot):
    badsuffixes = [
        "ROADS",
        "RAILS",
        "WATER",
        "STR",
        ]

    # Strip out parcels that are not suitable, ROW, water etc
    for s in badsuffixes:
        if taxlot.endswith(s):
            return True

    return False

def emptyjoin(sep, list):
    rval=''
    for s in list:
        if s:
            if rval:
                rval += sep + s
            else:
                rval = s
    return rval


def merge_rlis(infile, output):
    """ Merge in the RLIS feature class """
    print("Processing", infile)

    fields = ["SHAPE@","TLID",
              "SITEADDR","SITECITY","SITEZIP","COUNTY",
              "OWNER1", "OWNER2", "OWNER3", "OWNERADDR", "OWNERCITY", "OWNERSTATE", "OWNERZIP",
              "PROP_CODE"
              ]
    d_countycode = {
        'M':'Multnomah',
        'C':'Clackamas',
        'W':'Washington',
    }

    rows = arcpy.da.SearchCursor(infile, fields)
    count = errors = unwanted_taxlot = 0

    for row in rows:
        # Is this parcel >= 20?
        size_acres = round(row[0].area / 43560,1)
        if size_acres >= 20:
            count += 1
            taxlot = row[1].strip()

            # Strip out parcels that are not suitable, ROW, water etc
            if badtaxlot(taxlot):
                unwanted_taxlot +=1

            else:
                situs_st  = row[2].strip()
                situscity = row[3].strip()
                situszip  = row[4].strip()
                countycode = row[5].strip()

                o1 = row[6].strip()
                o2 = row[7].strip()
                o3 = row[8].strip()
                a  = row[9].strip()
                c  = row[10].strip()
                s  = row[11].strip()
                z  = row[12].strip()
                pc = row[13].strip()
                owner   = emptyjoin('<br />',[o1, o2, o3, a, ','.join([c, ' '.join([s, z]) ]) ])

                if situs_st=='0' or situs_st=='':
                    situs=''
                else:
                    situs = emptyjoin('<br />',[situs_st,situscity,situszip])

                out = []
                out.append(row[0])      # shape

                out.append(taxlot)
                out.append(owner)
                
                out.append(situs)
                
                try:
                    county = d_countycode[countycode]
                except KeyError:
                    arcpy.AddMessage("??? countycode is", countycode)
                    county = countycode
                
                out.append(county)
                out.append(str(pc))

                out.append('')          # subtype
                out.append(size_acres)
                
                out.append(0) # hvf
                out.append(0) # ara
                
                out.append(0) # nonarable
                #out.append(0) # p_nonarable
                
                #out.append(0) # niclass
                #out.append(0) # p_niclass

                try:
                    output.insertRow(out)
                except Exception as e:
                    print("Output error: %s" % e)
                    errors += 1
                del out
    del row
    del rows
    return errors


def merge_marion(infile, output):
    """ Merge in the Marion feature """
    print("Processing", infile)

    fields = ["SHAPE@",
              "TAXLOT",
              "STREET",
              "OWNERNAME", "OWNERADD1", "OWNERADD2", "OWNERADD3", "OWNERCITY", "OWNERSTATE", "OWNERZIP",
              "PROPCLAS_S" # prop code
              ]
    rows = arcpy.da.SearchCursor(infile, fields)

    count = errors = unwanted_taxlot = 0
    
    for row in rows:
        # Is this parcel >= 20?
        size_acres = round(row[0].area / 43560,1)
        if size_acres >= 20:
            count += 1
            taxlot = row[1].strip()
            situs  = row[2].strip()

            # Strip out parcels that are not suitable, ROW, water etc
            if badtaxlot(taxlot):
                unwanted_taxlot +=1
            else:

                o  = row[3].strip()
                a1 = row[4].strip()
                a2 = row[5].strip()
                a3 = row[6].strip()
                c  = row[7].strip()
                s  = row[8].strip()
                z  = row[9].strip()
                pc = row[10].strip()
                owner   = emptyjoin('<br />', [o, a1, a2, a3, ','.join([c, ' '.join([s, z]) ]) ])


                if situs=='0': situs=''

                out = []

                out.append(row[0])      # shape

                out.append(taxlot)
                out.append(owner)
                out.append(situs)
                out.append('Marion')    # county

                out.append(str(pc))

                out.append('')          # subtype
                out.append(size_acres)
               
                out.append(0) # hvf
                out.append(0) # ara
                
                out.append(0) # nonarable
                #out.append(0) # p_nonarable
                
                #out.append(0) # niclass
                #out.append(0) # p_niclass

                try:
                    output.insertRow(out)
                except Exception as e:
                    print("Output error: %s" % e)
                del out


    print("%d features, %d errors, %d unwanted" % (count, errors, unwanted_taxlot))
    del row
    del rows
    return errors


def merge_yamhill(infile, output):
    """ Merge in the Yamhill feature """
    print("Processing", infile)

    fields = ["SHAPE@",
              "taxlot_shape_MapTaxlot", # 1
              "Owner1", "Owner2", "Owner3", #2
              "MailAdd1","MailAdd2", "MailCity","MailState","MailZip", # 5
              "SitusAddress", "SitusCity", "SitusZip", # 10
              "taxlot_shape_ACCOUNT" # 13 prop code
              ]
    rows = arcpy.da.SearchCursor(infile, fields)

    count = errors = unwanted_taxlot = 0
    
    for row in rows:
        # Is this parcel >= 20?
        size_acres = round(row[0].area / 43560,1)
        if size_acres >= 20:
            count += 1
            taxlot    = row[1].strip()
            situsaddr = row[10]
            situscity = row[11]
            situszip  = row[12]

            # Strip out parcels that are not suitable, ROW, water etc
            if badtaxlot(taxlot):
                unwanted_taxlot +=1
            else:

                o1 = row[2]
                o2 = row[3]
                o3 = row[4]
                a1 = row[5]
                a2 = row[6]
                c  = row[7]
                s  = row[8]
                z  = row[9]
                pc = row[13]
                
                owner   = emptyjoin('<br />', [o1,o2,o3, a1,a2, ','.join([c, ' '.join([s, z]) ]) ])

                situs = emptyjoin('<br />', [situsaddr, ' '.join([situscity, situszip])])
                if situsaddr=="": situs = ''
                
                out = []

                out.append(row[0])      # shape

                out.append(taxlot)
                out.append(owner)
                out.append(situs)
                out.append('Yamhill')    # county

                out.append(str(pc))

                out.append('')          # subtype
                out.append(size_acres)
               
                out.append(0) # hvf
                out.append(0) # ara
                
                out.append(0) # nonarable
                #out.append(0) # p_nonarable
                
                #out.append(0) # niclass
                #out.append(0) # p_niclass

                try:
                    output.insertRow(out)
                except Exception as e:
                    print("Output error: %s" % e)
                del out

    print("%d features, %d errors, %d unwanted" % (count, errors, unwanted_taxlot))
    del row
    del rows
    return errors


def create_fc(path, sref):
    """ Set up output feature class """

    (workspace,output_fc) = os.path.split(path)

    if arcpy.Exists(path): arcpy.Delete_management(path)

    arcpy.CreateFeatureclass_management(workspace, output_fc, 'POLYGON', spatial_reference=sref)

    arcpy.AddField_management(path, "TAXLOT",    "TEXT",   field_length=20, field_is_required=True) # 1
    arcpy.AddField_management(path, "OWNER",     "TEXT",   field_length=200)   # 2
    arcpy.AddField_management(path, "SITUS",     "TEXT",   field_length=200)   # 3
    arcpy.AddField_management(path, "COUNTY",    "TEXT",   field_length=15)    # 4
    arcpy.AddField_management(path, "PROP_CODE", "TEXT",   field_length=6)
    
    arcpy.AddField_management(path, "subtype",     "TEXT",   field_length=1)
    arcpy.AddField_management(path, "acres",       "DOUBLE")
    arcpy.AddField_management(path, "hvf",         "DOUBLE")
    arcpy.AddField_management(path, "ara",         "DOUBLE")
    arcpy.AddField_management(path, "nonarable",   "DOUBLE")
    #arcpy.AddField_management(path, "p_nonarable", "DOUBLE")
    #arcpy.AddField_management(path, "niclass",     "DOUBLE")
    #arcpy.AddField_management(path, "p_niclass",   "DOUBLE")

    output = arcpy.da.InsertCursor(path, ["SHAPE@", "TAXLOT", "OWNER", "SITUS", "COUNTY", "PROP_CODE",
                                          "subtype", "acres",
                                          "hvf",
                                          "ara",
                                          "nonarable",
                                          #"p_nonarable",
                                          #"niclass", "p_niclass"
                                          ])
    return output

# ======================================================================

# UNIT TESTING
# You can run this file directly when writing it to aid in debugging

if __name__ == '__main__':

    folder = 'D:\\Google Drive\\CEG_GIS\\NexusSolutions'

    marion    = os.path.join(folder, 'marion_county.gdb\\taxlot')
    rlis      = os.path.join(folder, 'metro_rlis.gdb\\taxlot')
    yamhill   = os.path.join(folder, 'yamhill_county.gdb\\taxlot')
    output_fc = os.path.join(folder, 'workspace.gdb', 'taxlot_Merge')

    sref = arcpy.Describe(marion).spatialReference
    cursor=create_fc(output_fc, sref)
    merge_yamhill(yamhill, cursor)
    merge_marion(marion, cursor)
    merge_rlis(rlis, cursor)
    del cursor
    
# That's all
