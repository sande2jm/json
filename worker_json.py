#the point now is to create a worker that can use instructions.
import boto3
import json
from subprocess import call
from subprocess import check_output
from helper import *
import mpu.io

class Worker():

	def __init__(self):
		
		"""
		Connect to AWS s3 download full swarms parameters. Set the file this 
		will be reading from and the file this will be writing too. 
		"""
		self.direc = get_parent()
		self.params = {}
		self.s3 = boto3.resource('s3')
		# self.my_id = check_output(['curl', 'http://169.254.169.254/latest/meta-data/instance-id'])
		# self.my_id = "".join(map(chr, self.my_id))
		self.my_id = 'i-0583fd331291fecb4'
		self.results = "Results of worker " + self.my_id
		# self.s3.Bucket('swarm-instructions').download_file('instructions.txt', self.file_in)
		self.s3.Bucket('swarm-instructions').download_file('instructions.txt', 'instructions.txt')

	def extract(self):
		"""
		Use the file_in from init to extract this workers specific parameters
		from json dictionary based on ec2 instance ids
		"""		
		with open('instructions.txt', 'r') as f:
			swarm_params = json.load(f)
		self.params = swarm_params[self.my_id]
		self.s3.Bucket('swarm-instructions').download_file('data/' + self.params['images'], 'data.json')


	def run(self):
		"""
		Take the params from extract and run whatever operations you want
		on them. Set self.results in this method based on self.params
		"""
		print("Doing work on files")
		pass


	def report(self):
		"""
		Use the file_out to write the results of this worker to s3.
		"""
		with open(self.file_out, 'w') as outfile:
			json.dump(self.results, outfile)
		self.s3.meta.client.upload_file(self.file_out, 'swarm-results', self.file_out)
		



