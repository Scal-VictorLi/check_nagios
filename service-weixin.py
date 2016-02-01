import urllib.request
import json
import sys
def gettoken(corp_id,corp_secret):
    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corp_id + '&corpsecret=' + corp_secret
    try:
        token_file = urllib.request.urlopen(gettoken_url)
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))
    token_data = token_file.read().decode('utf-8')
    token_json = json.loads(token_data)
    token_json.keys()
    token = token_json['access_token']
    return token

def senddata(access_token,notify_str):
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
    notifydata = notify_str.split(",")
    user = notifydata[0]
    cationtype = notifydata[1]
    groupalias = notifydata[2]
    hostalias = notifydata[3]
    address = notifydata[4]
    desc = notifydata[5]
    state = notifydata[6]
    datatime = notifydata[7]
    output = notifydata[8]
    content = '***** 监控系统告警 *****\n\n 通知类型 : ' + cationtype + '\n 系统名称 : ' + groupalias + '\n 主机 : ' + hostalias + '\n 主机地址 : ' + address + '\n 监控点 : ' + desc + '\n 监控点状态 : ' + state + '\n 时间 : ' + datatime + '\n 信息 :\n ' + output + '\n'
    send_values = {
        "touser":user,
        "msgtype":"text",
        "agentid":"0",
        "text":{
            "content":content
            },
        "safe":"0"
        }
    send_data = json.dumps(send_values, ensure_ascii=False).encode(encoding='UTF8')

    send_request = urllib.request.Request(send_url, send_data)
    response = urllib.request.urlopen(send_request)
    msg = response.read()
    return msg

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
notifystr = str(sys.argv[1])
corpid = 'wxcbd83c2238619676'
corpsecret = 'NBQ8GcTE3mvPDKgPWOiox5_gr3EqdTeAy5vb_bG176ddb4zxZWxCaI1wLwpfWxVg'
accesstoken = gettoken(corpid,corpsecret)
msg = senddata(accesstoken,notifystr)
print(msg)
