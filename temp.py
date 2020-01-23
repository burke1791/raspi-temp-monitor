import adafruit_dht
import board
from datetime import datetime
import time

# ----------- User Settings --------------

# ----------------------------------------


class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'


dhtDevice = adafruit_dht.DHT22(board.D4)

class Monitor:
	def __init__(self):
		dhtDevice = adafruit_dht.DHT22(board.D4)

	def monitor(self):
		while True:
			self.get_temp()
			time.sleep(2.0)

	def get_temp(self):
		try:
			temp_c = dhtDevice.temperature
			humidity = dhtDevice.humidity

			t = datetime.now()
			current_time = t.strftime('%m/%d/%Y %H:%M:%S')

			print(f'{bcolors.BOLD}Time:{bcolors.ENDC} {bcolors.OKBLUE}{current_time}{bcolors.ENDC}   {bcolors.BOLD}Temp:{bcolors.ENDC} {bcolors.OKBLUE}{temp_c:.1f} C{bcolors.ENDC}    {bcolors.BOLD}Humidity:{bcolors.ENDC} {bcolors.OKBLUE}{humidity}%{bcolors.ENDC}')

		except RuntimeError as error:
			#print(error.args[0])
			dummy = 5


temp = Monitor()

temp.monitor()
