# https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_standard_messages.html

from .utils import get_xml_element
import xml.etree.cElementTree as ET


class WxReqMsg(object):
    def __init__(self, xml_tree):
        self.to_user_name = get_xml_element(xml_tree, "ToUserName")
        self.from_user_name = get_xml_element(xml_tree, "FromUserName")
        self.create_time = get_xml_element(xml_tree, "CreateTime")
        self.msg_type = get_xml_element(xml_tree, "MsgType")
        self.msg_id = get_xml_element(xml_tree, "MsgId")
        self.msg_data_id = get_xml_element(xml_tree, "MsgDataId")
        self.idx = get_xml_element(xml_tree, "Idx")
        self.xml_tree = xml_tree

    def __str__(self):
        return ET.tostring(self.xml_tree, encoding="utf-8", method="html").decode("utf-8")

    @staticmethod
    def create_msg(xml_tree=None, msg_type=None):
        if xml_tree is None:
            xml_tree = ET.fromstring("<xml></xml>")
        default_msg_type = get_xml_element(xml_tree, "MsgType")
        if msg_type is None:
            msg_type = default_msg_type
        else:
            xml_tree.find("MsgType").text = msg_type

        if msg_type == "text":
            return TextReqMsg(xml_tree)
        elif msg_type == "image":
            return ImageReqMsg(xml_tree)
        elif msg_type == "voice":
            return VoiceReqMsg(xml_tree)
        elif msg_type == "video":
            return VideoReqMsg(xml_tree)
        elif msg_type == "shortvideo":
            return ShortVideoReqMsg(xml_tree)
        elif msg_type == "location":
            return LocationReqMsg(xml_tree)
        elif msg_type == "link":
            return LinkReqMsg(xml_tree)
        elif msg_type == "event":
            return EventReqMsg(xml_tree)
        else:
            raise Exception("unknown msg type")


class TextReqMsg(WxReqMsg):
    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.content = get_xml_element(xml_tree, "Content")


class ImageReqMsg(WxReqMsg):
    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.pic_url = get_xml_element(xml_tree, "PicUrl")
        self.media_id = get_xml_element(xml_tree, "MediaId")


class VoiceReqMsg(WxReqMsg):
    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.media_id = get_xml_element(xml_tree, "MediaId")
        self.format = get_xml_element(xml_tree, "Format")
        self.recognition = get_xml_element(xml_tree, "Recognition")


class VideoReqMsg(WxReqMsg):
    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.media_id = get_xml_element(xml_tree, "MediaId")
        self.thumb_media_id = get_xml_element(xml_tree, "ThumbMediaId")


class ShortVideoReqMsg(WxReqMsg):
    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.media_id = get_xml_element(xml_tree, "MediaId")
        self.thumb_media_id = get_xml_element(xml_tree, "ThumbMediaId")


class LocationReqMsg(WxReqMsg):
    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.location_x = get_xml_element(xml_tree, "Location_X")
        self.location_y = get_xml_element(xml_tree, "Location_Y")
        self.scale = get_xml_element(xml_tree, "Scale")
        self.label = get_xml_element(xml_tree, "Label")


class LinkReqMsg(WxReqMsg):
    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.title = get_xml_element(xml_tree, "Title")
        self.description = get_xml_element(xml_tree, "Description")
        self.url = get_xml_element(xml_tree, "Url")


class EventReqMsg(WxReqMsg):
    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.event = get_xml_element(xml_tree, "Event")
        self.event_key = get_xml_element(xml_tree, "EventKey")
