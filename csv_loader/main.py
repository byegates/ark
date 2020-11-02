import os
from google.cloud import bigquery
from dedup import dedup
import time

def csv_loader(data, context):
        client = bigquery.Client()
        dataset_id = os.environ['DATASET']
        dataset_ref = client.dataset(dataset_id)
        job_config = bigquery.LoadJobConfig()
        job_config.schema = [
                bigquery.SchemaField('Date', 'DATE'),
                bigquery.SchemaField('Fund', 'STRING'),
                bigquery.SchemaField('Company', 'STRING'),
                bigquery.SchemaField('Ticker', 'STRING'),
                bigquery.SchemaField('CUSIP', 'STRING'),
                bigquery.SchemaField('Shares', 'FLOAT'),
                bigquery.SchemaField('Market_Value', 'FLOAT'),
                bigquery.SchemaField('Weight', 'FLOAT'),
                ]
        job_config.skip_leading_rows = 1
        job_config.source_format = bigquery.SourceFormat.CSV

        # get the URI for uploaded CSV in GCS from 'data'
        uri = f"gs://{os.environ['BUCKET']}/{data['name']}"

        # lets do this
        load_job = client.load_table_from_uri(
                uri,
                dataset_ref.table(os.environ['TABLE']),
                job_config=job_config)

        print(f'Starting job: {load_job.job_id}')
        print(f"Function=csv_loader, Version={os.environ['VERSION']}")
        print(f"Loading file: {data['name']}")

        load_job.result()  # wait for table load to complete.
        print('Job finished.')

        destination_table = client.get_table(dataset_ref.table(os.environ['TABLE']))
        print(f"Table: {os.environ['TABLE']} now have {destination_table.num_rows} rows.")

        time.sleep(1)
        tbl = f"{dataset_id}.{os.environ['TABLE']}"
        dedup(tbl)


if __name__ == '__main__':
    csv_loader('', '')

