import pytest
from get_station_info import *
import pandas as pd


# Fixtures

@pytest.fixture(scope="session")
def client_id():
    return(read_client_id("credentials.json"))

@pytest.fixture(scope="session")
def get_station_response(client_id):
    data = get_data("https://oslobysykkel.no/api/v1/stations", client_id)
    return(data)

@pytest.fixture(scope="session")
def get_station_availability_response(client_id):
    data = get_data("https://oslobysykkel.no/api/v1/stations/availability", client_id)
    return(data)

## Actual tests

def test_read_client_id_returns_string(client_id):
    assert(type(client_id) == str)


class TestGetData(object):
    """ Should use mocking for this """
    def test_station_response_is_dict(self, get_station_response):
        assert(type(get_station_response) == dict)

    def test_station_availability_response_is_dict(self, get_station_availability_response):
        assert(type(get_station_availability_response) == dict)

    def test_returns_stations(self, get_station_response):
        assert("stations" in list(get_station_response))

    def test_returns_availability(self, get_station_availability_response):
        assert("availability" in list(get_station_availability_response["stations"][0].keys()))


class TestParseStationsToDataframe(object):
    def test_returns_df(self, get_station_response):
        df = parse_stations_to_dataframe(get_station_response)
        assert(isinstance(df, pd.DataFrame))


def test_rename_columns():
    data = {
        "title": "A",
        "availability.bikes": 1,
        "availability.locks": 0
    }
    renamed_df = rename_columns(pd.DataFrame([data, ]))
    assert("station_name" in renamed_df.columns.tolist())
    assert("available_bikes" in renamed_df.columns.tolist())
    assert("available_locks" in renamed_df.columns.tolist())
