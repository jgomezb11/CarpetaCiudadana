import boto3
import os
from dotenv import (load_dotenv)
from botocore.exceptions import NoCredentialsError

def upload_file_to_s3(file, bucket_name, s3_file_name):
    load_dotenv()
    s3 = boto3.client('s3', 
                      aws_access_key_id=os.getenv('AWS_ACCESS_KEY'), 
                      aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

    try:
        s3.upload_fileobj(file, 
                          bucket_name, 
                          s3_file_name,
                          ExtraArgs={
                            'ACL': 'public-read',
                            'ContentType': file.content_type
                            }
                          )

        print("Upload Successful")
        return f"https://{bucket_name}.s3.amazonaws.com/{s3_file_name}"

    except FileNotFoundError:
        print("The file was not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None
