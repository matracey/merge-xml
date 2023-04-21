"""
Merge two XML files based on join properties and optionally output the merged data to a new XML file.
"""
import argparse


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


def main() -> None:
    """
    Main function
    """
    # Parse the command line arguments
    args = parse_command_line_args()


if __name__ == '__main__':
    main()
