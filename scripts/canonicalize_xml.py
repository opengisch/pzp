#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A pre-commit hook script to canonicalize XML files using lxml.etree.c14n().

This script ensures XML files are in a canonical form for consistent source control.
"""

import os
import sys

from lxml import etree


def canonicalize_file(filepath):
    """
    Canonicalizes a single XML file in-place.

    Args:
        filepath (str): The path to the XML file.

    Returns:
        bool: True if the file was canonicalized and modified, False otherwise.
              Returns None if an error occurred during processing.
    """
    try:
        # Parse the XML file.
        parser = etree.XMLParser()
        tree = etree.parse(filepath, parser)

        # Generate the DESIRED canonical output from the parsed tree.
        desired_canonical_output = etree.tostring(tree, method="c14n")

        # WORKAROUND: Add a single trailing newline to the canonical output.
        # This ensures compatibility with tools like 'end-of-file-fixer'.
        if not desired_canonical_output.endswith(b"\n"):
            desired_canonical_output += b"\n"

        # Read the CURRENT content of the file from disk (raw bytes).
        with open(filepath, "rb") as f:
            current_file_content = f.read()

        # Compare the DESIRED canonical output  with the CURRENT file content.
        # If they are identical, the file is already in the desired canonical form, and no write is needed.
        if current_file_content == desired_canonical_output:
            print(f"'{filepath}' is already canonical and has correct EOF. No changes needed.")
            return False  # File was not modified

        # If they differ, write the DESIRED canonical output back to the file.
        with open(filepath, "wb") as f:
            f.write(desired_canonical_output)

        print(f"Canonicalized and fixed EOF for '{filepath}'.")
        return True  # File was modified

    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML file '{filepath}': {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred while processing '{filepath}': {e}", file=sys.stderr)
        return None


def main():
    """
    Main function to process XML files provided as command-line arguments.
    """
    if len(sys.argv) < 2:
        print("Usage: canonicalize_xml.py <file1.xml> [file2.xml ...]", file=sys.stderr)
        sys.exit(1)

    has_error = False
    any_file_modified = False

    for filepath in sys.argv[1:]:
        if not os.path.exists(filepath):
            print(f"Warning: File not found: '{filepath}'. Skipping.", file=sys.stderr)
            continue

        modified = canonicalize_file(filepath)
        if modified is True:
            any_file_modified = True
        elif modified is None:  # An error occurred during processing of this specific file
            has_error = True

    if has_error:
        sys.exit(1)

    if any_file_modified:
        sys.exit(1)

    sys.exit(0)  # All files were already canonical, or no eligible files. Success.


if __name__ == "__main__":
    main()
