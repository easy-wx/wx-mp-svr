from wx_mp_svr import Server, WxMpReqMsg, WxMpRspMsg  # 从wx_mp_svr包中导入Server类


def main():
    token = "xxx"
    aes_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    appid = "YOUR_OWN_APP_ID"
    host = "127.0.0.1"
    port = 5001
    server = Server(
        "wx_svr", host, port, "/wx_mp_svr", token=token, aes_key=aes_key, appid=appid
    )

    def msg_handler(req_msg: WxMpReqMsg) -> WxMpRspMsg:
        # 简单的echo
        if req_msg.msg_type in ["text", "image", "voice"]:
            rsp_msg = WxMpRspMsg.create_msg(req_msg.msg_type)
            rsp_msg.to_user_name = req_msg.from_user_name
            rsp_msg.from_user_name = req_msg.to_user_name
            if req_msg.msg_type == "text":
                rsp_msg.content = req_msg.content
            elif req_msg.msg_type == "image":
                rsp_msg.media_id = req_msg.media_id
            elif req_msg.msg_type == "voice":
                rsp_msg.media_id = req_msg.media_id
        else:
            rsp_msg = WxMpRspMsg.create_msg("text")
            rsp_msg.to_user_name = req_msg.from_user_name
            rsp_msg.from_user_name = req_msg.to_user_name
            rsp_msg.content = "暂不支持ECHO的消息类型"

        return rsp_msg

    def event_handler(req_msg):
        rsp_msg = WxMpRspMsg.create_msg("text")
        rsp_msg.to_user_name = req_msg.from_user_name
        rsp_msg.from_user_name = req_msg.to_user_name
        rsp_msg.content = '欢迎关注【<a href="https://wlbcoder.com">老白码农在奋斗</a>】'
        return rsp_msg

    server.set_message_handler(msg_handler)
    server.set_event_handler(event_handler)
    server.run()


if __name__ == "__main__":
    main()
