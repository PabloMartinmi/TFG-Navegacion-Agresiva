import mysql.connector
import datetime
from dateutil.rrule import rrule, MINUTELY


# DB connection
connection = mysql.connector.connect(
    host="navegacion.ucavila.es",
    user="naveg_root",
    passwd="UCAV&UCLMtfg2023",
    db="navegacion")


cursor = connection.cursor()


def sql_request(init_date, end_date, time_range, min_vel):
    results = {}

    for date in rrule(freq=MINUTELY, dtstart=init_date, until=end_date, interval=30):

        # Set file name for each iteration (time window)
        start_interval_date = date - datetime.timedelta(minutes=time_range)
        end_interval_date = date + datetime.timedelta(minutes=time_range)
            
        # Query set with the time window
        query = f"""
            SELECT * FROM navegacion.trafico
            WHERE (timestamp BETWEEN '{start_interval_date}' AND '{end_interval_date}') AND width <> 0.0 AND length <> 0 AND speed > {min_vel}
            ORDER BY timestamp
        """
        cursor.execute(query)
        db_query = cursor.fetchall()

        ais_data = []
        
        for i in db_query:
            # mmsi, timestamp, draught, length, width, latitude, longitude, speed, heading 
            mmsi = str(i[0])  
            timestamp = i[1] 
            types = [(float, 0.0), (int, 0), (int, 0), (float, 0.0), (float, 0.0), (float, 0.0), (float, 0.0)]
            speed, course, heading, latitude, longitude, speed_over_ground, angle = [
                t(value) if value is not None else default for value, (t, default) in zip(i[2:9], types)] # Empty data is removed
            
            t = (mmsi, 
                datetime.datetime(
                    timestamp.year, timestamp.month, timestamp.day, 
                    timestamp.hour, timestamp.minute, timestamp.second
                ), 
                speed, course, heading, latitude, longitude, speed_over_ground, angle)

            ais_data.append(t)

        key = (
            start_interval_date, 
            end_interval_date,
            time_range
        )
        results[key] = ais_data

    connection.close()
    return results