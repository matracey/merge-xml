""" Merge two XML files and output the merged data to a new XML file.
"""
import sys
from typing import List, Tuple


def parse_command_line_args() -> Tuple[str, str, List[str], str]:
    """Parse the command line arguments and return the file names, properties, and output file name.

    Returns:
        Tuple[str, str, List[str], str]: A tuple containing the file names, properties, and output file name.
    """
    if len(sys.argv) < 4:
        print("Usage: python3 merge_xml.py <file1> <file2> <property1> "
              "<property2> <property3> ... -o <output_file>")
        print("Example: python3 merge_xml.py file1.xml file2.xml id name -o "
              "merged.xml")
        sys.exit(1)

    f_1 = sys.argv[1]
    f_2 = sys.argv[2]
    props = sys.argv[3:]

    # Check if output file is specified
    if "-o" in props:
        # Get the index of '-o' and the next argument
        index = props.index("-o")
        # Get the output file name
        out = props[index + 1]
        # Remove '-o' and the output file name from the properties list
        props = props[:index] + props[index + 2:]
    else:
        out = "merged.xml"
    # Add 'id' property if not already present
    if 'id' not in props:
        props.append('id')
    return f_1, f_2, props, out


if __name__ == '__main__':
    # Parse the command line arguments
    file1, file2, properties, output_file = parse_command_line_args()
