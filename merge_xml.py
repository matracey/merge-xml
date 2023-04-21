""" Merge two XML files and output the merged data to a new XML file.
"""
import logging
import sys
import os
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


def validate_output_filename(out_file: str) -> List[str]:
    """Validate the output file name and ensure that it is valid and doesn't already exist.

    Args:
        out_file (str): The name of the output file.

    Returns:
        List[str]: A list of error messages if the output file name is invalid or already exists, an empty list otherwise.
    """
    # List of invalid characters for Windows, Linux and Mac
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    # List of errors
    file_errors = []

    # Check if the output file name contains any invalid characters
    if any(char in out_file for char in invalid_chars):
        file_errors.append(
            "Please ensure the output file name doesn't contain any invalid characters.")
    # Check if the output file name has the .xml extension
    if not out_file.endswith(".xml"):
        file_errors.append(
            "Please ensure the output file name has the .xml extension.")
    # Check that the output file doesn't already exist
    if os.path.exists(out_file):
        file_errors.append(
            "Please ensure the output file doesn't already exist.")
    # Return the list of errors
    return file_errors


if __name__ == '__main__':
    logger = logging.getLogger(__name__)

    # Parse the command line arguments
    file1, file2, properties, output_file = parse_command_line_args()

    # Validate the output file name
    errors = validate_output_filename(output_file)
    if errors:
        for error in errors:
            logging.error(error)
        sys.exit(1)
