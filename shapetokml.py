#!/usr/bin/python
#  We're using the Apple version of Python (in /usr/bin) not the Brew version (/usr/local/bin)
#
#  This does a whole bunch of work
#  to turn shapefiles into a proper KMZ file.
#
#  -- THIS DOES NOT RUN UNDER WINDOWS YET --
#
from __future__ import print_function
import os
import subprocess

doc_title = 'Willamette Valley Potential Sites'
    
# The input folder
# WINDOWS
folder = 'D:\\Google Drive\\CEG_GIS\\NexusSolutions'
# MAC
folder = '/users/bwilson/Google Drive/CEG_GIS/NexusSolutions'
# The output folder (and KMZ file)
output_folder = "Willamette"

# The shapefiles we'll be processing are
sites = "sites.shp"
subs = "substation.shp"
subs_buffer = "subbuffer.shp"
existing = "existing_sites.shp"
existing_buffer = "existing_sites_buffer.shp"
soils = "project.gdb/usda_farmland_class"

# ============================================================

from bs4 import BeautifulSoup
# To install BeautifulSoup on ArcGIS, open a shell and 
# chdir to your Python folder and type "./Scripts/pip install BeautifulSoup4" (NOTE the '4')
#
# On my computer, /c/Python27/ArcGISx6410.5 is the place to be.
# I installed it in /c/Python27/ArcGIS10.5 too just to be certain.

ogr2ogr_binary = "ogr2ogr"
# To install ogr2ogr, 
# download http://download.gisinternals.com/sdk/downloads/release-1500-x64-gdal-2-1-3-mapserver-7-0-4.zip
# or the latest zip, I chose the 1500 release because it matches ESRI, not sure if it matters
# Unpack it someplace convenient, I put it in my home directory under GDAL, so mkdir /c/Users/bwilson/GDAL
# and add the "bin" to your PATH, I added this to the end C:\Users\bwilson\GDAL\bin;C:\Users\bwilson\GDAL\bin\gdal\apps
# If it worked then you should be able to open a cmd window and type 'ogrinfo', and get usage info not an error.

# KML color order is B G R not R G B

RED = 'FF0000FF'
#                 (line color, polygon fill color)
color_hvf        = (RED,         None)      # Red outline
color_arable     = ('FF000000', '7f00FFFF') # yellow fill
color_nonarable  = ('FF000000', '7f00FF00') # green fill
#color_both      = ('FF000000', '7fFFFF00') # magenta fill

# Lookup table based on value of attribute 'subtype'
d_color = {
    'A':color_arable,
    'N':color_nonarable,
    'H':color_hvf,
}

color_class12   = ('FF0000FF', None) # red edge
color_class3    = ('FF40FFFF', None) # pale yellow edge
color_class4    = ('FF00FFFF', None) # yellow edge
color_class5678 = ('FF00FF00', None) # green edge

d_soil = {
    '1': color_class12,
    '2': color_class12,
    '3': color_class3,
    '4': color_class4,
    '5': color_class5678,
    '6': color_class5678,
    '7': color_class5678,
    '8': color_class5678,
}
rename = ['none','hvf','hvf','class 3', 'class 4', 'non-arable','non-arable','non-arable','non-arable']

# =====================================================================
def renamer_size(taxlot):
    # Not doing this step yet, soon,
    return None

