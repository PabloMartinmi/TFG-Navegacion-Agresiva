from math import cos, sin, radians, pi

def ellipse_size(ship_l, lon, lat, speed, r, heading):
    """
    Based on the image where:
    - a = 4 times ship length (semi-major axis)
    - b = 1.6 times ship length (semi-minor axis)  
    - c = 0.25 times semi-major axis (distance from the center to the given point)
    
    Approximation of degrees to metres:
    - 1 degree of latitude ≈ 111,111 meters
    - 1 degree of longitude ≈ 111,111 * cos(latitude) meters

    Note:
    - The ship heading is measured in degrees (0° = North, 90° = East)
    """
    
    # Latitude:
    M_PER_DG_LAT = 111111.0
    # Longitude:
    m_per_dg_lon = M_PER_DG_LAT * cos(radians(lat))

    
    # Ellipse semi-axes (m)
    a_m = 1.5 * 4 * ship_l  # semi-major axis 
    b_m = 1.5 * 1.6 * ship_l  # semi-minor axis 
    c_m = 0.4 * a_m 
    
    # semi-axes (m) to degrees
    a_dg_lat = a_m / M_PER_DG_LAT
    b_dg_lat = b_m / M_PER_DG_LAT
    a_dg_lon = a_m / m_per_dg_lon
    b_dg_lon = b_m / m_per_dg_lon
    

    # Rotated ellipse:
    lx = 2 * max(a_dg_lat, a_dg_lon)  # full major axis in degrees
    ly = 2 * min(b_dg_lat, b_dg_lon)  # full minor axis in degrees
    
    # heading to radians (nautical heading: 0° = North, clockwise)
    heading_rad = radians(heading)

    # Calculate the center offset in meters:
    c_offset_x_m = -c_m * sin(heading_rad)  # East-West component
    c_offset_y_m = -c_m * cos(heading_rad)  # North-South component
    
    # Convert offsets from meters to degrees
    c_offset_lon = c_offset_x_m / m_per_dg_lon
    c_offset_lat = c_offset_y_m / M_PER_DG_LAT
    
    # Ellipse center position in geographic coordinates
    pos_c_x = lon - c_offset_lon
    pos_c_y = lat - c_offset_lat

    
    return lx, ly, lon, lat, pos_c_x, pos_c_y