from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from get_station_info import fetch_station_data, read_client_id
from datetime import datetime

app = Flask(__name__)
api = Api(app)

class StationInfo(Resource):
    def get(self):
        """
        Get Oslo Bysykkel station data using the fetch_station_data
        function.
        """

        # URL arguments
        station_name_startswith = request.args.get("startswith")

        # Auth to API
        client_id = read_client_id("credentials.json")

        # Do not need to write to file now
        df = fetch_station_data(client_id, numrows=0, write_to_file=False)

        if station_name_startswith:
            df = df[df["station_name"].str.startswith(station_name_startswith)]
        else:
            pass

        output = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "stations": df.to_dict(orient="records"),
            "n_results": df.shape[0]
        }

        return(jsonify(output))


# Testing more than one endpoint
api.add_resource(StationInfo, "/", "/station_info") # Route_1


if __name__ == "__main__":
    # debug=True reruns the script every time you save the file
    app.run(port=5002, debug=True)
