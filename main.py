import datetime
import json

# Scripts
from sql_request import sql_request
from test_collisions import check_collisions


# Config values
with open('config.json', 'r') as f:
    config = json.load(f)

init_date = datetime.datetime.strptime(config['init_date'], "%Y-%m-%d %H:%M:%S")
end_date = datetime.datetime.strptime(config['end_date'], "%Y-%m-%d %H:%M:%S")
time_range = config['time_range']
ell_factor = config['ell_factor']
min_vel = config['min_vel']

# Query the db with the parameters introduced by the user
query = sql_request(init_date, end_date, time_range, min_vel)

# Execute the script that calculates collisions
check_collisions(query, min_vel, ell_factor) 

# To run map:
# python map.py "2020-01-01_13-45-00_2020-01-01_14-15-00_15.txt"
