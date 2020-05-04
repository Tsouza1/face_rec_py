import boto3
import json
import decimal
import requests
import urllib.request
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')
# table = dynamodb.Table('sala')

access_key = "AKIAZOIKPN5TFJPVJJ4Y"
secret_key = "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"
region_name='sa-east-1'

# s3_client = boto3.client('s3', aws_access_key_id=access_key,aws_secret_access_key=secret_key, region_name=region_name)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


# Carregando Imagem no Bucket
def bucket_upload(file, filename):
    
    bucket = "bucketknowface"
    img_file = file
    region_name='sa-east-1'
    s3_client = boto3.client('s3', region_name)
    try:
        response = s3_client.put_object(Body=img_file, Bucket=bucket, Key=filename)
    except ClientError as e:
        logging.error(e)
        return False

    url = "https://%s.s3-%s.amazonaws.com/%s" % (bucket, region_name, filename)

    return url

# Criando User no banco 
def create_item(form, file, filename):
    
    url = bucket_upload(file, filename)
    name = form['name']
    try:
        table.put_item(
        Item={
              'participante' : [
                {
                    'id': '2',
                    'name': name,
                    'url': url
                }]
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return "Created"

# Lendo url do Bucket
def get_item(bucket, item):
    url = create_presigned_url(bucket, item)

    img = urllib.request.urlopen(url)
    
    return img

# Criando url temporaria
def create_presigned_url(bucket_name, object_name, expiration=3600):
    s3_client = boto3.client('s3', aws_access_key_id=access_key,aws_secret_access_key=secret_key, region_name=region_name)

    try:
        response = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name,'Key': object_name},ExpiresIn=expiration)

    except ClientError as e:
        logging.error(e)
        return None

    return response