### Hello, and welcome to my Fire Tracker project!

I love to play in the mountains, but where I live in the southwest I often need to check for fires before I head out for a hike. This app helps me choose a hike on US Forest Service lands and then lets me know if there are any fires nearby (with links to their inciweb information if there are). Further, this app lets me know the current AQI and weather at the trailhead, and I can choose an anticipated hiking date to get a weather forecast and historical weather data for that date.

### Features: 

- a decision tree to help user pick a FS Region, Forest, District, and Trail with corresponding maps
- a report of fires near the trail with both trailhead and fire locations listed on map
- the ability to choose how far from the trail to check for fires
- an AQI reading for the trailhead
- current and historical weather data for the trailhead
- option to get weather forecast and historical data for the trailhead on day of planned trip
- using the carousel navigation, option to go back and redirect search at any point in the decision tree

### Technologies: 

Python Libraries: bs4, csv, datetime, dotenv, flask, flask_sqlalchemy, geojson, jinja2, os, re,  requests, time

JS Library: Mapbox GL JS

APIs: Open Weather One Call API 3.0, Open Weather Air Pollution API

### Next features?

- user login with saved searches
- Twilio alert if a fire appears near a planned hike
- check for other things near the trail, like iNaturalist sightings
- get trails from non-forest service sources

### About the Author

Margaret Barnes developed this app as part of a software engineering fellowship with Hackbright Academy. You can learn more about her at https://www.linkedin.com/in/mbarnestech/