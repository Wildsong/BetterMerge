#!/usr/bin/env python

import arcpy
import special_merge

class Special_Merge_Tool(object):
    """This class has the methods you need to define
       to use your code as an ArcGIS Python Tool."""
        
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Special_Merge Tool"
        self.description = """Wrapper for Merge that captures some of the merge tool as python code."""
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
        input_fc1 = arcpy.Parameter(name="marion_fc",
                                   displayName="Marion county taxlots",
                                   datatype="DEFeatureClass",
                                   parameterType="Required", # Required|Optional|Derived
                                   direction="Input", # Input|Output
                                   multiValue=False, # Allow entering many feature classes
                                )
        input_fc2 = arcpy.Parameter(name="rlis_fc",
                                   displayName="Metro RLIS county taxlots",
                                   datatype="DEFeatureClass",
                                   parameterType="Required", # Required|Optional|Derived
                                   direction="Input", # Input|Output
                                   multiValue=False, # Allow entering many feature classes
                                )

        params.append(input_fc1)
        params.append(input_fc2)
        
        output_fc = arcpy.Parameter(name="merged_fc",
                                 displayName="Merged output feature class",
                                 datatype="DEFeatureClass",
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
        in1  = parameters[0].valueAsText
        in2  = parameters[1].valueAsText
        output_fc = parameters[2].valueAsText
        # Okay finally go ahead and do the work.
        special_merge.merge(in1, in2, output_fc)

        return

# That's all!
