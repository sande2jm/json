#the point now is to create a worker that can use instructions.
import boto3
import json
from subprocess import call
from subprocess import check_output
from helper import *
import mpu.io
from joblib import Parallel, delayed
import multiprocessing
from PIL import Image
import pickle
import MacOSFile as msf
import numpy as np
import mpu.io
import requests
from io import BytesIO

class Worker():

	def __init__(self):
		
		"""
		Connect to AWS s3 download full swarms parameters. Set the file this 
		will be reading from and the file this will be writing too. 
		"""
		self.direc = get_parent()
		self.params = {}
		#self.s3 = boto3.resource('s3')
		#sqs = boto3.resource('sqs',region_name='us-east-1')
		#self.queue = sqs.get_queue_by_name(QueueName='swarm.fifo')
		self.my_id = check_output(['curl', 'http://169.254.169.254/latest/meta-data/instance-id'])
		self.my_id = "".join(map(chr, self.my_id))
		# self.my_id = 'i-0097e1fa8c756c590'
		self.file_out = None
		self.results = "Results of worker " + self.my_id
		self.data = None
		#self.s3.Bucket('swarm-instructions').download_file('instructions.txt', 'instructions.txt')

	def extract(self):
		"""
		Use the file_in from init to extract this workers specific parameters
		from json dictionary based on ec2 instance ids
		"""		
		with open('instructions.txt', 'r') as f:
			swarm_params = json.load(f)
		self.params = swarm_params[self.my_id]
		#self.s3.Bucket('swarm-instructions').download_file('data/' + self.params['images'], 'data.json')
		self.data = mpu.io.read('data.json')
		pos = self.params['index']
		self.file_out = "data" + "_" + str(pos) + ".pkl"


	def run(self):
		"""
		Take the params from extract and run whatever operations you want
		on them. Set self.results in this method based on self.params
		"""
		# print(self.params)
		transformed_data = self.convert_json()
		msf.pickle_dump(transformed_data, self.file_out)
		

	def convert_json(self):
		# print(type(self.data['images']),self.data['images'][0], self.data['images'][0]['url'])
		#num_cores = multiprocessing.cpu_count()
		# images = Parallel(n_jobs=num_cores)(delayed(self.create_image)(i) for i in self.data['images'][:100])
		dummy = [0,0,0,0,0,0,0]
		results = []
		num_cores = multiprocessing.cpu_count()
		print(num_cores)
		print(type(self.data['images']))
		if num_cores > 1:
			results = Parallel(n_jobs=num_cores)(delayed(self.create_image)(i) for i in dummy)
		else:
			# results = [self.create_image(x) for x in self.data['images']]
			for i,x in enumerate(self.data['images']):
				if i %100 == 0:self.report(i)
				results.append(self.create_image(x))
		return results

	def create_image(self,elem):
		#print(elem)
		print(elem['imageId'])
		try:
			response = requests.get(elem['url'],timeout=2)
		except:
			return "Failed"
		return np.array(Image.open(BytesIO(response.content)).convert('RGB').resize((64,64)))

	def report(self,i):
		size = len(self.data['images'])
		d = {
		'message': 'working',
		'id': self.my_id,
		'progress': round(i/size,4)}
		#response = self.queue.send_message(MessageBody=json.dumps(d), MessageGroupId='json_bots')


	def dump(self):
		"""
		Use the file_out to write the results of this worker to s3.
		"""
		self.s3.meta.client.upload_file(self.file_out, 'swarm-results', self.file_out)
		d = {
		'message': 'complete',
		'id': self.my_id,
		'progress': 'None'}
		#response = queue.send_message(MessageBody=json.dumps(d), MessageGroupId='json_bots')



