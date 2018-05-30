import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
import os

session = Session(profile_name='default')
myfile = input('enter file to upload: ')

def upload(myfile):
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(myfile,'jedijamez-projects','recording.mp3')


if __name__ == '__main__':
    upload(myfile)
print ('success')