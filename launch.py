from subprocess import call
import time
import boto3
import json
from worker_json import Worker

print("Launch Complete")
w = Worker()
w.extract()
w.run()
w.report()

