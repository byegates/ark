gcloud functions describe  ark-holdings-daily-pull

gcloud functions deploy ark-holdings-daily-pull \
--runtime=python39 \
--trigger-http \
--allow-unauthenticated \
--entry-point=ark_pull \
--env-vars-file=env.yaml
