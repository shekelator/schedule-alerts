import requests
import json
import boto3
from datetime import datetime, time
import re

# deploy instructions: https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html
# zip -r9 ../function.zip .
# aws lambda update-function-code --function-name schedule-alerts --zip-file fileb://function.zip


# https://api-v3.mbta.com/predictions?filter[stop]=31187&filter[route]=42&filter[direction_id]=0

def iso_to_datetime(datetimeStr):
    #arrival_time = datetime.fromisoformat(p['attributes']['arrival_time']) #2019-11-16T22:44:26-05:00
    time_parsed = re.sub(r'\-0[45]:00$', "", datetimeStr)
    convertedTime = datetime.strptime(time_parsed, "%Y-%m-%dT%H:%M:%S")
    return convertedTime

def is_in_range(arrival_time):
    t = arrival_time.time()
    if(t > time(7, 55, 0) and t < time(8, 10, 0)):
        return True
    else:
        return False

def get_response_from_predictions(predictions):
    '''
    upcoming = []
    for p in predictions:
        arrival_time = iso_to_datetime(p['attributes']['arrival_time'])
        if(is_in_range(arrival_time)):
            upcoming.append(arrival_time)
    '''
    
    times = list(map(lambda x: iso_to_datetime(x['attributes']['arrival_time']), predictions))
    upcoming = [p for p in times if is_in_range(p)]

    if not upcoming:
        return "Bus is not coming"

    if(len(upcoming) == 1):
        return "Next bus is coming at " + upcoming[0].strftime("%I:%M %p")

    else:
        return "Next buses are coming at " + upcoming[0].strftime("%I:%M %p") \
            + " and " + upcoming[1].strftime("%I:%M %p")




def lambda_handler(event, context):
    predictionsResponse = requests.get("https://api-v3.mbta.com/predictions?filter[stop]=31187&filter[route]=42&filter[direction_id]=0")

    predictionsData = predictionsResponse.json()['data']

    message = get_response_from_predictions(predictionsData)
    
    sns = boto3.client('sns')
    response = sns.publish(
        TopicArn = "arn:aws:sns:us-east-1:261024489445:schedule-alerts",
        # TargetArn = "",
        Message = message,
        MessageStructure = "string"
    )

    print(message)
    print(response)

    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }
