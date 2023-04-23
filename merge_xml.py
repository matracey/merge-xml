"""
Merge two XML files based on join properties and optionally output the merged data to a new XML file.
"""
import argparse
import os
import re
from typing import List, Tuple

from lxml import etree


class MergeStrategy:
    """
    MergeStrategy is an abstract class that defines the merge method.
    """
    def merge(self, left: etree._Element, right: etree._Element, join_properties: List[str]) -> etree._Element:
        """
        Merge two element trees based on join properties.
        """
        raise NotImplementedError


class LeftOuterJoinStrategy(MergeStrategy):
    """
    LeftOuterJoinStrategy is a concrete class that defines the merge method. It merges the two XML files using a left outer join strategy.
    """
    def merge(self, left: etree._Element, right: etree._Element, join_properties: List[str]) -> etree._Element:
        join_dict = {}
        for elem in right:
            join_key = tuple(elem.find(prop).text for prop in join_properties)
            join_dict[join_key] = elem
        for elem in left:
            join_key = tuple(elem.find(prop).text for prop in join_properties)
            join_elem = join_dict.get(join_key)
            if join_elem is not None:
                join_dict.pop(join_key)
        left.extend(join_dict.values())
        return left


class RightOuterJoinStrategy(MergeStrategy):
    """
    LeftOuterJoinnStrategy is a concrete class that defines the merge method. It merges the two XML files using a right outer join strategy.
    """
    def merge(self, left: etree._Element, right: etree._Element, join_properties: List[str]) -> etree._Element:
        join_dict = {}
        for elem in left:
            join_key = tuple(elem.find(prop).text for prop in join_properties)
            join_dict[join_key] = elem
        for elem in right:
            join_key = tuple(elem.find(prop).text for prop in join_properties)
            join_elem = join_dict.get(join_key)
            if join_elem is not None:
                join_dict.pop(join_key)
        right.extend(join_dict.values())
        return right


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


def validate_xml_data(l_data: etree._Element, l_schema: etree.XMLSchema, r_data: etree._Element, r_schema: etree.XMLSchema, join_props_xpath: List[str]) -> None:
    """
    Validate XML data

    Args:
        left_data (etree._Element): The XML data from the left file
        right_data (etree._Element): The XML data from the right file
        join_properties (List[str]): The properties to join on as xpath strings

    Raises:
        ValueError: If the XML schema does not match between the files
        ValueError: If the join properties do not match to at least one element in both left_data and right_data
    """
    errors = []
    # Test the left schema against the right data and vice versa
    if not l_schema.validate(r_data):
        errors.append('Left schema does not match right data')
    if not r_schema.validate(l_data):
        errors.append('Right schema does not match left data')
    # Test the join properties exist in both files
    for prop in join_props_xpath:
        left_prop = l_data.xpath(prop)
        right_prop = r_data.xpath(prop)
        if not left_prop or not right_prop:
            errors.append('Join property {prop} does not match to at least one element in both files')
    if errors:
        error_message = "\n\t".join(errors)
        raise ValueError(f"Invalid XML data: \n\n\t{error_message}")


def merge_data(left: etree._Element, right: etree._Element, join_properties: List[str], merge_strategy: MergeStrategy = LeftOuterJoinStrategy()) -> etree._Element:
    """Merge the data from the two XML files, uniquely identifying each record using the specified properties.

    Args:
        left_data (etree._Element): The XML data from the left file
        right_data (etree._Element): The XML data from the right file
        join_properties (List[str]): The properties to join on as xpath strings
        merge_strategy (MergeStrategy): The merge strategy to use. Defaults to LeftOuterJoinnStrategy.

    Returns:
        etree._Element: The merged XML data
    """
    return merge_strategy.merge(left, right, join_properties)


def write_merged_data_to_file(xml_data: etree._Element, output_file: str = None) -> None:
    """
    Write the merged data to the output file.

    Args:
        xml_data (etree._Element): The merged XML data
        output_file (str, optional): The output file path. Defaults to None.
    """
    # Write the merged data to the output file
    if output_file:
        try:
            with open(output_file, 'wb') as file:
                file.write(etree.tostring(
                    xml_data, encoding='utf-8', xml_declaration=True))
        except IOError as io_error:
            raise IOError(f'Unable to write to output file {output_file}') from io_error
    else:
        print(etree.tostring(xml_data, encoding='unicode'))


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
    # Validate the XML data
    validate_xml_data(left_data, left_schema, right_data, right_schema, args.join_properties)
    # Merge the data
    merged_data = merge_data(left_data, right_data, args.join_properties)
    # Write the merged data to the output file
    write_merged_data_to_file(merged_data, args.output)


if __name__ == '__main__':
    main()