def fix_sites(soup):
    """ Parse the polygon kml file and fix up the colors.  """

    lpm = soup.kml.Document.find_all('Placemark')

    #print(len(lpm),"objects")
    count = 0
    changed = 0
    
    # Look at each placemark
    for pm in lpm:
        count += 1
        ls=pm.find_all('SimpleData')
        taxlot = ''
        address = ''

        linecolor = RED
        fillcolor = None
        
        # Look at the attributes for this placemark
        for s in ls:
            try:
                if s.attrs['name'] == 'subtype':
                    subtype = s.contents[0]
                    if subtype:
                        (linecolor, fillcolor) = d_color[subtype]
                        #print(subtype, linecolor, fillcolor)
                        changed += 1

                    pass

                elif s.attrs['name'] == 'TAXLOT':
                    taxlot = s.contents[0]

                elif s.attrs['name'] == 'SITUS':
                    address = s.contents[0]

            except KeyError as e:
                print('Key error!',e)
                pass
            
            except Exception as e:
                print("Something bad:", e)
                exit(0)
            pass
        
        # Change linestyle color
        pm.Style.LineStyle.color.string.replace_with(linecolor)
         
        if fillcolor:
            # Change polystyle
            # Fill is YES
            pm.Style.PolyStyle.fill.string.replace_with('1')
        
            colortag = soup.new_tag("color")
            colortag.string = fillcolor
            pm.Style.PolyStyle.insert(0,colortag)
            colormodetag = soup.new_tag("colorMode")
            colormodetag.string = 'normal'
            pm.Style.PolyStyle.insert(1,colormodetag)
        
            outlinetag = soup.new_tag("outline")
            outlinetag.string = '1'
            pm.Style.PolyStyle.insert(1,outlinetag)

#            if renamer:
#                name = renamer(taxlot)
#                if name:
#                    nametag = soup.new_tag("name")
#                    nametag.string = name
#                    pm.insert(0,nametag)
        
        pass
    print("Sites: %d, changed: %d" % (count, changed))
    return soup


# ------------------------------------------------------------------------

def fix_soils(soup):
    """ Parse the "polygons" kml file and fix up the colors, use renamer to fix the KML name field.  """

    lpm = soup.kml.Document.find_all('Placemark')

    #print(len(lpm),"objects")
    count = 0
    changed = 0
    
    # Look at each placemark
    for pm in lpm:
        count += 1
        ls=pm.find_all('SimpleData')
        taxlot = ''
        address = ''

        linecolor = RED
        fillcolor = None
        
        # Look at the attributes for this placemark
        for s in ls:
            niccdcd = 'None'
            try:
                if s.attrs['name'] == 'niccdcd':
                    niccdcd = s.contents[0]
                    if niccdcd:
                        print(niccdcd)
                        (linecolor, fillcolor) = d_soil[niccdcd]
                        #print(subtype, linecolor, fillcolor)
                        changed += 1
                    pass

            except KeyError as e:
                print('Key error!',e)
                pass
            
            except Exception as e:
                print("Something bad:", e, niccdcd)

            pass

        # Change linestyle color
        pm.Style.LineStyle.color.string.replace_with(linecolor)
         
        if fillcolor:
            # Change polystyle
            # Fill is YES
            pm.Style.PolyStyle.fill.string.replace_with('1')
        
            colortag = soup.new_tag("color")
            colortag.string = fillcolor
            pm.Style.PolyStyle.insert(0,colortag)
            colormodetag = soup.new_tag("colorMode")
            colormodetag.string = 'normal'
            pm.Style.PolyStyle.insert(1,colormodetag)
        
            outlinetag = soup.new_tag("outline")
            outlinetag.string = '1'
            pm.Style.PolyStyle.insert(1,outlinetag)

            name = rename[niccdcd]
            if name:
                nametag = soup.new_tag("name")
                nametag.string = name
                pm.insert(0,nametag)
        
        pass
    print("Polygons: %d, changed: %d" % (count, changed))
    return soup


# ------------------------------------------------------------------------

def ogr2ogr(input_fc, kmlfile, options=None):
# ogr2ogr -f kml ${FILE}.kml ${FILE}.shp $FILE 

# Todo - get rid of subprocess - call ogr directly

    (folder, file) = os.path.split(input_fc)
    (base, ext) = os.path.splitext(file)

    if ext.lower() == '.shp':
        # SHAPEFILE
        container = input_fc
        layername = base
    else:
        container = folder
        layername = file
        print("FGDB are now possible", container)

    args = [ogr2ogr_binary, '-f', 'KML']
    if options: args += options

    args += [kmlfile, container, layername]
    #print(args)
    p = subprocess.check_output(args)

# Todo - check return code from process
    print("ogr2ogr says", p)
    return True

# ------------------------------------------------------------------------
# This is the main entry point for ESRI python toolbox

