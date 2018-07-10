#the point now is to create a worker that can use instructions.
import boto3
import json
from subprocess import call
from subprocess import check_output
from helper import *
from threading import Thread
import time

class Worker():

	def __init__(self):
		
		"""
		Connect to AWS s3 download full swarms parameters. Set the file this 
		will be reading from and the file this will be writing too. 
		"""
		self.direc = get_parent()
		self.params = {}
		self.s3 = boto3.resource('s3')
		self.my_id = check_output(['curl', 'http://169.254.169.254/latest/meta-data/instance-id'])
		self.my_id = "".join(map(chr, self.my_id))
		self.sqs = boto3.resource('sqs', region_name='us-east-1')
		self.state = ['waiting']
		self.queue = self.sqs.get_queue_by_name(QueueName='swarm.fifo')
		self.controller_listener = Thread(target=self.check_in, daemon=True)
		self.controller_listener.start()
		self.group_id = 'json'
		# self.s3.Bucket('swarm-instructions').download_file('instructions.txt', self.file_in)
		# self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
		# self.table = dynamodb.Table('swarm')

		"""JSON SPECIFIC VARIABLES"""
		self.file_out = None
		self.data = None
		self.s3.Bucket('swarm-instructions').download_file('parameters.txt', 'parameters.txt')

	def check_in(self):
		while True:
			with open(self.group_id +'/state.txt', 'r') as f:
				self.state[0] = f.read()
				time.sleep(3)

	def extract(self):
		"""JSON SPECIFIC EXTRACT"""		
		with open('parameters.txt', 'r') as f:
			swarm_params = json.load(f)
		self.params = swarm_params[self.my_id]
		self.s3.Bucket('swarm-instructions').download_file('data/' + self.params['images'], 'data.json')
		self.data = mpu.io.read('data.json')
		pos = self.params['index']
		self.file_out = "data" + "_" + str(pos) + ".pkl"
		


	def run(self):
		"""
		Take the params from extract and run whatever operations you want
		on them. Set self.results in this method based on self.params
		"""
		size = len(self.data['images'])
		i = 0
		while self.state[0] == 'waiting':
			print("Waiting for GO") 
			time.sleep(.3)

		results = []
		i = 0
		while i < size and self.state[0] != 'exit':
			if i%100 == 0:
				self.report(i, size=size)
			results.append(self.create_image(x))
			while self.state[0] == 'pause':
				time.sleep(.3)
				self.report(i,size=size)
			i += 1
		msf.pickle_dump(results, self.file_out)

	def create_image(self,elem):
		#print(elem)
		print(elem['imageId'])
		try:
			response = requests.get(elem['url'],timeout=2)
		except:
			return "Failed"
		return np.array(Image.open(BytesIO(response.content)).convert('RGB').resize((64,64)))


		


	def report(self,i, size = 100):
		"""
		Post to swarm queue my progress and state
		"""
		d = {
		'message': 'working',
		'state': self.state[0],
		'id': self.my_id,
		'progress': round(i/size,4)}
		response = self.queue.send_message(MessageBody=json.dumps(d), MessageGroupId=self.group_id)

	def dump(self):
		"""
		Use the file_out to write the results of this worker to s3.
		"""
		d = {
		'message': 'complete',
		'state': self.state[0],
		'id': self.my_id,
		'progress': 'None'}
		response = self.queue.send_message(MessageBody=json.dumps(d), MessageGroupId=self.group_id)


		



