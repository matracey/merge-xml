# merge_xml.py

## Introduction

`merge_xml.py` is a simple script that merges two XML files based on the specified properties.

## Purpose

The purpose of `merge_xml.py` is to provide a simple way to merge two XML files based on common properties. This can be useful when you have two separate data sources that you need to combine into a single file.

## Installation

To install `merge_xml.py`, you'll need Python 3.6+ and the `defusedxml` library. You can install `defusedxml` using pip:

```bash
pip install defusedxml
```

or you can use requirements.txt:

```bash
pip install -r requirements.txt
```

## Usage

To run `merge_xml.py`, use the following command:

```python
python merge_xml.py <file1> <file2> <property1> <property2> <property3> ... -o <output_file>
```

Here's an example:

```python
python merge_xml.py file1.xml file2.xml id name -o output.xml
```

## Expected Input and Output

`merge_xml.py` expects two input files in XML format, as well as a list of properties to merge on. If no properties are specified, the script will merge on the `id` property. The output file will also be in XML format, with the merged data. If no output file is specified, the file will be saved as `output.xml`.

## Limitations

`merge_xml.py` may have some limitations that I'm not aware of. I have only tested it for my own use cases, so if you encounter any issues, please raise a pull request or create an issue.

## Troubleshooting

If you encounter issues while running `merge_xml.py`, there are a few things you can try. First, make sure that your input files are in the correct format and that you have specified the correct properties to merge on.

## Testing

`merge_xml.py` includes a suite of unit tests to ensure that it works as expected. To run the tests, use the following command:

```python
python -m unittest test_merge_xml.py
```

This will run all of the tests and output the results.

## Contributing

If you'd like to contribute to `merge_xml.py`, please fork the repository and create a pull request.

## License

`merge_xml.py` is licensed under the MIT License. See `LICENSE` for more information.
