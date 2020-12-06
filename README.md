# ark Invest Holdings Tracking and Analytics
Ark Invest holdings tracking and analytics app built on GCP (Google Cloud Platform). This is pretty much a learning project.

## Overview

### `csv_loader`
a GCP Cloud function
* Trigger: a new (including overrides) csv file uploaded to a specific cloud storage location (`nw-msds498-ark-etf-analytics`)
* This function does one task: load the csv file (Ark Invest daily holding, specific format) to BigQuery table: `ark.holdings`
* `env.yaml` - environment variables for cloud function
* `main.py` - main logic
* `requirement.txt` - python libraries required to run this function


### pdf
One-off function to convert Ark Invest's PDF files to csv format, then load it to cloud storage/BigQuery.
* `docs` - Store pdf files to be converted temporarily
* `csv` - Store converted csv files temporarily
    * `upload.sh` - Upload converted csvs to cloud storage
* `main.py` - convert holdings pdf to csv using `tabula` and `pandas` library
* `trade_price.py` - Convert ark trade log (with real execution prices) pdf to csv format
* `merge_price.py` - merged converted csvs, validates duplicates and inconsistencies as well

### `price.py`

#### `cli`
* `ixe.py` - core functions to get minute price and day price information using `iexcloud API` via `iexfinance` python library
* `config.py` - configuration files used by multiple py file. Including reading/preparing API keys, dictionaries of commonly used fields like:
    * foreign symbols that can't be handled now
    * standard API errors
    * standard API request types
    * query all available trading days and symbols etc.
* `get_trade_days.py` use `pandas_market_calendars` library to get trading days between date range
* `token.py` - Retrieve iex API token, will deprecate soon

#### `data` and `log`
temporary folders for data and logging

#### `cre_req.sh`
Shell script to create python requirements file and remove `pkg-resources==0.0.0`, this is specific for develop in google cloud shell 

#### `get_price.py`
A wrapper function to call `cli/iex.py`

#### `load.sh` 
Upload files that with specific name pattern to cloud storage then load them from cloud storage to BigQuery
* Delete table from BigQuery first if needed

#### `mergedf.py`
One-off function to merge mulitple csv file in the same format into one.

#### `price.py`
WIP python library to get data from iex API (potentially other APIs as well in the future), to solve the efficiency issue with `iexfinance` library

#### `rename.sh`
one off shell script to rename some files produced before

#### `requirement.txt` 
python libraries required to run everything under price folder

#### `upload.sh`
bulk upload files to cloud storage

#### `upload_n_load.sh`
local --> cloud storage --> BigQuery
* takes in two arguments
    * price type, min or day
    * file name to be loaded (on cloud storage)

### pull
This folder contains all components of a full-fledged working cloud functions.

It pulls holdings data from Ark Invest website (csv format) and upload the csv files onto cloud storage. (Which would then trigger `csv_loader` function automatically)

* `env.yaml` - environmental variables for cloud function
* `main.py` code of the cloud function
* `requirements.txt` - list of python libraries needed
* `sh folder` - scripts to support deployment of the function etc.
    * `deploy.sh` - script to deploy this cloud function
    * `log_today.sh` to get logs of this function (`ark-holdings-daily-pull`) running on GCP for today.
        * Takes specific date and start time as well
    * `list_raw.sh` - simple script to list cloud storage where raw files are stored with a specific pattern
    * `less_than_7_etfs.sh` - old script to see whether load has failed for certainly day that resulted in not all 7 etfs are loaded
    * `count_dup.sh` - old command line version of BQ query to verify duplicate record counts in ark.holdings table


### web
Web interface built with `Dash framework` on `Google App Engine`.

* `app.py` - python code to create `Dash` app and server
* `apps` folder
    * `holdings.py` page for ark holdings
    * `changes.py` page for daily changes in ark holdings
* `main.py` - main page of web interface
* `core.py`
    * core backend logic to support data presented on web interface
    * filling up data in dropdown of all pages
    * Once selection is made (including the default selection while opening the first page), retrieve data from BigQuery tables and return data to frontend
* `app.yaml` - App Engine config file
    * `app_flex.yaml` - To deploy this app into flexible Google App Engine, override `app.yaml` using this file
    * `app_stand.yaml` - To deploy thsi app into standard Google App Engine, override `app.yaml` using this file.
        * By default `app.yaml` uses this standard config
* `assets` - folder for css file and Ark Invest logo
* `requirements.txt` - python libraries required to run this web interface


### zWIP (Working in progress)
This fodler contains some deprecated functions, temporary fixes and functions that are not yet running in production

#### data (pls ignore for now)
Some temporary scripts and data mostly for data fixes
* `fixes` - This folder contains data that's been fixed manually and some scripts related to it
* `tmp` - trades table related describe, schema etc. info

#### dedup
A full-fledged cloud function that remove duplicates records from ark.holdings table
* Still running on cloud function
* No longer really needed as the problem that would cause duplicate records has been fixed

#### gmail and oauth (Not working yet)
for gmail authentication to retrieve daily trade notification emails from ARK, not working yet.

