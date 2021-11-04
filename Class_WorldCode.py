import arcpy
import time
import os
import sys
import shutil

start = time.time()

arcpy.env.overwriteOutput = True


def count_and_display(item):
    desc = arcpy.Describe(item)
    cnt = arcpy.GetCount_management(item)
    print(f"{desc.name} is a {desc.shapeType} with {cnt} records.")


def main():

    base_folder = r"C:\GISc450\ArcPy7_tool"

    data_folder = os.path.join(base_folder, "World")

    arcpy.env.workspace = base_folder

    globe_cities = os.path.join(data_folder, "Cities.shp")
    globe_lakes = os.path.join(data_folder, "Lakes.shp")
    globe_rivers = os.path.join(data_folder, "Rivers.shp")
    globe_country = os.path.join(data_folder, "Country.shp")

    country_to_extract = "Canada"
    cntry = "Canada.shp"
    cntry_city = f"{country_to_extract}_cities"
    cntry_rivers = f"{country_to_extract}_rivers"
    cntry_lakes = f"{country_to_extract}_lakes"


    #sql_phrase = f"CNTRY_NAME = '{cntry}'"    # this was yours.......
    #
    # THis is mine
    sql_phrase = f""" "CNTRY_NAME" = \'{country_to_extract}\' """

    gdb_name = f"My_Canada.gdb"

    gdb_path = os.path.join(base_folder, gdb_name)
    print((gdb_path))

    if arcpy.Exists(gdb_path):
        shutil.rmtree(gdb_path)

    arcpy.CreateFileGDB_management(base_folder, gdb_name)

    arcpy.env.workspace = gdb = gdb_path

    coord = arcpy.SpatialReference(102002)
    arcpy.env.outputCoordinateSystem = coord


    select_country = arcpy.SelectLayerByAttribute_management(globe_country, "NEW_SELECTION", sql_phrase, None)
    cntry_country = arcpy.FeatureClassToFeatureClass_conversion(select_country, gdb_path, country_to_extract)
    arcpy.Delete_management(select_country)

    select_cities = arcpy.SelectLayerByLocation_management(globe_cities, "WITHIN", cntry_country
                                                           , None, "NEW_SELECTION", "NOT_INVERT")
    arcpy.FeatureClassToFeatureClass_conversion(select_cities, gdb_path, cntry_city)
    arcpy.Delete_management(select_cities)

    arcpy.analysis.Clip(globe_lakes,cntry_country, cntry_lakes)
    #arcpy.FeatureClassToGeodatabase_conversion(clip_lakes, gdb)
    #arcpy.Delete_management(clip_lakes)

    arcpy.analysis.Clip(globe_rivers, cntry_country, cntry_rivers)
    # cntry_rivers = arcpy.FeatureClassToGeodatabase_conversion(clip_rivers, gdb)
    # arcpy.Delete_management(clip_rivers)

    fc_list = arcpy.ListFeatureClasses()

    for fc in fc_list:
        fc_info = os.path.join(gdb_path, fc)
        count_and_display(fc_info)   # need full path here


if __name__ == '__main__':
    main()
    end = time.time()
    total_time = end - start
    minutes = round(total_time / 60)
    seconds = round(total_time % 60, 2)
    print(f"This script took {minutes} minutes and {seconds} seconds")
    sys.exit()
