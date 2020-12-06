pip freeze | sed '/pkg-resources==0.0.0/d' > requirements.txt
