import random
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

def send_sms(phone,code):
    client = AcsClient('LTAI4Fs7zksbXbguq7oE9bDm', 'uL7dMovhLMQ3bt0weqMQX0Yy9kp7G9', 'cn-hangzhou')

    code = "{'code':%s}"%(code)
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_body_params('PhoneNumbers',phone)
    request.add_body_params('SignName','月涵')
    request.add_body_params('TemplateCode','SMS_178985504')
    request.add_body_params('TemplateParam',code)

    response = client.do_action(request)

    print(str(response,encoding='utf-8'))

    return str(response,encoding='utf-8')


def get_code(n=6,alpha=True):
    s=''
    for i in range(n):
        num = random.randint(0,9)
        if alpha:
            upper_alpha = chr(random.randint(65,90))
            lower_alpha = chr(random.randint(97,122))
            num = random.choice([num,upper_alpha,lower_alpha])
        s=s+str(num)
    return s

if __name__ == '__main__':
    '''生成随机验证码: 数字表示生成几位, True表示生成带有字母的 False不带字母的'''
    a = get_code(6,False)
    send_sms('18235696161',a)
    print(a)
    print(get_code(6,False))
    print(get_code(6,True))
    print(get_code(4,False))
    print(get_code(4,True))
