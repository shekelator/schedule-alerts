import requests
import json
from datetime import datetime, time

# deploy instructions: https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html

# https://api-v3.mbta.com/predictions?filter[stop]=31187&filter[route]=42&filter[direction_id]=0



def is_in_range(arrival_time):
    t = arrival_time.time()
    if(t > time(7, 55, 0) and t < time(8, 5, 0)):
        return True
    else:
        return False


def lambda_handler(event, context):
    response = requests.get("https://api-v3.mbta.com/predictions?filter[stop]=31187&filter[route]=42&filter[direction_id]=0")
    # print(response.json()[0]['attributes']['arrival_time'])
    upcoming = []

    for p in response.json()['data']:
        arrival_time = datetime.fromisoformat(p['attributes']['arrival_time'])
        if(is_in_range(arrival_time)):
            upcoming.append(p)

    if(len(upcoming) > 0):
        message = "Bus is coming at"
    else:
        message = "Bus is not coming"

    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }
