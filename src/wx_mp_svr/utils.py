import xml.etree.cElementTree as ET


def get_xml_element(xml_tree, name):
    if xml_tree.find(name) is None:
        e = ET.Element(name)
        e.text = ""
        xml_tree.insert(0, e)
    return xml_tree.find(name).text
