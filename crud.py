# import Python modules
from datetime import datetime

# import local modules
from model import Trail, TrailPoint, Fire, connect_to_db, db

# CRUD functions

# helper functions
def create_decimal_latlong(latlong):
    """change coordinates from sexagesimal string format to decimal float format"""

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

# functions to create class instances
def create_trail(trail_name, hp_id, state, area, city):
    """Create and return a new trail."""
    return Trail(trail_name=trail_name, hp_id=hp_id, state=state, area=area, city=city)


def create_trail_point(trail, latitude, longitude):
    """Create and return a new trail point"""
    return TrailPoint(trail=trail, latitude=latitude, longitude=longitude)


def create_fire(fire_url, fire_name, latitude, longitude, incident_type, last_updated, size, contained):
    """Create and return a new fire."""

    decimal_latitude = create_decimal_latlong(latitude)
    decimal_longitude = create_decimal_latlong(longitude)

    return Fire(fire_url=fire_url, fire_name=fire_name, latitude=decimal_latitude, longitude=decimal_longitude, incident_type=incident_type, last_updated=last_updated, size=size, contained=contained)


# Connect to database when running crud.py interactively
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
