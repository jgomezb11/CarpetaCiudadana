import os
import boto3
from dotenv import load_dotenv

def get_aws_keys():
    access = os.getenv('AWS_ACCESS_KEY')
    secret = os.getenv('AWS_SECRET_ACCESS_KEY')
    session = os.getenv('AWS_SESSION_TOKEN')
    return (access, secret, session)

class s3:
    def __init__(self):
        load_dotenv()
        self.credentialsAWS = get_aws_keys()
        self.s3 = self.get_boto_client()

    def get_boto_client(self):
        connection = boto3.client(
            's3',
            aws_access_key_id=self.credentialsAWS[0],
            aws_secret_access_key=self.credentialsAWS[1],
            aws_session_token=self.credentialsAWS[2],
            region_name="us-east-1"
        )
        return connection


    def upload_file(self, archivo, nombre_archivo):
        bucket_name = 'carpetaciudadana'
        self.s3.upload_fileobj(archivo, bucket_name, nombre_archivo)
        url = f'https://.s3.amazonaws.com/{bucket_name}/{nombre_archivo}'
        return url


    def delete_file(self, nombre_archivo):
        nombre = nombre_archivo.split('carpetaciudadana/')[1]
        self.s3.delete_object(Bucket='carpetaciudadana', Key=nombre)


    def delete_folder(self, name_folder):
        bucket_name = 'carpetaciudadana'
        objects = self.s3.list_objects_v2(Bucket=bucket_name,
                                           Prefix=name_folder)
        keys = [{'Key': obj['Key']} for obj in objects]
        if keys:
            self.s3.delete_objects(Bucket=bucket_name,
                                    Delete={'Objects': keys})
        self.s3.delete_object(Bucket=bucket_name, Key=name_folder)
