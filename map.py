import tkinter as tk
from tkintermapview import TkinterMapView
import mysql.connector
from datetime import datetime
import math
from matplotlib.patches import Ellipse
import argparse
import numpy as np

def get_db(start_date, end_date):
    query = f"""
            SELECT mmsi, latitude, longitude, length, course FROM navegacion.trafico
            WHERE (timestamp BETWEEN '{start_date}' AND '{end_date}') AND width <> 0.0 AND length <> 0 AND speed > 0
            ORDER BY timestamp
        """
    # DB connection
    connection = mysql.connector.connect(
        host="navegacion.ucavila.es",
        user="naveg_root",
        passwd="UCAV&UCLMtfg2023",
        db="navegacion")
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

def rotate_point(point, angle, center):
    """
    Rotates a point around a given center by an angle.
    - param point: Point coordinates (x, y)
    - param angle: Rotation angle in degrees
    - param center: Rotation center (x_c, y_c)
    return: New point coordinates
    """
    x, y = point
    cx, cy = center
    angle_rad = np.radians(angle)

    # Rotation matrix
    x_rotated = cx + np.cos(angle_rad) * (x - cx) - np.sin(angle_rad) * (y - cy)
    y_rotated = cy + np.sin(angle_rad) * (x - cx) + np.cos(angle_rad) * (y - cy)
    return x_rotated, y_rotated

def print_map(map_widget, data, collision):
    for vessel in data:
        mmsi = vessel[0]
        latitude = vessel[1]
        longitude = vessel[2]
        length = vessel[3]
        course = vessel[4]

        # Approach for precision:
        # https://en.wikipedia.org/wiki/Decimal_degrees
        length_factor = 0.00001 * length
        width_factor = 0.000005 * length

        vertices = [[latitude+(length_factor*2), longitude], [latitude-width_factor, longitude-width_factor], [latitude-width_factor, longitude+width_factor]]
        center = (latitude,longitude)

        # Rotated according to direction
        # cos_val = math.cos(course)
        # sin_val = math.sin(course)
        # cx, cy = center
        new_points = [rotate_point(point, course, center) for point in vertices]

        color = "blue"
        if mmsi in collision:
            color = "red"
            col = collision.get(mmsi)
            # Only collision ellipses
            print(col)
            print(f"---------> {course}")
            ellipse = Ellipse((float(col[2]), float(col[3])), float(col[4]), float(col[5]), angle=course)
            map_widget.set_polygon(ellipse.get_verts(),
                                   fill_color="",
                                   outline_color=color,
                                   border_width=1)
        # Vessels
        map_widget.set_polygon(new_points,
                                    fill_color=color,
                                    outline_color=color,
                                    border_width=1)

def gui_start():
    root = tk.Tk()
    root.state('zoomed')

    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)

    # Interactive map
    map_widget = TkinterMapView(frame)
    map_widget.pack(fill='both', expand=True)
    map_widget.set_position(40, -10)  # Centered map
    map_widget.set_zoom(7)  # Initial zoom

    # Bottom bar
    bottom_bar = tk.Frame(root, height=30, bg="#f0f0f0")
    bottom_bar.pack(fill='x', side='bottom')
    coords_label = tk.Label(bottom_bar, text="Lat: --, Lng: --", anchor='e', padx=10)
    coords_label.pack(fill='both', expand=True)

    def update_coordinates(coords):
        # Get mouse coordinates on the map
        latitude = coords[0]   #round(coords[0], 5)
        longitude = coords[1]  #round(coords[1], 5)
        coords_label.config(text=f"Lat: {latitude}, Lng: {longitude}")
    map_widget.add_left_click_map_command(update_coordinates)

    return root, map_widget

def get_dates(line):
    elements = line.split(';')
    format = "%Y-%m-%d %H:%M:%S"  # Specifies the format
    start_date = datetime.strptime(elements[0], format)
    end_date = datetime.strptime(elements[1], format)
    return start_date, end_date

def collision_vessels(line):
    elements = line.split(';')
    vessel1 = (
        elements[0],    # mmsi
        elements[1],    # timestamp
        elements[2],    # center_x
        elements[3],    # center_y
        elements[4],    # semi_major_axis
        elements[5],    # semi_minor_axis
        elements[6],    # angle
    )
    vessel2 = (
        elements[7],    # mmsi
        elements[8],    # timestamp
        elements[9],    # center_x
        elements[10],    # center_y
        elements[11],    # semi_major_axis
        elements[12],    # semi_minor_axis
        elements[13],    # angle
    )
    return vessel1, vessel2

def read_file(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            line_num = 0
            collision = {}
            for line in f:
                if line_num > 1:       # Collisions description
                    vessel1, vessel2 = collision_vessels(line.strip())
                    if vessel1[0] not in collision:
                        collision[vessel1[0]] = vessel1
                    if vessel2[0] not in collision:
                        collision[vessel2[0]] = vessel2
                if line_num == 0:       # Line with general description
                    start_date, end_date = get_dates(line.strip())
                    vessels = get_db(start_date, end_date)
                line_num = line_num + 1
            return vessels, collision
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
    except IOError:
        print(f"Error: Not access for reading file '{file}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help="File name")
    args = parser.parse_args()

    print(f'Reading {args.file} and extracting context data from DB...')
    vessels, collision = read_file(args.file)
    root, map_widget = gui_start()
    print_map(map_widget, vessels, collision)

    root.mainloop()
