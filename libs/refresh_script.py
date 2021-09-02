#coding:utf-8
import requests,sys

###加入crontab

# #结算资产价值
# 0 5 25 * * /usr/bin/python /usr/share/nginx/wzhl_oa/libs/refresh_script.py assets_refresh
#
# #刷新假日
# 0 10 * * * /usr/bin/python /usr/share/nginx/wzhl_oa/libs/refresh_script.py vacation_refresh

username = 'refresh_user'
password = 'MTFkNzJkYjkyM2Ji'

path = sys.argv[1]

def refresh(path):
    s = requests.session()
    payload = {'username':username,'password':password}
    #print payload
    headers = {'content-type':'application/json'}
    r = s.post('http://oa.xiaoquan.com:10000/login_auth/',data=payload,headers=headers)
    cookies = r.cookies
    s.post('http://oa.xiaoquan.com:10000/%s/' % path,cookies=cookies)

refresh(path)