gcloud functions deploy dedup \
--runtime=python38 \
--trigger-http \
--allow-unauthenticated \
--entry-point=dedup \
--env-vars-file=env.yaml