def convert_polygons(input_fc, output_kml, kml_fixer):
    sqlsort = [] # ['-sql', 'SELECT '] NOT YET THIS IS SUPPOSED TO SORT FEATURES

    if not ogr2ogr(input_fc, output_kml, sqlsort):
        print("Writing KML failed.")
        exit(1)

    soup = BeautifulSoup(open(output_kml,'r'), 'xml')
    kml_fixer(soup)

    with open(output_kml,"w") as fp:
        fp.write(str(soup))

    return

def convert_point(input_fc, output_kml, symbolignored):
    ogr2ogr(input_fc, output_kml)
    # Should I change the point symbols?
#    # Overwrite the KML file.
#    with open(output_kml,"w") as fp:
#        fp.write(str(soup))
    return

def convert_buffer_ring(input_fc, output_kml, linecolor):
    ogr2ogr(input_fc, output_kml)
    
    soup = BeautifulSoup(open(output_kml,'r'), 'xml')

    # Fix the line color. 
    lpm = soup.kml.Document.find_all('Placemark')
    for pm in lpm: pm.Style.LineStyle.color.string.replace_with(linecolor)        

    # Overwrite the KML file.
    with open(output_kml,"w") as fp:
        fp.write(str(soup))
    return

# =====================================================================
def shp2kml(l_layers):
    for l in l_layers:
        (infc, title, outkml, func, symbol) = l
        print("shp2kml for",title)
        func(infc, os.path.join(output_folder, outkml), symbol)
    return


def make_doc(l_layers):
    xmlpreamble = '<?xml version="1.0" encoding="UTF-8"?>\
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\
'
    netlink = '  <NetworkLink>\n        <name>%s</name>\n          <visibility>%d</visibility>\n          <Link><href>%s</href></Link>\n	</NetworkLink>\n'
    
    dockml = os.path.join(output_folder, 'doc.kml')
    input_files = [dockml,
                   os.path.join(output_folder,"solarpanel.png"),
                   os.path.join(output_folder,"transformer.png"),
                   ] # files to be zipped in final KMZ file
        
    with open(dockml,"w") as doc:
        print("Writing", dockml)
        doc.write(xmlpreamble)
        doc.write("<Folder>\n")
        doc.write('  <name>%s</name>\n  <open>1</open>\n' % doc_title)

        for l in l_layers:
            infc,title,kmlfile,func,sym = l
            kmlpath = output_folder + '/' + kmlfile
            doc.write('    ' + netlink % (title, 1, kmlpath))
            input_files.append(kmlpath)
        doc.write("</Folder>\n</kml>\n")
        
        doc.close()
    
    print("I must zip and rename")
    args = ['zip', output_folder + '.kmz', ] + input_files
    p = subprocess.check_output(args)

    return

# UNIT TESTING
# You can run this file directly when writing it to aid in debugging

if __name__ == '__main__':

    l_layers = [
        (soils,           "Soils",                 "soils.kml",                convert_polygons,       fix_soils),
        (subs_buffer,     "Substation buffers",    "subbuffer.kml",            convert_buffer_ring,  '80FFFFFF'), # grey ring
        (subs,            "Substations",           "substation.kml",           convert_point,        ''),
        (existing_buffer, "Existing site buffers", "existing_site_buffer.kml", convert_buffer_ring,  '8000FFFF'), # yellow ring
        (existing,        "Existing sites",        "existing_site.kml",        convert_point,        ''), # yellow point?
        (sites,           "Parcels",               "parcel.kml",               convert_polygons,       fix_sites),
#        (sites,           "Parcels",               "parcel_sizes.kml",        convert_polygons,       renamer_sizes),
        ]

    os.chdir(folder)
    print("working in", folder)

    #print("Not generating KML files")    
#    shp2kml([l_layers[0]])
    shp2kml(l_layers)
    
    # now merge the KML files into one.
    # They are all written to a folder
    # and all we need do is
    #   build a proper doc.kml
    #   zip
    #   and rename
    
#    make_doc(l_layers)
   
    print("All done!")

# That's all


