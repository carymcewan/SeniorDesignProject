# Curated by Cary McEwan. Stay tuned. 
# Twitter   :: @Cary_MakinMoves
# Instagram :: @Cary_MakinMoves
# LinkedIn  :: https://www.linkedin.com/in/cary-mcewan-000b64140/

import boto3

class S3Client():
    def __init__(self):
        self.s3 = boto3.resource('s3')

    def uploadFile(self, fileLocation, bucketName, fileName):
        self.s3.meta.client.upload_file(fileLocation, bucketName, fileName)
        return 'https://s3.amazonaws.com/' + bucketName + '/' + fileName