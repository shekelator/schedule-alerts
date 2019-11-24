import requests
import json
import boto3
from datetime import datetime, time
import re

# deploy instructions: https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html
# zip -r9 ../function.zip .
# aws lambda update-function-code --function-name schedule-alerts --zip-file fileb://function.zip


# https://api-v3.mbta.com/predictions?filter[stop]=31187&filter[route]=42&filter[direction_id]=0



def is_in_range(arrival_time):
    t = arrival_time.time()
    if(t > time(7, 55, 0) and t < time(8, 5, 0)):
        return True
    else:
        return False

def get_response_from_predictions(predictions):
    upcoming = []

    for p in predictions:
        #arrival_time = datetime.fromisoformat(p['attributes']['arrival_time']) #2019-11-16T22:44:26-05:00
        arrival_time_parsed = re.sub(r'\-0[45]:00$', "", p['attributes']['arrival_time'])
        arrival_time = datetime.strptime(arrival_time_parsed, "%Y-%m-%dT%H:%M:%S")
        if(is_in_range(arrival_time)):
            upcoming.append(arrival_time)

    if(len(upcoming) > 0):
        return "Next bus is coming at " + upcoming[0].strftime("%I:%M %p")

    else:
        return "Bus is not coming"



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