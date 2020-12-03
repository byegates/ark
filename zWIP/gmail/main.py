request = {
  'labelIds': ['INBOX'],
  'topicName': 'projects/nw-msds498-ark-etf-analytics/topics/ark_trades'
}

gmail.users().watch(userId='me', body=request).execute()
