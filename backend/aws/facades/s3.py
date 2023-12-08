from uuid import uuid4

import boto3


class S3:

    def __init__(self):
        self.client = boto3.client('s3')
        self.bucket_name = 'gsn-01-public'

    def upload_in_memory_file(self, file, folder) -> str:
        """
        uploads a file that is currently on memory
        """

        extension = file.name.split('.')[-1]
        file_name = f"{uuid4()}.{extension}"
        destiny = f"{folder}/{file_name}"

        kwargs = {
            'Body': file.file,
            'Bucket': self.bucket_name,
            'Key': destiny,
            'ContentType': file.content_type,
        }
        
        self.client.put_object(**kwargs)  # check HTTPStatusCode ?

        return f"https://{self.bucket_name}.s3.amazonaws.com/{destiny}"