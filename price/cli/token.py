def get_token(fi='dont.mess.with.me'):
    with open(fi, 'r') as f:
        return f.readline().strip()


t = get_token()