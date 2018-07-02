#the point now is to create a worker that can use instructions.
import boto3
import json
from subprocess import call
from subprocess import check_output
from helper import *

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
		self.file_in = self.direc + "/" + self.my_id[-4:] +"_input.txt"
		self.file_out = self.direc + "/" + self.my_id[-4:] +"_output.txt"
		self.results = "Results of worker " + self.my_id
		self.s3.Bucket('swarm-instructions').download_file('instructions.txt', self.file_in)

	def extract(self):
		"""
		Use the file_in from init to extract this workers specific parameters
		from json dictionary based on ec2 instance ids
		"""		
		with open(self.file_in, 'r') as f:
			swarm_params = json.load(f)
		self.params = swarm_params[self.my_id]


	def run(self):
		"""
		Take the params from extract and run whatever operations you want
		on them. Set self.results in this method based on self.params
		"""
		pass


	def report(self):
		"""
		Use the file_out to write the results of this worker to s3.
		"""
		with open(self.file_out, 'w') as outfile:
			json.dump(self.results, outfile)
		self.s3.meta.client.upload_file(self.file_out, 'swarm-results', self.file_out)
		



