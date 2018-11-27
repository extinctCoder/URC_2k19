import time
import math
import serial

gps_conn = serial.Serial('COM4', 115200)
runner_conn = serial.Serial('COM6', 9600)


def execute_command(command):
    runner_conn.write(command.encode('ascii'))
    return


def calculate_distance(source_latitude, source_longitude, destination_latitude, destination_longitude):
    radiant = 6371

    source_latitude_radiant = math.radians(source_latitude)
    source_longitude_radiant = math.radians(source_longitude)

    destination_latitude_radiant = math.radians(destination_latitude)
    destination_longitude_radiant = math.radians(destination_longitude)

    remain_latitude = destination_latitude_radiant - source_latitude_radiant
    remain_longitude = destination_longitude_radiant - source_longitude_radiant

    # Distance calculated through Haversine Formula [https://en.wikipedia.org/wiki/Haversine_formula]
    haversine_formula = math.sin(remain_latitude / 2) ** 2 + (math.cos(source_latitude_radiant) * math.cos(destination_latitude_radiant) * math.sin(remain_longitude / 2) ** 2)
    return radiant * (2 * math.asin(math.sqrt(haversine_formula)))  # Error margin 10%


def intermediate_point(step_size, source_latitude, source_longitude, destination_latitude, destination_longitude):
    distance_radius = calculate_distance(source_latitude, source_longitude, destination_latitude, destination_longitude) / 6371

    source_latitude_radiant = math.radians(source_latitude)
    source_longitude_radiant = math.radians(source_longitude)

    destination_latitude_radiant = math.radians(destination_latitude)
    destination_longitude_radiant = math.radians(destination_longitude)

    a = math.sin((1 - step_size) * distance_radius) / math.sin(distance_radius)
    b = math.sin(step_size * distance_radius) / math.sin(distance_radius)

    x = a * math.cos(source_latitude_radiant) * math.cos(source_longitude_radiant) + b * math.cos(destination_latitude_radiant) * math.cos(destination_longitude_radiant)
    y = a * math.cos(source_latitude_radiant) * math.sin(source_longitude_radiant) + b * math.cos(destination_latitude_radiant) * math.sin(destination_longitude_radiant)
    z = a * math.sin(source_latitude_radiant) + b * math.sin(destination_latitude_radiant)

    latitude = math.degrees(math.atan2(z, math.sqrt(x * x + y * y)))
    longitude = math.degrees(math.atan2(y, x))

    return [latitude, longitude]


def get_gps_data():
    data = gps_conn.readline().decode('utf-8').strip('\r\n')
    return data.split(',')


# Main Code Block

d_latitude = 23.82191  # float(input("Destination Latitude in Decimal Degrees: "))
d_longitude = 90.42742   # float(input("Destination Longitude in Decimal Degrees: "))
error = .014
time_error = 20
time_count = 0;
p_array = get_gps_data()
p_array[0] = float(p_array[0])
p_array[1] = float(p_array[1])

t_distance = calculate_distance(p_array[0], p_array[1], d_latitude, d_longitude)

s_size = 0.01
curStp = 0

time.sleep(2)
print("Distance from source to destination: ", t_distance, " Km\n")
print("Current Location: ", p_array)

while calculate_distance(p_array[0], p_array[1], d_latitude, d_longitude) >= error:
    execute_command('w')
    print("Rover forward direction")
    print("Current position: ", p_array, "\n")
    p_array = get_gps_data()
    p_array[0] = float(p_array[0])
    p_array[1] = float(p_array[1])
    print("Dist: ", calculate_distance(p_array[0], p_array[1], d_latitude, d_longitude))
    time.sleep(1)
    time_count = time_count + 1
    if time_count == 5:
        print("fixing gps error")
        execute_command('z')
        for i in range(0, time_error):
            p_array = get_gps_data()
            p_array[0] = float(p_array[0])
            p_array[1] = float(p_array[1])
            print("Current position: ", p_array, "\n")
            time.sleep(1)

        time_count = 0

execute_command('z')
gps_conn.close()
runner_conn.close()
print('Destination Reached\nHalt!')
