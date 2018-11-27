import serial
import time

gps_conn = serial.Serial('COM4', 115200)


def get_gps_data():

    data = gps_conn.readline().decode('utf-8').strip('\r\n')
    return data.split(',')


# Main Code Block

while 1:
    new_data = get_gps_data()
    new_data[0] = float(new_data[0])
    new_data[1] = float(new_data[1])
    print(new_data)
