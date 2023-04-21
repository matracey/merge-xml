"""
Merge two XML files based on join properties and optionally output the merged data to a new XML file.
"""
import argparse
import re


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


def main() -> None:
    """
    Main function
    """
    # Parse the command line arguments
    args = parse_command_line_args()


if __name__ == '__main__':
    main()
