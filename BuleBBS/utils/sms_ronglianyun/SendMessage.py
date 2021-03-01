import json

from utils.sms_ronglianyun.ronglian_sms_sdk import SmsSDK
accId = '8a216da8762cb4570176474929830953'
accToken = '1100e7946ff74b89ae4e435689113133'
appId = '8a216da8762cb457017647492a4c095a'

def send_message(mobile, image_code, ttl):
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'
    mobile = mobile
    datas = (image_code, ttl)
    resp = sdk.sendMessage(tid, mobile, datas)
    status = json.loads(resp)
    if status["statusCode"] == "000000":
        return 0
    return 1
# send_message(mobile='13753949664',
#              image_code='123456',
#              ttl = 5
#              )