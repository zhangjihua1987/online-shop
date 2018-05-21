import requests


def get_auth_url():
    weibo_auth_url = 'https://api.weibo.com/oauth2/authorize'
    client_id = 2723933757
    redirect_uri = 'http://47.106.173.70/complete/weibo/'
    get_auth_url = weibo_auth_url+'?client_id={client_id}&redirect_uri={redirect_uri}'.format(client_id=client_id, redirect_uri=redirect_uri)

    print(get_auth_url)


def get_token(code):
    weibo_token_url = 'https://api.weibo.com/oauth2/access_token'
    client_secret = '3412fd9b97015442f4ac992b99716029'
    grant_type = 'authorization_code'
    client_id = 2723933757
    redirect_uri = 'http://47.106.173.70/complete/weibo/'

    re_dict = requests.post(weibo_token_url, data={
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': grant_type,
        'code': code,
        'redirect_uri': redirect_uri
    })
    pass

# '{"access_token":"2.00bko_oB8b22yC638fb9058e078y9y","remind_in":"157679999","expires_in":157679999,"uid":"1659672953","isRealName":"true"}'


def get_token_info(token):
    re_dict = requests.post('https://api.weibo.com/oauth2/get_token_info', data={'access_token': token})
    pass

def get_user_info(token, uid):
    weibo_get_url = 'https://api.weibo.com/2/users/show.json'
    access_token = token
    uid = uid
    get_user_info_url = weibo_get_url+'?access_token={access_token}&uid={uid}'.format(access_token=access_token, uid=uid)
    print(get_user_info_url)


if __name__ == '__main__':
    # get_auth_url()
    # get_token(code='2d805edc13df27b2ef6057095102312c')
    # get_token_info(token='2.00bko_oB8b22yC638fb9058e078y9y')
    get_user_info(token='2.00bko_oB8b22yC638fb9058e078y9y', uid=1659672953)
