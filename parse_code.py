import xml.etree.ElementTree as ET
from typing import TextIO

# --- load the file -----------------------------------------------------------
tree = ET.parse('xml_uscAll@119-23not21/usc01.xml')
root = tree.getroot()

# --- DFS helper --------------------------------------------------------------
def dfs(elem: ET.Element, depth: int = 0, file_handle: TextIO | None = None) -> None:
    tag = elem.tag.split('}')[-1]  # strip namespace

    if tag == 'section':
        # Extract <num> and <heading>
        num_elem = elem.find('.//{*}num')
        heading_elem = elem.find('.//{*}heading')

        num_text = num_elem.text.strip() if num_elem is not None and num_elem.text else ''
        heading_text = heading_elem.text.strip() if heading_elem is not None and heading_elem.text else ''

        if file_handle is not None:
            file_handle.write(f"{num_text} {heading_text}\n")

        # Find the <content> element
        content = elem.find('.//{*}content')
        if content is not None:
            for p in content.iter():
                if p.tag.split('}')[-1] == 'p' and p.text and p.text.strip():
                    para_text = p.text.strip()
                    if file_handle is not None:
                        file_handle.write(f"{para_text}\n")

    # Continue DFS regardless of tag
    for child in elem:
        dfs(child, depth + 1, file_handle=file_handle)


# --- run it ------------------------------------------------------------------
with open('title1.txt', 'w', encoding='utf-8') as f:
    dfs(root, file_handle=f)
