"""
使用有道翻译,对每个指标进行翻译
这个密钥可能后面需要改
"""
import hashlib
import json
import time
import uuid
import requests


def addAuthParams(appKey, appSecret, params):
    q = params.get('q')
    if q is None:
        q = params.get('img')
    q = "".join(q)
    salt = str(uuid.uuid1())
    curtime = str(int(time.time()))
    sign = calculateSign(appKey, appSecret, q, salt, curtime)
    params['appKey'] = appKey
    params['salt'] = salt
    params['curtime'] = curtime
    params['signType'] = 'v3'
    params['sign'] = sign


def returnAuthMap(appKey, appSecret, q):
    salt = str(uuid.uuid1())
    curtime = str(int(time.time()))
    sign = calculateSign(appKey, appSecret, q, salt, curtime)
    params = {'appKey': appKey,
              'salt': salt,
              'curtime': curtime,
              'signType': 'v3',
              'sign': sign}
    return params


'''
    计算鉴权签名 -
    计算方式 : sign = sha256(appKey + input(q) + salt + curtime + appSecret)
    @param appKey    您的应用ID
    @param appSecret 您的应用密钥
    @param q         请求内容
    @param salt      随机值
    @param curtime   当前时间戳(秒)
    @return 鉴权签名sign
'''


def calculateSign(appKey, appSecret, q, salt, curtime):
    strSrc = appKey + getInput(q) + salt + curtime + appSecret
    return encrypt(strSrc)


def encrypt(strSrc):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(strSrc.encode('utf-8'))
    return hash_algorithm.hexdigest()


def getInput(input):
    if input is None:
        return input
    inputLen = len(input)
    return input if inputLen <= 20 else input[0:10] + str(inputLen) + input[inputLen - 10:inputLen]


# 您的应用ID
APP_KEY = '3e6d9cec768e7962'
# 您的应用密钥
APP_SECRET = 'D3t24XxOoibzakpO5zg6Iq3VWJwKKKyb'


def createRequest(eWord):
    '''
    note: 将下列变量替换为需要请求的参数
    '''
    q = eWord
    lang_from = 'en'
    lang_to = 'zh-CHS'

    data = {'q': q, 'from': lang_from, 'to': lang_to}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/api', header, data, 'post')
    # print(str(res.content, 'utf-8'))
    # 解析JSON字符串
    data = json.loads(str(res.content, 'utf-8'))

    # 获取translation字段的值
    translation = data['translation']

    # 打印translation的值
    # print(translation[0])
    time.sleep(1)
    print("成功睡眠10秒")
    return translation[0]

def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)

# 网易有道智云翻译服务api调用demo
# api接口: https://openapi.youdao.com/api
