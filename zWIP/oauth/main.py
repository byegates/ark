import os

name = os.environ['META_NAME']
content = os.environ['CONTENT']

s = f"""
<html>
<head>
<meta name="{name}" content="{content}" />
<title> My title </title>
</head> 
<body>
page contents
</body>
</html>
"""


def html_tag(dummy):
    return s