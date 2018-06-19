import boto3
import sys
import os
from time import time
from tempfile import gettempdir
from contextlib import closing

session = Session(profile_name='default', region_name='us-west-2')
rk = boto3.client('rekognition')
