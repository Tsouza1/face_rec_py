import boto3
import json
import decimal
import requests
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')
table = dynamodb.Table('sala')


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

# Capturando Elemento do Banco
def get_item(user_id, roomId):

    url = r'https://84x8skef0k.execute-api.sa-east-1.amazonaws.com/dev/room/participant'
    
    obj = {
            'id' : user_id,
            'roomId' : roomId
    }
    print (user_id)
        # try:
    # person = requests.post(url, json=json.dumps(obj), headers = {'content-type': 'application/json'})

    # except ClientError as e:
    #     print(e.response['Error']['Message'])
    # else:
    # return (json.dumps(person, indent=4, cls=DecimalEncoder))
          