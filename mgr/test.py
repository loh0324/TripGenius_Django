import requests,pprint

# 测试登录模块
payload = {
    'username': 'loh',
    'password': '123456'
}

response = requests.post('http://localhost:8000/api/mgr/signin', data=payload)

pprint.pprint(response.json())

import  requests,pprint

# 先登陆,获取sessionid
payload = {
        'username': 'loh',
        'password': '123456'
    }
response = requests.post('http://localhost:8000/api/mgr/signin', data=payload)


retDict = response.json()

sessionid = response.cookies['sessionid']

# 再发送列出请求，注意多了 pagenum 和 pagesize
payload = {
    'action': 'list_medicine',
    'pagenum': 1,
    'pagesize' : 3
}

response = requests.get('http://localhost:8000/api/mgr/medicines',
              params=payload,
              cookies={'sessionid': sessionid})

pprint.pprint(response.json())