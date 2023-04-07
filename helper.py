""" file for helper functions """

import crud

def create_decimal_latlong(latlong):
    """change coordinates from sexagesimal string format to decimal float format
    
    for use in instantiating Fire class, lat/long data from .kml file needs reformatting
    """

    # remove whitespace before and after
    latlong.strip()
    # create string to move degrees to
    decimal_string = ''
    # set assumption of positive lat long
    neg = False
    # if lat long is negative
    if latlong[0] == '-':
        # set negative equal to true
        neg = True
        # remove first char, '-', from latlong string
        latlong = latlong[1:]
    # run while loop for first 2 or 3 numbers
    while latlong[0].isnumeric():
        # add the number to the decimal string
        decimal_string += latlong[0]
        # remove the number from the latlong string
        latlong = latlong[1:]
    # remove whitespace and . from latlong between degrees and minutes 
    while not latlong[0].isnumeric():
        latlong = latlong[1:]
    # change the decimal_string to a float
    decimal_latlong = float(decimal_string)
    # the next two numbers in latlong are the minutes - divide by 60 and add to the float
    decimal_latlong += float(latlong[:2]) / 60
    # remove the minute numbers from latlong
    latlong = latlong[2:]
    # all the remaining numbers are the seconds - divide by 3600 and add to the float
    decimal_latlong += float(latlong) / 3600
    # if latlong was negative, make float negative as well
    if neg == True:
        decimal_latlong *= -1
    # return decimal version of latlong
    return decimal_latlong


def get_maxmin_latlong(points):
    """get the maximum and minimum latitude and longitude of a trail
    
    points is a list of TrailPoint objects
    """
    max_lat = points[0].latitude
    min_lat = max_lat
    max_long = points[0].longitude
    min_long = max_long
    for point in points:
        max_lat = max(point.latitude, max_lat)
        min_lat = min(point.latitude, min_lat)
        max_long = max(point.longitude, max_long)
        min_long = min(point.longitude, min_long)
    return (min_lat, max_lat, min_long, max_long)


def get_fires():
    """return a list of all Fire objects"""
    return Fire.query.all()


def get_fire_search_boundaries(maxmin_latlong, miles):
    """return fire search boundaries """
    
    # use 1 deg latitude = 69 miles and 1 deg longitude = 54.6 miles to get radius in lat/long
        # this is math based on numbers from 38 deg North latitude, which I'm calling close enough for my purposes here
    lat_offset = miles/69
    long_offset = miles/54.6
    
    #unpack maxmin_latlong
    min_lat, max_lat, min_long, max_long = maxmin_latlong
    
    # create min/max lat/long boundaries for fire search
    min_lat -= lat_offset
    max_lat += lat_offset
    min_long -= long_offset
    max_long += long_offset

    return (min_lat, max_lat, min_long, max_long)


def get_nearby_fires(trailpoint_list, miles):
    """get list of Fire instances for fires within requested miles of trail"""

    # get maximum and minimum latitude and longitude of the trail
    maxmin_latlong = get_maxmin_latlong(trailpoint_list)
    # get maximum and minimum latitude and longitude for fire search
    min_lat, max_lat, min_long, max_long = get_fire_search_boundaries(maxmin_latlong, miles)
    # create empty nearby_fires list
    nearby_fires = []
    # get list of fires
    fires = crud.get_fires()
    # loop through known fires
    for fire in fires:
        # if fire is within boundaries
        if min_lat < fire.latitude < max_lat and min_long < fire.longitude < max_long:
            # add fire object to list
            nearby_fires.append(fire)
    # return list of Fire instances
    return nearby_fires
    

    