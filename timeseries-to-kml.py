# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 18:44:14 2020

@author: Jordi Bolibar

Converting arrrays with time series into multiple KML files in order to produce
animations. 

"""

## Dependencies: ##
from pykml import parser
from lxml import etree

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import os
import ast

######   FILE PATHS    #######
workspace = str(Path(os.getcwd())) + '\\'
path_glims = workspace + 'glacier_data\\GLIMS\\' 
path_smb = workspace + 'glacier_data\\smb\\'
path_glacier_evolution = workspace + 'glacier_data\\glacier_evolution\\'
path_glacier_volume = path_glacier_evolution + 'glacier_volume\\'

path_base_kml_sample = workspace + 'kml\\'
path_annual_ice_cubes = workspace + 'kml\\annual_ice_cubes\\'


#######################    FUNCTIONS    ##########################################################

def update_coordinates(base_file, new_altitude):
    
    base_sample_coordinates = base_file.getroot().Document.Placemark.Polygon.outerBoundaryIs.LinearRing.coordinates
    
    ### convert the co-ordinate to text and delimiters become ordinary text (i.e. repr)
    coordinates_text  =  repr(base_sample_coordinates.text)
    header = coordinates_text[:15]
    tail = coordinates_text[-14:]
    
    # ## Split the text (identifying the delimters)
    coordinates_split_before = coordinates_text.split("\\t")[6]
    coordinates_split = coordinates_split_before.split(",")
    
    coordinates_split[2] = str(new_altitude) + " " + coordinates_split[2].split(" ")[1]
    coordinates_split[4] = str(new_altitude) + " " + coordinates_split[4].split(" ")[1]
    coordinates_split[6] = str(new_altitude) + " " + coordinates_split[6].split(" ")[1]
    coordinates_split[8] = str(new_altitude) + " " + coordinates_split[8].split(" ")[1]
    coordinates_split[-1] = str(new_altitude) 
    
    counter = 0
    string_updated_coordinates = header
    for coordinate in coordinates_split:
        if(counter != (len(coordinates_split)-1)):
            string_updated_coordinates = string_updated_coordinates + coordinate + ","
        else:
            string_updated_coordinates = string_updated_coordinates + coordinate + tail
        
        counter=counter+1
        
#    print("\noriginal coordinates: " + str(coordinates_text))
#       
#    print("\nupdated coordinates: " + string_updated_coordinates)
    
    updated_coordinates = ast.literal_eval(string_updated_coordinates)
    
    # # Store Updated Coordinates into original coordinates location
    base_file.getroot().Document.Placemark.Polygon.outerBoundaryIs.LinearRing.coordinates = updated_coordinates
    
    return base_file
                            
##################################################################################################


###############################################################################
###                           MAIN                                          ###
###############################################################################

# Read the baseline cube to update with the glacier data
base_kml_file= path_base_kml_sample + 'glacier_cube_sample.kml'
with open(base_kml_file) as f:
#    folder = parser.parse(f).getroot().Document.Folder
    base_file = parser.parse(f)
    
base_file_str = etree.tostring(base_file, pretty_print=True).decode('utf-8')

altitudes = range(5, 1000, 80)
years = range(2019, 2100)

# We create new ice cube KML files for every year's ice altitude
for current_altitude, year in zip(altitudes, years):
    updated_kml = update_coordinates(base_file, current_altitude)
    
    # Output a KML file (named based on the Python script)
    outfile = open(path_annual_ice_cubes + 'ice_cube_alt_' + str(current_altitude) + '_' + str(year) + '.kml','w')
    outfile.write(etree.tostring(updated_kml, pretty_print=True).decode('utf-8'))
    outfile.close()
    
