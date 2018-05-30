import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
import os

session = Session(profile_name="default")
myfile = input("Please enter a file to upload: ")

def upload(myfile):
    os.system('aws s3 cp ' + myfile + ' s3://jedijamez-projects/')

if __name__ == '__main__':
    upload(myfile)
print("success")
