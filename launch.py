from subprocess import call
import time
import boto3
import json
from worker_json import Worker
import sys

sqs = boto3.resource('sqs',region_name='us-east-1')
# Create the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(QueueName='test')
my_id = check_output(['curl', 'http://169.254.169.254/latest/meta-data/instance-id'])
my_id = "".join(map(chr, self.my_id))

d = {
'message': 'launched',
'id': my_id,
'progress': 'None'}

response = queue.send_message(MessageBody=json.dumps(d))

# w = Worker()
# w.extract()
# w.run()
# w.report()

