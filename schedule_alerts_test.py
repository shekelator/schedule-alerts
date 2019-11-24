import schedule_alerts
import pytest
import datetime
import json

def test_seven_fifty_is_too_early():
    time = datetime.datetime(2019, 2, 16, 7, 50)
    assert schedule_alerts.is_in_range(time) == False
 
def test_no_bus_coming():
    file = open("testdata_nobus1.json")
    data = json.loads(file.read())["data"]
    assert schedule_alerts.get_response_from_predictions(data) == "Bus is not coming"
