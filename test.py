from __future__ import print_function
import boto3
from boto3 import Session
import time
from random import randint
import urllib
import os
from tempfile import gettempdir
import subprocess
import contextlib
import json
import pprint

myFile = os.path.join(gettempdir(), 'ts.json')

subprocess.Popen(['cat', myFile])