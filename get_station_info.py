# Libraries used
import argparse # This looks like is included with py36 :)
import pandas as pd
import requests
import simplejson as json
from pandas.io.json import json_normalize


# Helper functions

def read_client_id(fpath):
    """
    Credentials json file is stored in fpath and has the format:

    {"client-id" : "<your_unique_client_id>"}

    """
    with open(fpath, "r") as f:
        credentials = json.load(f)

    return(credentials["client-id"])


def get_data(url, client_id):
    """ Fetch data from Oslo Bysykkel API using a GET request"""
    # Set up mandatory header
    headers = {"Client-Identifier": client_id}

    # Perform the get request to fetch wanted data
    r = requests.get(url, headers=headers)

    return(r.json())


def parse_stations_to_dataframe(json_data):
    """ Transform station data into a dataframe. """
    df = pd.DataFrame(json_data["stations"])
    # Remove stations not in service
    df = df[df.in_service == True]

    return(df)


def rename_columns(df):
    """ Rename specific columns of the dataframe """

    column_mapper = {
        'title': "station_name",
        'availability.bikes': 'available_bikes',
        'availability.locks': 'available_locks',
    }
    df.rename(inplace=True, columns=column_mapper)

    return(df)

# Create own function for the fetching part
def fetch_station_data(client_id, numrows, write_to_file=True):
    """ Get data from Bysykkel API """

    # Base url of the api
    base_url = "https://oslobysykkel.no/api/v1"
    # Name of the output file where the results will be stored
    outfile_name = "station_availability.csv"

    # Return this if something goes wrong
    station_status_df = None

    # Get the data
    try:
        # Get API data and store into dicts
        stations_dict = get_data(base_url + "/stations", client_id)
        availability_dict = get_data(base_url + "/stations/availability", client_id)

        # Transform from dicts to dataframes
        stations_df = parse_stations_to_dataframe(stations_dict)
        availability_df = json_normalize(availability_dict["stations"])

        # Join into one dataframe
        station_status_df = pd.merge(stations_df, availability_df, on="id", how="left")

        station_status_df = rename_columns(station_status_df)

        # Need only to present these three cols
        station_status_df = station_status_df[['station_name',
                                               'available_bikes',
                                               'available_locks']]

        # Sort by name and reset index
        station_status_df.sort_values(by="station_name", ascending=True, inplace=True)
        station_status_df.reset_index(drop=True, inplace=True)

        # Print data and info
        if numrows > 0:
            print("\nStation availability at {} stations:\n".format(numrows))
            print(station_status_df.head(numrows))

        # Write to file by default
        if write_to_file:
            station_status_df.to_csv(outfile_name, index=False)
            print("\nAll station results written to file: {}\n".format(outfile_name))

    # Handle errors
    except requests.exceptions.ConnectionError:
        print("No internet connection")
    except KeyError as kerr:
        print("The api url is not correct. Erroneous key: {}".format(kerr))
    # Handle other exceptions
    except Exception as exp:
        print(type(exp))
        print(exp)

    return(station_status_df)


# Main function

def main():
    """ Main flow of the script """

    # Client-Identifier string
    client_id = read_client_id("credentials.json")


    # Setup parser for better cli usage
    script_description = """
    Get the status of available locks and bikes at all Oslo byskkel stations.
    """

    parser = argparse.ArgumentParser(description=script_description)

    # Optional argument
    parser.add_argument("--numrows",
                        help="""
                        Number of dataframe rows to be printed on the console.
                        Will not print if not given. 
                        """,
                        default=0,
                        type=int)

    args = parser.parse_args()

    # Get data, bot do not need the result here
    _ = fetch_station_data(client_id, args.numrows)


if __name__ == "__main__":
    main()
