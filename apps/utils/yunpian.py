import requests
import json


class YunPian(object):
    def __init__(self, api_key):

        # api_key为云片apikey
        self.api_key = api_key

        # url为云片发送单短信发送url
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):

        # 填入必填信息，书写格式固定
        params = {
            "apikey": self.api_key,
            "mobile": mobile,

            # 这里必须是审核通过的模版，否则不能通过验证
            "text": "【慕学生鲜】您的验证码是%s。如非本人操作，请忽略本短信" % code
        }

        # 接收云片返回的json信息
        response = requests.post(self.single_send_url, data=params)

        # 将json信息loads为dict返回
        re_msg = json.loads(response.text)
        return re_msg
