"""
Merge two XML files based on join properties and optionally output the merged data to a new XML file.
"""
import argparse
import os
import re
from typing import List, Tuple

from lxml import etree


def parse_command_line_args() -> argparse.Namespace:
    """Parse the command line arguments and return the file names, properties, and output file name.

    Returns:
        argparse.Namespace: The parsed command line arguments
    """

    parser = argparse.ArgumentParser(description='Merge two XML files based on join properties')
    # Required left file, right file, and join properties
    parser.add_argument('left_file', help='Path to the left XML file')
    parser.add_argument('right_file', help='Path to the right XML file')
    parser.add_argument('join_properties', nargs='+', help='List of join properties as xpath strings')
    # Optional output file name
    parser.add_argument('-o', '--output', help='Path to the output XML file', default=None)

    return parser.parse_args()


def validate_output_filename(out_path: str) -> None:
    """Validate the output file name and ensure that it is valid, writable and doesn't already exist.

    Args:
        out_file (str): The output file path

    Raises:
        ValueError: If the output file name is invalid or already exists
    """

    # Check if the output file name contains any invalid characters
    if not is_valid_filename(out_path):
        raise ValueError("The output file name contains invalid characters.")

    # Check if the output file name has the .xml extension
    if not has_xml_extension(out_path):
        raise ValueError("The output file name must have the .xml extension.")

    # Check that the output file doesn't already exist
    if file_exists(out_path):
        raise ValueError("The output file already exists.")

    # Check that the output directory is writable
    if not is_writable_directory(os.path.dirname(out_path)):
        raise ValueError("The output directory is not writable.")


def is_valid_filename(filename: str) -> bool:
    """Check if the filename contains any invalid characters.

    Args:
        filename (str): The filename to check

    Returns:
        bool: True if the filename is valid, False otherwise
    """
    return re.compile(r"[^*?<>|]+").fullmatch(filename) is not None


def has_xml_extension(filename: str) -> bool:
    """Check if the filename has the .xml extension.

    Args:
        filename (str): The filename to check

    Returns:
        bool: True if the filename has the .xml extension, False otherwise
    """
    return filename.endswith(".xml")


def file_exists(filepath: str) -> bool:
    """Check if the file already exists.

    Args:
        filepath (str): The file path to check

    Returns:
        bool: True if the file exists, False otherwise
    """
    return os.path.exists(filepath)


def is_writable_directory(directory: str) -> bool:
    """Check if the directory is writable.

    Args:
        directory (str): The directory to check

    Returns:
        bool: True if the directory is writable, False otherwise
    """
    return os.access(directory, os.W_OK)


def validate_props_xpath(props_xpath: List[str]) -> None:
    """
    Checks that each xpath string is valid using lxml.
    If not, throws an error listing each invalid xpath string.
    """
    invalid_props = []
    for prop in props_xpath:
        try:
            etree.XPath(prop)
        except etree.XPathSyntaxError as ex:
            invalid_props.append(f"{prop}: {ex}")
    if invalid_props:
        error_message = "\n".join(invalid_props)
        raise ValueError(f"The following xpath strings are invalid:\n\n{error_message}")


def parse_xml_files(xml_file: str) -> Tuple[etree._Element, etree.XMLSchema]:
    """
    Parse XML file that returns a tuple of the root element and the schema
    """
    parser = etree.XMLParser(resolve_entities=False, strip_cdata=False)
    tree = etree.parse(xml_file, parser=parser)
    schema_root = etree.XMLSchema(tree)
    root = tree.getroot()
    return root, schema_root


def main() -> None:
    """
    Main function
    """
    # Parse the command line arguments
    args = parse_command_line_args()
    # Normalize the output file name if it is provided
    if args.output is not None:
        args.output = os.path.abspath(os.path.normpath(args.output))
    # Validate the output file name
    validate_output_filename(args.output)
    # Validate the xpath strings
    validate_props_xpath(args.join_properties)
    # Parse the XML files
    left_data, left_schema = parse_xml_files(args.left_file)
    right_data, right_schema = parse_xml_files(args.right_file)


if __name__ == '__main__':
    main()
