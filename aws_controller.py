import boto3
import json
import decimal
import urllib.request

region_name='sa-east-1'

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

# Criando url temporaria
def create_presigned_url(bucket_name, object_name, expiration=3600):

    s3_client = boto3.client('s3', region_name)

    try:
        response = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name,'Key': object_name},ExpiresIn=expiration)

    except ClientError as e:
        logging.error(e)
        return None

    return response

# Lendo url do Bucket
def get_item(bucket, item):
    url = create_presigned_url(bucket, item)

    img = urllib.request.urlopen(url)
    
    return img
