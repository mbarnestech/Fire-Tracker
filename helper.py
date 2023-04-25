""" file for helper functions """
from datetime import date
import crud


#---------------------------------------------------------------------#
# FIRE_DATA.PY

def create_decimal_latlong(latlong):
    """change coordinates from sexagesimal string format to decimal float format
    
    for use in instantiating Fire class, lat/long data from .kml file needs reformatting
    """
    neg, degrees, minutes, seconds = latlong
    
    # check for seconds
    if seconds:
        seconds = float(seconds)
    else:
        seconds = 0
        
    # create decimal latlong -> deg + min/60 + sec/3600
    decimal_latlong = int(degrees) + int(minutes)/60 + seconds/3600
    # if original latlong was negative, make decimal latlong negative as well
    if neg:
        decimal_latlong *= -1
    # return decimal version of latlong
    return decimal_latlong
    
def get_latlong_float(latlong):
    """turn latlong list into float"""
    neg, latlong_str, _ = latlong
    latlong_float = float(latlong_str)
    if neg:
        latlong_float *= -1
    return latlong_float

#---------------------------------------------------------------------#
# SERVER.PY

def get_maxmin_latlong(points):
    """get the maximum and minimum latitude and longitude of a trail
    
    points is a list of TrailPoint objects
    """

    # TODO try / except statement to make sure there are coords or 'if points'
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

def get_lnglat_list(points):
    """create a list of (longitude, latitude) tuples for a set of points"""
    lnglat_list = []
    for point in points:
        lnglat_list.append([point.longitude, point.latitude])
    return lnglat_list


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
    
def to_int(string_distance):
    """return distance as int; return 25 if not possible"""
    if string_distance.isdigit():
        return int(string_distance)
    return 25

#---------------------------------------------------------------------#
# SERVER.PY

# for updating fire table

def get_str_from_date(day):
    return day.strftime('%Y/%m/%d')

def get_today_str():
    return date.today().strftime('%Y/%m/%d')

def get_date_from_str(day):
    return date(int(day[:4]), int(day[5:7]), int(day[8:]))

def fires_are_old():
    current_day = date.today()
    old_day = get_date_from_str(crud.get_last_db_update())
    print(f'{current_day=}, {old_day=}')
    # difference in days
    difference = (current_day - old_day).days
    print(difference)
    if difference >= 1:
        return True
    return False

# for generating dictionaries for JS to fetch

def generate_index_dict():
    regions = [{'name': region.region_name, 'id': region.region_id} for region in crud.get_regions()]
    forests = [{'name': forest.forest_name, 'isEmpty': forest.is_forest_empty, 'id': forest.forest_id} for forest in crud.get_forests()]
    districts = [{'name': district.district_name, 'isEmpty': district.is_district_empty, 'id': district.district_id} for district in crud.get_districts()]
    trails = [{'name': trail.trail_name, 'isEmpty': trail.is_trail_empty, 'id': trail.trail_id} for trail in crud.get_trails()]

    return {'regions': regions, 'forests': forests, 'districts': districts, 'trails': trails}


def generate_region_dict(region_name):
    forests = [{'name': forest.forest_name, 'isEmpty': forest.is_forest_empty, 'id': forest.forest_id} for forest in crud.get_forests_by_region(region_name)]
    districts = [{'name': district.district_name, 'isEmpty': district.is_district_empty, 'id': district.district_id} for district in crud.get_districts_by_region(region_name)]
    trails = [{'name': trail.trail_name, 'isEmpty': trail.is_trail_empty, 'id': trail.trail_id} for trail in crud.get_trails_by_region(region_name)]

    return {'forests': forests, 'districts': districts, 'trails': trails}


def generate_forest_dict(forest_name):
    districts = [{'name': district.district_name, 'isEmpty': district.is_district_empty, 'id': district.district_id} for district in crud.get_districts_by_forest(forest_name)]
    trails = [{'name': trail.trail_name, 'isEmpty': trail.is_trail_empty, 'id': trail.trail_id} for trail in crud.get_trails_by_forest(forest_name)]
    print('GENERATING FOREST DICTIONARY YAYYYYYAYAYAYAYAYAYYA!')
    return {'districts': districts, 'trails': trails}


def generate_district_dict(district_name):
    trails = [{'name': trail.trail_name, 'isEmpty': trail.is_trail_empty, 'id': trail.trail_id} for trail in crud.get_trails_by_district(district_name)]

    return {'trails': trails}

