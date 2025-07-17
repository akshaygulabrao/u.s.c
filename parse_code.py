import xml.etree.ElementTree as ET
from typing import TextIO

# --- load the file -----------------------------------------------------------
tree = ET.parse('xml_uscAll@119-23not21/usc01.xml')
root = tree.getroot()

# --- DFS helper --------------------------------------------------------------
def dfs(elem: ET.Element, depth: int = 0, file_handle: TextIO | None = None) -> None:
    if any('identifier' in k.lower() for k in elem.attrib):
        indent: str = '  ' * depth
        tag: str = elem.tag.split('}')[-1]          # strip namespace
        if file_handle is not None:
            file_handle.write(f"{indent}<{tag}>  {elem.attrib}\n")

    child: ET.Element
    for child in elem:
        dfs(child, depth + 1, file_handle)

# --- run it ------------------------------------------------------------------
with open('output.txt', 'w', encoding='utf-8') as f:
    dfs(root, file_handle=f)
