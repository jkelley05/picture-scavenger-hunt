from picture_hunt.secrets import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from picture_hunt.config import UPLOADS, S3_BUCKET


from werkzeug import secure_filename

from boto3.session import Session

from datetime import datetime
import os


def upload_to_s3(file_):
    
    session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                     )
    s3 = session.resource('s3')  
    
    # Create a key for the new file
    time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
    file_name = secure_filename(file_.filename)
    key_str = time + '_' + file_name
    print('The key will be ' + key_str)
     
    # Upload the file
    s3.Bucket(S3_BUCKET).put_object(Key=key_str, Body=file_.stream)
    
    week = 60 * 60 * 24 * 7 
    client = session.client('s3')
    presigned_url = client.generate_presigned_url( 'get_object', Params={'Bucket': S3_BUCKET, 'Key': key_str}, ExpiresIn=week) 
    uri = key_str
    print(presigned_url)
    return presigned_url
