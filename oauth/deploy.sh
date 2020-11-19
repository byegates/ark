gcloud functions deploy htmltag \
--runtime=python38 \
--trigger-http \
--allow-unauthenticated \
--entry-point=html_tag \
--env-vars-file=env.yaml
