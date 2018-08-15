from __future__ import absolute_import, unicode_literals
import os
from flask import Flask, request, abort
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.enterprise.exceptions import InvalidCorpIdException
from wechatpy.enterprise import parse_message, create_reply
from extools.solusVM import vmStatus, vmctl

TOKEN = os.getenv('WECHAT_TOKEN', '')
EncodingAESKey = os.getenv('WECHAT_ENCODING_AES_KEY', '')
CorpId = os.getenv('WECHAT_CORP_ID', '')
PORT = os.getenv('PORT', '5000')


app = Flask(__name__)

@app.route('/')
def index():
    return 'index'


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    crypto = WeChatCrypto(TOKEN, EncodingAESKey, CorpId)
    if request.method == 'GET':
    # 验证
        echo_str = request.args.get('echostr', '')
        try:
            echo_str = crypto.check_signature(
                signature,
                timestamp,
                nonce,
                echo_str
            )
        except InvalidSignatureException:
            abort(403)
        return echo_str
    else:
    # 接收消息
        try:
            msg = crypto.decrypt_message(
                request.data,
                signature,
                timestamp,
                nonce
            )
        except (InvalidSignatureException, InvalidCorpIdException):
            abort(403)
        msg = parse_message(msg)
        if msg.type == 'text':
            # 文本消息
            # reply = create_reply('点击下面的按钮进行操作!', msg).render()
            reply = text_action(msg)
        elif msg.type == 'event':
            # 按钮事件
            reply = click_action(msg)
        else:
            reply = create_reply('暂时不支持的消息类型!', msg).render()
        res = crypto.encrypt_message(reply, nonce, timestamp)
        return res 

def click_action(msg):
    action = msg.key
    if action == 'click001':
        vps_info = vmStatus()
        hdd = vps_info['hdd']
        hdd_usage = hdd.split(',')[3]
        bw = vps_info['bw']
        bw_usage = bw.split(',')[3]
        vmstat = vps_info['vmstat']
        ret_msg = "主机状态: {}\n带宽已使用: {}% \n磁盘已使用: {}%".format(vmstat,bw_usage,hdd_usage)
        rep = create_reply(ret_msg, msg).render()
    elif action == 'click002':
        rep = create_reply('通过API获取VPS面板信息.', msg).render()
    elif action in ["boot", "shutdown", "reboot"]:
        print(action)
        vmctl(action)
        rep = create_reply("操作成功, 稍后刷新状态查看", msg).render()
    return rep

def text_action(msg):
    action = msg.content
     
    if action.startswith('sc'):
        # 控制服务指令
        ret = create_reply('服务控制 {}'.format(action), msg).render()
    else:
        ret = create_reply('未能识别的指令', msg).render()
    return ret

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
