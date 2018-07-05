import boto3
self.s3 = boto3.resource('s3')
sqs = boto3.resource('sqs',region_name='us-east-1')
self.queue = sqs.get_queue_by_name(QueueName='swarm.fifo')