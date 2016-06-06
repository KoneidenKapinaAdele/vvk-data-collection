
import sys, json

from oauth import oauth
from config import public_key, private_key, token, token_secret
from requests import get

consumer = oauth.OAuthConsumer(public_key, private_key)
token = oauth.OAuthToken(token, token_secret)

def request(url):
    url = 'http://api.telldus.com/json/' + url
    oauth_req = oauth.OAuthRequest.from_consumer_and_token(consumer,
            token=token, http_method='GET', http_url=url)
    oauth_req.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(),
            consumer, token)
    headers = oauth_req.to_header()
    return get(url, headers=headers).json()

if __name__ == '__main__':
    result = request(sys.argv[1])
    json.dump(result, sys.stdout, sort_keys=True,
            indent=4, separators=(',', ': '))
    print()

