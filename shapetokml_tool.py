#!/usr/bin/env python

import arcpy
import shapetokml

class ShapeToKML_Tool(object):
    """This class has the methods you need to define
       to use your code as an ArcGIS Python Tool."""
        
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Shape To KML Tool"
        self.description = """Export a taxlot shapefile to kml."""
        self.canRunInBackground = False
        self.category = "Wildsong" # Use your own category here, or an existing one.
        #self.stylesheet = "" # I don't know how to use this yet.
        
    def getParameterInfo(self):
        """Define parameter definitions
           Refer to 
           http://desktop.arcgis.com/en/arcmap/latest/analyze/creating-tools/defining-parameter-data-types-in-a-python-toolbox.htm
        """
        
        # You can define a tool to have no parameters
        params = []
    
        # ..or you can define a parameter
        input_fc = arcpy.Parameter(name="parcel_fc",
                                   displayName="Parcel polygons",
                                   datatype="DEFeatureClass",
                                   parameterType="Required", # Required|Optional|Derived
                                   direction="Input", # Input|Output
                                   multiValue=False, # Allow entering many feature classes
                                )
        params.append(input_fc)
        
        output_kml = arcpy.Parameter(name="kml_file",
                                 displayName="KML output file",
                                 datatype="DEFile",
                                 parameterType="Required", # Required|Optional|Derived
                                 direction="Output", # Input|Output
                                )
        params.append(output_fc)

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of your tool."""
        
        # Let's dump out what we know here.
        messages.addMessage("Special merge starting up.")
        for param in parameters:
            messages.addMessage("Parameter: %s = %s" % (param.name, param.valueAsText) )
        
        # Get the parameters from our parameters list,
        # then call a generic python function.
        #
        # This separates the code doing the work from all
        # the crazy code required to talk to ArcGIS.
        
        # See http://desktop.arcgis.com/en/arcmap/latest/analyze/creating-tools/accessing-parameters-within-a-python-toolbox.htm
        in1       = parameters[0].valueAsText
        output_fc = parameters[1].valueAsText

        # Okay finally go ahead and do the work.
        shapetokml.convert_parcel(in1, output_fc)
        
        #shapetokml.convert_substation("sub.shp","sub.kml")
        #shapetokml.convert_buffer("buf.shp", "buf.kml")
        
        # wrap into one KMZ
        return

# That's all!
