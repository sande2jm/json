from subprocess import call
import time
import boto3
import json
from worker_json import Worker
import sys


print("Launch Complete")
sys.stdout.flush()
w = Worker()
w.extract()
w.run()
w.report()

