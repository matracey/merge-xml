""" Merge two XML files and output the merged data to a new XML file.
"""
import logging
import sys
import os
from typing import List, Tuple
from defusedxml.ElementTree import parse


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


def parse_xml_files(
    f_1: str,
    f_2: str,
    props: List[str]
) -> Tuple[List[dict], List[dict]]:
    """Parse the XML files and return a list of dictionaries containing the specified properties.

    Args:
        f_1 (str): The name of the first XML file.
        f_2 (str): The name of the second XML file.
        props (List[str]): The list of properties to extract from each file.

    Returns:
        Tuple[List[dict], List[dict]]: A tuple containing the list of dictionaries for each file.
    """
    # Parse the XML files
    try:
        tree1 = parse(f_1)
        tree2 = parse(f_2)
    except FileNotFoundError as ex:
        logging.error("Error parsing XML files: %s", ex)
        sys.exit(1)

    # Extract the specified properties from the XML files
    data_1 = []
    data_2 = []
    for elem in tree1.getroot():
        data_1.append({prop: elem.find(prop).text for prop in props})
    for elem in tree2.getroot():
        data_2.append({prop: elem.find(prop).text for prop in props})
    return data_1, data_2


def validate_xml_data(d_1: List[dict], d_2: List[dict], props: List[str]) -> List[str]:
    """Validate the data from the XML files and ensure that it is valid.

    Args:
        data1_list (List[dict]): The data from the first XML file.
        data2_list (List[dict]): The data from the second XML file.
        properties_list (List[str]): The list of properties to extract from the XML files.
    """

    xml_errors = []

    # Check if the data from the XML files is valid
    if not d_1:
        xml_errors.append(
            "The first XML file is empty or could not be parsed.")
    if not d_2:
        xml_errors.append(
            "The second XML file is empty or could not be parsed.")
    for data in d_1:
        if not all(prop in data for prop in props):
            xml_errors.append(
                "The first XML file does not contain all of the specified properties.")
    for data in d_2:
        if not all(prop in data for prop in props):
            xml_errors.append(
                "The second XML file does not contain all of the specified properties.")
    return xml_errors


def merge_data(d_1: List[dict], d_2: List[dict], props: List[str]) -> List[dict]:
    """Merge the data from the two XML files, uniquely identifying each record using the specified properties.

    Args:
        d_1 (List[dict]): The data from the first XML file.
        d_2 (List[dict]): The data from the second XML file.
        props (List[str]): The list of properties that uniquely identify each record.

    Returns:
        List[dict]: The merged data.
    """
    # Merge the data based on the specified properties
    merged = set()
    for left in d_1:
        merged.add(tuple(left[prop] for prop in props))
    for right in d_2:
        # Check if the record already exists
        if tuple(right[prop] for prop in props) not in merged:
            merged.add(tuple(right[prop] for prop in props))
    # Convert the merged data back to a list of dictionaries
    return [dict(zip(props, record)) for record in merged]


if __name__ == '__main__':
    logger = logging.getLogger(__name__)

    # Parse the command line arguments
    file1, file2, properties, output_file = parse_command_line_args()

    # Validate the output file name
    errors = validate_output_filename(output_file)

    if not errors:
        # Parse the XML files
        data1, data2 = parse_xml_files(file1, file2, properties)

        # Validate the XML data
        errors = validate_xml_data(data1, data2, properties)

    if errors:
        for error in errors:
            logging.error(error)
        sys.exit(1)

    # Merge the data
    merged_data = merge_data(data1, data2, properties)
