gcloud functions deploy ark-holdings-daily-pull \
--runtime=python38 \
--trigger-http \
--allow-unauthenticated \
--entry-point=ark_pull \
--env-vars-file=env.yaml
