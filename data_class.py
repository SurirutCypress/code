#standard library
import graphs
import csv
import struct
import datetime

C1 = -8.784695
C2 = 1.61139411
C3 = 2.338549
C4 = -0.14611605
C5 = -1.2308094 * (10 ** -2)
C6 = -1.6424828 * (10 ** -2)
C7 = 2.211732 * (10 ** -3)
C8 = 7.2546 * (10 ** -4)
C9 = -3.582 * (10 ** -6)

SENSORS = ['LPG', 'Dust', 'Current', 'ElectricPower', 'lux', 'motion', 'temperature', 'humidity','HI']
class SensorData(object):
    def __init__(self):
        self.LPG = []
        self.Dust = []
        self.Current = []
        self.ElectricPower = []
        self.lux = []
        self.motion = []
        self.motion_hold = 0
        self.temperature = []
        self.HI = []
        self.humidity = []
        self.time = []
        self.time_pt = 0
        self.initialized = False
        # fill out other attributes needed
        date_started = datetime.datetime.now().strftime("%Y_%m_%d")
        print(date_started)

        self.filename = date_started + "_air_logging.csv"

        with open(self.filename, 'a') as self._file:
            self.writer = csv.writer(self._file)

            self.writer.writerow(['time','LPG', 'Dust', 'Current', 'ElectricPower', 'lux', 'motion', 'temperature', 'humidity', 'HI'])


    def add_data(self, packet):

        self.LPG.append(convert_bytes_to_float32(packet[0:4]))
        print(self.LPG)

        self.Dust.append(convert_bytes_to_float32(packet[4:8]))
        print(self.Dust)

        self.Current.append(convert_bytes_to_float32(packet[8:12]))
        print(self.Current)

        self.ElectricPower.append(convert_bytes_to_float32(packet[12:16]))
        print(self.ElectricPower)

        self.lux.append(packet[16] | (packet[17] << 8))
        print(self.lux)

        motion_pre = packet[18]
        if motion_pre == 1:
            self.motion_hold = 10
        elif self.motion_hold > 0:
            motion_pre = 1
            self.motion_hold -= 1

        self.motion.append(motion_pre)
        print(self.motion)

        self.temperature.append(packet[19])
        print(self.temperature)

        self.humidity.append(packet[20])
        print(self.humidity)

        self.HI.append(calculate_heat_index(self.temperature[-1], self.humidity[-1]))
        print(self.HI)


        self.time_pt += 1
        self.time.append(self.time_pt)
        time = datetime.datetime.now().strftime("%H:%M:%S")

        with open(self.filename, 'a') as self._file:
            self.writer = csv.writer(self._file)
            self.writer.writerow([time, self.LPG[-1], self.Dust[-1], self.Current[-1], self.ElectricPower[-1], self.lux[-1], self.motion[-1], self.temperature[-1], self.humidity[-1], self.HI[-1]])

def convert_bytes_to_float32(_bytes):
    _float = struct.unpack('f', _bytes)
    return _float[0]

def calculate_heat_index(temp, humidity):
    return C1+(C2*temp)+(C3*humidity)+(C4*temp*humidity)+(C5*(temp**2))+(C6*(humidity**2))+(C7*(temp**2)*humidity)+(C8*temp*(humidity**2))+(C9*(temp**2)*(humidity**2))




