echo '\n--------------- DETAIL OF cloud function: ark-holdings-daily-pull ---------------\n'
gcloud functions describe  ark-holdings-daily-pull

echo '\n--------------- Deploying new verion of cloud function: ark-holdings-daily-pull ---------------\n'
gcloud functions deploy ark-holdings-daily-pull \
--runtime=python39 \
--trigger-http \
--allow-unauthenticated \
--entry-point=ark_pull \
--env-vars-file=env.yaml
