""" file for helper functions """
from datetime import date
import crud
from os import environ
import requests
import re


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
    neg, latlong_str, dir = latlong
    latlong_float = float(latlong_str)
    if neg or (dir and dir == 'W' or dir == 'S'):
        latlong_float *= -1

    return latlong_float

#---------------------------------------------------------------------#
# SERVER.PY

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

def get_lnglat_tuples(points):
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
    trails = [{'name': trail.trail_name, 'no': trail.trail_no, 'isEmpty': trail.is_trail_empty, 'id': trail.trail_id} for trail in crud.get_trails()]
    mapKey = environ['DEFAULTMAPBOXTOKEN']

    return {'regions': regions, 'forests': forests, 'districts': districts, 'trails': trails, 'mapKey': mapKey}


def generate_region_dict(region_id):
    region = crud.get_region_by_region(region_id)
    starting_lnglat = [region.long, region.lat]
    forests = [{'name': forest.forest_name, 'isEmpty': forest.is_forest_empty, 'id': forest.forest_id} for forest in crud.get_forests_by_region(region_id)]
    districts = [{'name': district.district_name, 'isEmpty': district.is_district_empty, 'id': district.district_id} for district in crud.get_districts_by_region(region_id)]
    trails = [{'name': trail.trail_name, 'no': trail.trail_no, 'isEmpty': trail.is_trail_empty, 'id': trail.trail_id} for trail in crud.get_trails_by_region(region_id)]

    return {'forests': forests, 'districts': districts, 'trails': trails, 'startingLngLat': starting_lnglat}


def generate_forest_dict(forest_id):
    districts = [{'name': district.district_name, 'isEmpty': district.is_district_empty, 'id': district.district_id} for district in crud.get_districts_by_forest(forest_id)]
    trails = [{'name': trail.trail_name, 'no': trail.trail_no, 'isEmpty': trail.is_trail_empty, 'id': trail.trail_id} for trail in crud.get_trails_by_forest(forest_id)]
    return {'districts': districts, 'trails': trails}


def generate_district_dict(district_id):
    trails = [{'name': trail.trail_name, 'no': trail.trail_no, 'isEmpty': trail.is_trail_empty, 'id': trail.trail_id} for trail in crud.get_trails_by_district(district_id)]

    return {'trails': trails}

def generate_trail_dict(trail_id):
    trail_name = crud.get_trail_name_with_trail_id(trail_id)
    trailpoint_list = crud.get_trailpoint_list_with_trail_id(trail_id)
    trailhead = [trailpoint_list[0].longitude, trailpoint_list[0].latitude]
    nearby_fires = get_nearby_fires(trailpoint_list, 25)
    fires = [{'id': fire.fire_id, 'name': fire.fire_name, 'url': fire.fire_url, 'longitude': fire.longitude, 'latitude': fire.latitude} for fire in nearby_fires]

    return {'fires': fires, 'trail_name': trail_name, 'trailhead': trailhead}

# for updating tables
def get_lnglat_for_place(place):
    "given a city or forest unit, get LngLat"

    place_string = place + ' coordinates'
    response = requests.get(f'https://www.google.com/search?q={place_string}')
    html_string = response.text
    result = re.search(r"(?P<Nneg>-)?(?P<Ndegrees>\d+\.\d+).{1,2}? ?(?P<Ndir>N?S?),? (?P<Wneg>-)?(?P<Wdegrees>\d+\.\d+).{1,2}? ?(?P<Wdir>E?W?)", html_string)
    if result:
        print('yay')
        print(f"{result.group('Nneg')=}, {result.group('Wneg')=}, {result.group('Ndegrees')=}, {result.group('Wdegrees')=}, {result.group('Ndir')=}, {result.group('Wdir')=}")
        lat = get_latlong_float([result.group('Nneg'), result.group('Ndegrees'), result.group('Ndir')])
        lng = get_latlong_float([result.group('Wneg'), result.group('Wdegrees'), result.group('Wdir')])
        return [lng, lat]
    result = re.search(r"(?P<Nneg>-)?(?P<Ndegrees>\d{2,3} ?)\°(?P<Nminutes>\d{1,2})\′(?P<Nseconds>\d*\.?\d*)?\″?N?S? (?P<Wneg>-)?(?P<Wdegrees>\d{2,3} ?)\°(?P<Wminutes>\d{1,2})\′(?P<Wseconds>\d*\.?\d*)?", html_string) 
    if result:
        print('also yay!')
        lat = create_decimal_latlong([result.group('Nneg'), result.group('Ndegrees'), result.group('Nminutes'), result.group('Nseconds') ])
        lng = create_decimal_latlong([result.group('Wneg'), result.group('Wdegrees'), result.group('Wminutes'), result.group('Wseconds') ])
        return [lng, lat]
    print('********** COULD NOT FIND COORDINATES **********')

