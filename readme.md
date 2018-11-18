# Readme
The script [get_station_info.py](get_station_info.py) connects to the [Oslo 
Bysykkel API](https://developer.oslobysykkel.no/api) and fetches status about the number of available bikes and locks at each station.

All results are stored in a created csv file called `station_availability.csv`.
One also gets a preview of the results in the console. Number of rows
which is printed to the console is determined by the optional parameter
`numrows` (default value: 5).

## How to run the script

### 1. Python environment
This script is made and tested in a conda python environment. You do not
need to use a conda environment, but be sure to use same/similar python 
version and libraries. Info about versions and libraries is found in the 
[environment file](environment.yml)

### 2. API credentials: client-identifier
In order to run the script, you will need to have an unique `client-identifier` 
string which identifies your application. How to get this is informed in the 
API link above.

### 3. Credentials json file
Simply paste your `client-identifier` in the [tmp_credentials.json](tmp_credentials.json),
and rename the file to `credentials.json`. The script reads the 
identifier from this file. 

### 4. How to use the script

```shell
# Get help and info about script and input arguments
python get_station_info.py -h

# Run with default parameters
python get_station_info.py

# Run with different number of output rows in the console
python get_station_info.py --numrows 20
```