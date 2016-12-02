from zeus import client

USER_TOKEN = "747oiktknkxj6ww3j94ulfmcno6dixwt"
LOG_NAME = "gbos1"

z = client.ZeusClient(USER_TOKEN, 'https://data04.ciscozeus.io')

logs = [
    {"message": "My Test Log"},
    {"message": "My Second Test Log"}
]
t = z.sendLog(LOG_NAME,logs)
#
# z.getLog(LOG_NAME,
#           pattern='*',
#           from_date=123456789,
#           to_date=126235344235,
#           offset=23,
#           limit=10)
#
