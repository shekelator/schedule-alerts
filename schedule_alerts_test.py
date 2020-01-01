import schedule_alerts
import pytest
import datetime
import json

def test_seven_fifty_is_too_early():
    time = datetime.datetime(2019, 2, 16, 7, 50)
    assert schedule_alerts.is_in_range(time) == False
 
def test_no_bus_coming():
    data = get_data("testdata_nobus1.json")
    assert schedule_alerts.get_response_from_predictions(data) == "Bus is not coming"

def test_one_coming():
    data = get_data("testdata_1coming.json")
    assert schedule_alerts.get_response_from_predictions(data) == "Next bus is coming at 08:01 AM"

def test_two_coming():
    data = get_data("testdata_2coming.json")
    assert schedule_alerts.get_response_from_predictions(data) == "Next buses are coming at 07:56 AM and 08:09 AM"

def get_data(filename):
    file = open(filename)
    return json.loads(file.read())["data"]
