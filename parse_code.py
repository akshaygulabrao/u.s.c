import xml.etree.ElementTree as ET
from typing import TextIO
from pathlib import Path

# --- DFS helper --------------------------------------------------------------
def dfs(elem: ET.Element, depth: int, file_handle: TextIO | None, inside_section: bool = False) -> None:
    tag = elem.tag.split('}')[-1]

    if tag == 'section':
        num_elem = elem.find('.//{*}num')
        heading_elem = elem.find('.//{*}heading')

        num_text = num_elem.text.strip() if num_elem is not None and num_elem.text else ''
        heading_text = heading_elem.text.strip() if heading_elem is not None and heading_elem.text else ''

        if file_handle is not None:
            file_handle.write(f"{num_text} {heading_text}\n")

        for child in elem:
            child_tag = child.tag.split('}')[-1]
            if child_tag in {'subsection', 'paragraph', 'content', 'p'}:
                write_element(child, depth + 1, file_handle, inside_section=True)
    else:
        for child in elem:
            dfs(child, depth, file_handle, inside_section=False)

# --- helper to write indented content ----------------------------------------
def write_element(elem: ET.Element, depth: int, file_handle: TextIO | None, inside_section: bool = False) -> None:
    tag = elem.tag.split('}')[-1]
    indent = '    ' * depth

    num_elem = elem.find('.//{*}num')
    heading_elem = elem.find('.//{*}heading')

    num_text = num_elem.text.strip() if num_elem is not None and num_elem.text else ''
    heading_text = heading_elem.text.strip() if heading_elem is not None and heading_elem.text else ''

    if not inside_section and (num_text or heading_text):
        if file_handle is not None:
            file_handle.write(f"{indent}{num_text} {heading_text}\n")
    elif inside_section and heading_text:
        if file_handle is not None:
            file_handle.write(f"{indent}{heading_text}\n")

    if elem.text and elem.text.strip():
        if file_handle is not None:
            file_handle.write(f"{indent}{elem.text.strip()}\n")

    for child in elem:
        write_element(child, depth + 1, file_handle, inside_section=inside_section)

# --- main processing function -------------------------------------------------
def process_usc_title(title_num: int,
                      xml_dir: str | Path = "xml_uscAll@119-23not21",
                      out_dir: str | Path = ".") -> None:
    """
    Parse the XML file for a given U.S. Code title and write a flattened
    text representation.

    Parameters
    ----------
    title_num : int
        The numeric identifier of the title (e.g., 34).
    xml_dir : str | Path, optional
        Directory containing the XML files (default: "xml_uscAll@119-23not21").
    out_dir : str | Path, optional
        Directory where the output .txt file will be written (default: ".").

    Raises
    ------
    FileNotFoundError
        If the expected XML file does not exist.
    """
    xml_dir = Path(xml_dir)
    out_dir = Path(out_dir)

    input_file = xml_dir / f"usc{title_num:02d}.xml"
    output_file = out_dir / f"usc{title_num:02d}.txt"

    if not input_file.is_file():
        raise FileNotFoundError(input_file)

    tree = ET.parse(input_file)
    root = tree.getroot()

    out_dir.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        dfs(root, depth=0, file_handle=f)

# --- run it ------------------------------------------------------------------
if __name__ == "__main__":
    for title_num in range(1,55):
        # weird exceptions
        if title_num == 53: continue
        process_usc_title(title_num)