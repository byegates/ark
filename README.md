# ark Invest Holdings Tracking and Analytics
Ark Invest holdings tracking and analytics app built on GCP (Google Cloud Platform). This is pretty much a learning project.

## Overview

### `csv_loader`
* a GCP Cloud function
    * Trigger: a new (including overrides) csv file uploaded to a specific cloud storage location (`nw-msds498-ark-etf-analytics`)
    * This function does one task: load the csv file (Ark Invest daily holding, specific format) to BigQuery table: `ark.holdings`
    * `env.yaml` - environment variables for cloud function
    * `main.py` - function source code
    * `requirement.txt` - python libraries required to run this function, for GCP cloud function's reference to run this function


### pdf
* One-off function to convert Ark Invest's PDF format daily holding file to csv format, then load it to cloud storage. 
* csv file uploaded to cloud storage will automatically trigger the `csv_loader` function to load the file to BigQuery
* `docs` - this folder contains pdf files to be read
* `csv` - Folder for converted csv files
    * `2020-11-13/upload.sh` - script to upload converted csvs to cloud storage
* `main.py` - python script for pdf to csv conversion using `tabula` and `pandas` library

### `price.py`

#### `cli`
* `ixe.py` - core functions to get minute price and day price information using `iexcloud API` via `iexfinance` python library

#### `get_price.py`
* Right now just a shell function to call `cli/iex.py', need it outside to make import of other lib easier

#### `mergedf.py`
One-off function to merge mulitple csv file in the same format into one. With simple statistic and error logging

#### `day_price`
* temporarily store intermediate files for processing and uploading history day price files 
* some logs
* `load.sh` upload files that with name in specific pattern to cloud storage then load them from cloud storage to BigQuery
    * Can delete and re-create table from BigQuery as needed
* `mkdef` - create a table schema for reference from csv file
* `rename.sh` one off shell script to rename some files produced before
* `upload.sh` bulk upload files to cloud storage

#### `min_price`
* `data`, `logs` folder, self-explainatory
* `get_trade_days.py` use `pandas_market_calendars` library to get trade days between date range
* `load.sh`
    * remove BigQuery table to be loaded (Optional)
* `upload_n_load.sh`
    * local --> cloud storage --> BigQuery
    * takes in month arguments
* `upload.sh` - simple cloud storage upload scripts

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
* `price.py` - WIP, retrieve and calculate price to support holding change page trading sizes information
* `app.yaml` - App Engine config file
    * `app_flex.yaml` - To deploy this app into flexible Google App Engine, override `app.yaml` using this file
    * `app_stand.yaml` - To deploy thsi app into standard Google App Engine, override `app.yaml` using this file.
        * By default `app.yaml` uses this standard config
* `assets` - folder for css file and Ark Invest logo
* `bkup.py` - old single page app's `main.py`, deprecated
* `requirements.txt` - python libraries required to run this web interface, `Google App Engine` use this to config runtime env.


### zWIP (Working in progress or not longer valid)
This fodler contains some deprecated functions, temporary fixes and functions that are not yet running in production

#### data (pls ignore for now)
* Some temporary scripts and data mostly for data fixes
* `fixes` - This folder contains data that's been fixed manually and some scripts related to it
* `tmp` - trades table related describe, schema etc. info

#### dedup
* A full-fledged cloud function that remove duplicates records from ark.holdings table
* Still running on cloud function
* But no longer really needed as the problem that would cause duplicate records has been fixed

#### gmail and oauth (Not working yet)
* for gmail authentication to retrieve daily trade notification emails from ARK, not working yet.

