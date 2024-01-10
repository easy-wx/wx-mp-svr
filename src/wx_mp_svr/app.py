import os
from flask import Flask, request

from wx_crypt import WXBizMsgCrypt, WxChannel_Mp
import xml.etree.cElementTree as ET

from .req_msg import WxReqMsg


def _encode_rsp(wx_cpt, msg):
    # 加密消息
    params = request.args
    timestamp = params.get("timestamp")
    nonce = params.get("nonce")
    ret, rsp = wx_cpt.EncryptMsg(msg.dump_xml(), nonce, timestamp)
    if ret != 0:
        print("err: encrypt fail: " + str(ret))
    return rsp


class WxMpSvr(object):

    def __init__(self, name, host, port, path, token=None, aes_key=None, appid=None):
        self.host = host
        self.port = port
        self.path = path
        self._token = token if token is not None else os.getenv("WX_MP_TOKEN")
        self._aes_key = aes_key if aes_key is not None else os.getenv("WX_MP_AES_KEY")
        self._appid = appid if appid is not None else os.getenv("WX_MP_APPID")
        self._app = Flask(name)
        self._message_handler = None
        self._event_handler = None
        self._error_handler = None

    def set_message_handler(self, handler):
        self._message_handler = handler

    def set_event_handler(self, handler):
        self._event_handler = handler

    def set_error_handler(self, handler):
        self._error_handler = handler

    def set_flask_error_handler(self, handler):
        self._app.errorhandler(Exception)(handler)

    def run(self):
        if self._message_handler is None:
            raise Exception("message handler is not set")
        if self._event_handler is None:
            raise Exception("event handler is not set")
        self._app.get(self.path)(self.handle_call_get)
        self._app.post(self.path)(self.handle_call_post)
        self._app.run(host=self.host, port=self.port)

    def get_crypto_obj(self):
        return WXBizMsgCrypt(self._token, self._aes_key, self._appid, WxChannel_Mp)

    def handle_call_get(self):
        # 获取请求参数
        params = request.args
        msg_signature = params.get("signature")
        timestamp = params.get("timestamp")
        nonce = params.get("nonce")
        encrypted_echo_str = params.get("echostr")
        wx_cpt = self.get_crypto_obj()
        ret, decrypted_echo_str = wx_cpt.VerifyURL(
            msg_signature, timestamp, nonce, encrypted_echo_str
        )
        if ret != 0:
            return None
        return decrypted_echo_str

    def handle_call_post(self):
        # 获取请求参数
        params = request.args
        msg_signature = params.get("signature")
        timestamp = params.get("timestamp")
        nonce = params.get("nonce")
        wx_cpt = self.get_crypto_obj()

        # 解密出明文的echostr
        ret, xml_content = wx_cpt.DecryptMsg(
            request.data, msg_signature, timestamp, nonce
        )
        if ret != 0:
            if self._error_handler:
                self._error_handler(ret)
            else:
                return None
            # 获取所有的查询参数

        # 解密后的数据是xml格式，用python的标准库xml.etree.cElementTree可以解析
        xml_tree = ET.fromstring(xml_content)
        req_msg = WxReqMsg.create_msg(xml_tree)
        if req_msg.msg_type == "event":
            rsp_msg = self._event_handler(req_msg)
        else:
            rsp_msg = self._message_handler(req_msg)

        return _encode_rsp(wx_cpt, rsp_msg)
