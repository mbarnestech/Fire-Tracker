""" file for helper functions """

# import Python modules
import datetime
from dotenv import load_dotenv
from os import environ
import re
import requests
import time
from flask import Flask, render_template, session, request, jsonify


# import local modules
import crud

load_dotenv()


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

def get_lnglat_tuples(points):
    """create a list of (longitude, latitude) tuples for a set of points"""
    lnglat_list = []
    for point in points:
        lnglat_list.append([point.longitude, point.latitude])
    return lnglat_list


def get_fire_search_boundaries(lnglat, miles):
    """return fire search boundaries """
    
    # use 1 deg latitude = 69 miles and 1 deg longitude = 54.6 miles to get radius in lat/long
        # this is math based on numbers from 38 deg North latitude, which I'm calling close enough for my purposes here
    lat_offset = miles/69
    long_offset = miles/54.6
    #unpack maxmin_latlong
    long, lat = lnglat
    
    # create min/max lat/long boundaries for fire search
    min_lat = lat - lat_offset
    max_lat = lat + lat_offset
    min_long = long - long_offset
    max_long = long + long_offset

    return (min_lat, max_lat, min_long, max_long)

def get_nearby_fires(lnglat, distance):
    min_lat, max_lat, min_long, max_long = get_fire_search_boundaries(lnglat, distance)
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
    return datetime.date.today().strftime('%Y/%m/%d')

def get_date_from_str(day):
    return datetime.date(int(day[:4]), int(day[5:7]), int(day[8:]))

def fires_are_old():
    current_day = datetime.date.today()
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

def generate_trail_dict(trail_id, openweatherkey, distance='25'):
    int_distance = int(distance)
    trail = crud.get_trail_with_trail_id(trail_id)
    trail_name = trail.trail_name
    trailhead = [trail.th_long, trail.th_lat]
    nearby_fires = get_nearby_fires(trailhead, int_distance)
    fires = [{'id': fire.fire_id, 'name': fire.fire_name, 'url': fire.fire_url, 'longitude': fire.longitude, 'latitude': fire.latitude} for fire in nearby_fires]
    aqi = get_aqi_info(trailhead, openweatherkey)
    print(f'##### aqi = {aqi}')
    weather_info = get_weather_info(trailhead, openweatherkey)
    print(f'%%%%% weather = {weather_info}')

    return {'fires': fires, 'trail_name': trail_name, 'trailhead': trailhead, 'aqi': aqi, 'weather_info': weather_info}

# , 'weather_info': weather_info

# for updating tables
def get_lnglat_for_place(place):
    "given a city or forest unit, get LngLat"

    place_string = place + ' coordinates'
    response = requests.get(f'https://www.google.com/search?q={place_string}')
    html_string = response.text
    result = re.search(r"(?P<Nneg>-)?(?P<Ndegrees>\d+\.\d+).{1,2}?°? ?(?P<Ndir>\(North\)|\(South\)|N|S?)?.? ?(?P<Wneg>-)?(?P<Wdegrees>\d+\.\d+).{1,2}?°? ?(?P<Wdir>E|W|\(East\)|\(West\)?)", html_string)
    if result:
        # print('yay')
        # print(f"{result.group('Nneg')=}, {result.group('Wneg')=}, {result.group('Ndegrees')=}, {result.group('Wdegrees')=}, {result.group('Ndir')=}, {result.group('Wdir')=}")
        lat = get_latlong_float([result.group('Nneg'), result.group('Ndegrees'), result.group('Ndir')])
        lng = get_latlong_float([result.group('Wneg'), result.group('Wdegrees'), result.group('Wdir')])
        return [lng, lat]
    result = re.search(r"(?P<Nneg>-)?(?P<Ndegrees>\d{2,3})\°(?P<Nminutes>\d{1,2})(′|(&#8242;))?(?P<Nseconds>\d+\.?\d*)?(″|(&#8243;))(?P<Ndir>\(North\)|\(South\)|N|S)? ?(?P<Wneg>-)?(?P<Wdegrees>\d{2,3})\°(?P<Wminutes>\d{1,2})(′|(&#8242;))(?P<Wseconds>\d+\.?\d*)?(″|(&#8243\;))(?P<Wdir>E|W|\(East\)|\(West\))?", html_string) 
    if result:
        print('also yay!')
        print(f'{result.group()=}')
        print(f"{result.group('Nneg')=}, {result.group('Wneg')=}, {result.group('Ndegrees')=}, {result.group('Wdegrees')=}, {result.group('Ndir')=}, {result.group('Wdir')=}")
        neg = False
        if result.group('Wdir') and result.group('Wneg') == None:
            if result.group('Wdir') == 'W' or result.group('Wdir') == 'West':
                neg = True
        if result.group('Wneg'):
            neg = True
        lat = create_decimal_latlong([result.group('Nneg'), result.group('Ndegrees'), result.group('Nminutes'), result.group('Nseconds') ])
        lng = create_decimal_latlong([neg, result.group('Wdegrees'), result.group('Wminutes'), result.group('Wseconds') ])
        return [lng, lat]
        
    print('********** COULD NOT FIND COORDINATES **********')


def get_aqi_info(lnglat, openweatherkey):
    long, lat = lnglat
    response = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={long}&appid={openweatherkey}')
    print(response)
    json_info = response.json()
    print(json_info)
    aqi = json_info['list'][0]['main']['aqi']
    print(f'********{aqi}*******')
    return aqi

def get_weather_info(lnglat, openweatherkey, date = datetime.date.today()):
    long, lat = lnglat
    today = time.mktime(datetime.date.today().timetuple())
    date_given = time.mktime(date.timetuple())
    date_diff = int((date_given - today)/ 86400)
    weather_info = {}
    if 0 <= date_diff <= 8:
        response = requests.get(f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={long}&exclude=current,minutely,hourly&units=imperial&appid={openweatherkey}')
        current_weather = response.json()
        weather = current_weather['daily'][date_diff]
        weather_info['current'] = {'high': weather['temp']['max'], 'low': weather['temp']['min'], 'humidity': weather['humidity'], 'wind_speed': weather['wind_speed'], 'description': weather['weather'][0]['description']}
    temp = 0 
    humidity = 0
    wind_speed = 0 
    description = []
    month = int(date.strftime('%m'))
    day = int(date.strftime('%d'))
    for yr in range(2018, 2023):
        print(yr)
        date_given_2022 = int(time.mktime(datetime.date(yr, month, day).timetuple()))
        historic_response = requests.get(f'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={long}&dt={date_given_2022}&units=imperial&appid={openweatherkey}')
        historic_weather = historic_response.json()
        print(f'*****${historic_weather}')
        historic = historic_weather['data'][0]
        temp += historic['temp'] 
        humidity += historic['humidity']
        wind_speed += historic['wind_speed']
        description.append(historic['weather'][0]['description'])
    weather_info['historic'] = {'temp': temp/5, 'humidity': humidity/5, 'wind_speed': wind_speed/5, 'description': list(set(description))}
    return weather_info

def get_today():
    return datetime.date.today().strftime('%Y-%m-%d')

def get_next_year():
    today = datetime.date.today()
    next_year = today.replace(year = today.year + 1)
    return next_year.strftime('%Y-%m-%d')

def get_weather_dict(date, trail_id, openweatherkey):
    dt_date = get_date_from_str(date)
    trail = crud.get_trail_with_trail_id(trail_id)
    lnglat = [trail.th_long, trail.th_lat]
    weather = get_weather_info(lnglat, openweatherkey, dt_date)
    return weather