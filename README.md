A simple program to generate a weather report across a longer drive.

It uses:
* Nomatim for geosearching
* openrouteservice.org for routing
* tomorrow.io for weather report


# How to run server

## Install dependencies
```
pip install -r requirements.txt
```

## Set up API keys

Create `.env` file containing:
```
ORS_API_KEY="<ORS_API_KEY>"
TOMORROW_API_KEY="<TOMORROW_API_KEY>"
```
Get ORS_API_KEY from https://account.heigit.org/manage/key
Get TOMORROW_API_KEY from https://app.tomorrow.io


## Run server
```
uvicorn main:app --reload
```

# Supported requests
```
GET("/route-weather")
    origin: str 
    destination: strn
    departure_time: datetime 
```
`origin` - starting point

`destination` - destination point

`departure_time` - the departure time


# Example

`test_and_draw_route.py` contains an example client that queries the server and draws a map in html