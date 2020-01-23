import adafruit_dht
import board
from datetime import datetime
import time
import statistics

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('secret.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'


class Monitor:
	def __init__(self, location):
		self.location = location
		self.dhtDevice = adafruit_dht.DHT22(board.D4)
		self.temps = []
		self.humidities = []
		self.beginTime = datetime.now()
		self.endTime = 0

	def monitor(self):
		while True:
			now = datetime.now()
			difference = now - self.beginTime

			if difference.seconds > 300:
				self.aggregate()
				self.reset()

			self.get_temp()
			time.sleep(2.0)

	def reset(self):
		self.beginTime = datetime.now()
		self.endTime = 0
		self.temps = []
		self.humidities = []

	def get_temp(self):
		try:
			temp_c = self.dhtDevice.temperature
			humidity = self.dhtDevice.humidity

			t = datetime.now()
			current_time = t.strftime('%m/%d/%Y %H:%M:%S')

			self.temps.append(temp_c)
			self.humidities.append(humidity)

		except RuntimeError as error:
			# print(error.args[0])
			dummy = 5

	def aggregate(self):
		tempMed = statistics.median(self.temps)
		humidityMed = statistics.median(self.humidities)
		self.endTime = datetime.now()

		self.send_aggregate(tempMed, humidityMed)

	def send_aggregate(self, tempMed, humidityMed):
		dataCount = len(self.temps)

		record = {
			'temp': tempMed,
			'humidity': humidityMed,
			'beginTime': self.beginTime.strftime('%m/%d/%Y %H:%M:%S'),
			'endTime': self.endTime.strftime('%m/%d/%Y %H:%M:%S'),
			'timestamp': firestore.SERVER_TIMESTAMP,
			'location': self.location,
			'recordCount': len(self.temps)
		}

		db.collection(u'temp_records').add(record)

		print(f'Record Count: {dataCount}')


temp = Monitor('Living Room')

temp.monitor()
