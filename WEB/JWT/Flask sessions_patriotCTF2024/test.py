import requests
from requests.cookies import RequestsCookieJar

# Create a session
session = requests.Session()

# Create a RequestsCookieJar and add your cookie
# jar = RequestsCookieJar()
# jar.set('session', 'eJwdzjkSwjAMAMC_uE4h2dbhfCZjHR5oE1Ix_B2Gbst9l2OdeT3K_jrv3MrxjLKX5tqBGbq7MfmPiYi8aA7RAG8haZJoDZ0HrlSG6Oa1-yCqsaJNJlSVAQToNXsAt8UiFQBIbIa3bmYiarYyiEaNsUJjmlLZyn3l-c_Uzxf_2C6a.Cnf0yA.xIUSIFgcvjqwszrbwCA_D2Rqa5k', domain='localhost.local')

# # Assign the cookie jar to the session
# session.cookies = jar

# Make a request
response = session.get(url="http://127.0.0.1:9999/user1")
print(response.request.headers)

# Print the response
print(response.text)
