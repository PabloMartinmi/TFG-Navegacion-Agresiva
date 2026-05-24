import numpy as np
from ellipse_size import ellipse_size
from itertools import combinations


def compute_ellipse_matrix(a, b, theta):
    theta_rad = np.radians(theta)
    R = np.array([[np.cos(theta_rad), -np.sin(theta_rad)],
                  [np.sin(theta_rad),  np.cos(theta_rad)]])  # Rotation matrix
    D = np.diag([1/a**2, 1/b**2])
    A = R.T @ D @ R  # ellipse in matrix form
    
    return A

def is_center_inside_ellipse(A, center, point):
    # Checks if the point is inside the ellipse
    diff = np.array(point) - np.array(center)
    value = diff.T @ A @ diff

    return value <= 1

def check_centers_inside_each_other(ellipse1, ellipse2):
    a1, b1, h1, k1, theta1 = ellipse1
    a2, b2, h2, k2, theta2 = ellipse2

    A1 = compute_ellipse_matrix(a1, b1, theta1)  # Vessel 1 ellipse
    A2 = compute_ellipse_matrix(a2, b2, theta2)  # Vessel 2 ellipse

    center1_in_ellipse2 = is_center_inside_ellipse(A2, [h2, k2], [h1, k1])
    center2_in_ellipse1 = is_center_inside_ellipse(A1, [h1, k1], [h2, k2])

    return center1_in_ellipse2, center2_in_ellipse1



def check_collisions(query, min_vel, ell_factor):

    for key, ais_data in query.items():

        title = f"{key[0].strftime('%Y-%m-%d_%H-%M-%S')}_{key[1].strftime('%Y-%m-%d_%H-%M-%S')}_{key[2]}"
        file_name = f"{title}.txt"

        # RESULTS CALCULATION
        with open(file_name, 'w', encoding='utf-8') as result:
            result.write(f"{key[0]};{key[1]};{key[2]}\n")
            result.write("mmsi1;timestamp1;x1,y1;semi_major_axis1;semi_minor_axis1;ang1;mmsi2;timestamp2;x2,y2;semi_major_axis2;semi_minor_axis2;ang2;collision\n")

            for i, j in combinations(range(len(ais_data)), 2):

                # mmsi, timestamp, draught, length, width, latitude, longitude, speed, heading 
                mmsi_1, timestamp1, _, length1, _, center_x1, center_y1, vel_1, ang1 = ais_data[i]
                mmsi_2, timestamp2, _, length2, _, center_x2, center_y2, vel_2, ang2 = ais_data[j]

                # Create ellipses in matrix form, according to Hansen proportions
                semi_major_axis1, semi_minor_axis1, center_x1, center_y1, center_xe_1, center_ye_1 = ellipse_size(length1, center_x1, center_y1, vel_1, ell_factor, ang1)
                semi_major_axis2, semi_minor_axis2, center_x2, center_y2, center_xe_2, center_ye_2 = ellipse_size(length2, center_x2, center_y2, vel_2, ell_factor, ang2)

                # Filter:
                # distance between vessels is at least less than 5 times the sum of the domains' major axes
                if not ((center_x2 - center_x1)**2 + (center_y2 - center_y1)**2)**0.5 > 5 * (semi_major_axis1 + semi_major_axis2) and not (vel_1 < min_vel and vel_2 < min_vel):

                    # Check if centers are inside the other ellipse
                    center1_in_ellipse2, center2_in_ellipse1 = check_centers_inside_each_other(
                        (semi_major_axis1, semi_minor_axis1, center_x1, center_y1, ang1),
                        (semi_major_axis2, semi_minor_axis2, center_x2, center_y2, ang2))

                    # Write result to file
                    if center1_in_ellipse2 or center2_in_ellipse1:
                        result.write(f"{mmsi_1};{timestamp1};{center_xe_1};{center_ye_1};{semi_major_axis1};{semi_minor_axis1};{ang1};{mmsi_2};{timestamp2};{center_xe_2};{center_ye_2};{semi_major_axis2};{semi_minor_axis2};{ang2}\n")