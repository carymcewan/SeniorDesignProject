# Curated by Cary McEwan. Stay tuned. 
# Twitter   :: @Cary_MakinMoves
# Instagram :: @Cary_MakinMoves
# LinkedIn  :: https://www.linkedin.com/in/cary-mcewan-000b64140/

# from emailClient import EmailClient
#
# fileName = 'cube.ply'
# file = open(fileName)
# import boto3
# s3 = boto3.resource('s3')
# s3.meta.client.upload_file(fileName, 'seniordesigngroupb', fileName)
#
# url = 'https://s3.amazonaws.com/seniordesigngroupb/' + fileName

from boto.s3.connection import S3Connection
from boto.s3.key import Key

class S3Client():
    def __init__(self, key, otherKey):
        self.conn = S3Connection(key, otherKey)

    def uploadFile(self, bucket, fileName):
        file = open(fileName)
        b = self.conn.get_bucket(str(bucket))
        k = Key(b)
        k.key = fileName
        k.set_contents_from_file(file)
        return 'https://s3.amazonaws.com/seniordesigngroupb/' + fileName
