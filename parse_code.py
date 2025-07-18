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

        # Process subsections and content
        for child in elem:
            child_tag = child.tag.split('}')[-1]
            if child_tag in {'subsection', 'paragraph', 'content', 'p'}:
                write_element(child, depth + 1, file_handle)

    else:
        # Continue DFS for non-section elements
        for child in elem:
            dfs(child, depth, file_handle)

# --- helper to write indented content ----------------------------------------
def write_element(elem: ET.Element, depth: int, file_handle: TextIO | None) -> None:
    tag = elem.tag.split('}')[-1]
    indent = '    ' * depth

    # Handle <num> and <heading> for subsections/paragraphs
    num_elem = elem.find('.//{*}num')
    heading_elem = elem.find('.//{*}heading')

    num_text = num_elem.text.strip() if num_elem is not None and num_elem.text else ''
    heading_text = heading_elem.text.strip() if heading_elem is not None and heading_elem.text else ''

    if num_text or heading_text:
        if file_handle is not None:
            file_handle.write(f"{indent}{num_text} {heading_text}\n")

    # Handle direct text in <content> or <p>
    if elem.text and elem.text.strip():
        if file_handle is not None:
            file_handle.write(f"{indent}{elem.text.strip()}\n")

    # Recurse into children
    for child in elem:
        write_element(child, depth + 1, file_handle)

# --- run it ------------------------------------------------------------------
with open('title1.txt', 'w', encoding='utf-8') as f:
    dfs(root, file_handle=f)