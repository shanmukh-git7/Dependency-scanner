import xml.etree.ElementTree as ET

def parse_pom(content: bytes):
    root = ET.fromstring(content)
    dependencies = root.findall(".//dependency")
    return dependencies
