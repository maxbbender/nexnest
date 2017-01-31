from nexnest.application import oauth

twitter = oauth.remote_app('twitter',
                           base_url='https://api.twitter.com/1.1/',
                           request_token_url='https://api.twitter.com/oauth/request_token',
                           access_token_url='https://api.twitter.com/oauth/access_token',
                           authorize_url='https://api.twitter.com/oauth/authorize',
                           consumer_key='P6XBK2DKSdwUV7eWloQklXVUU',
                           consumer_secret='jCmQctecPPXrT4DWLCPkhU5Ixoouy42T0FJmsJRocI311uCvFA')
