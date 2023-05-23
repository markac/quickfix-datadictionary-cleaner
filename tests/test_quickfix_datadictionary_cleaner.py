import unittest
import os
from xmldiff import main, formatting
import xml.etree.ElementTree as ET
from parameterized import parameterized
from quickfix_datadictionary_cleaner.quickfix_datadictionary_cleaner import remove_unreferenced_fields


class TestRemoveUnreferencedFields(unittest.TestCase):
    def tearDown(self):
        # Remove the output files
        os.remove(self.output_file)

    @parameterized.expand([
        ("should_maintain_fields_referenced_in_header"),
        ("should_maintain_groups_referenced_in_header"),
        ("should_maintain_fields_referenced_in_trailer"),
        ("should_maintain_fields_referenced_in_messages"),
        ("should_maintain_groups_referenced_in_messages"),
    ])
    def test_remove_unreferenced_fields(self, file_root_name):
        # Create a sample input XML file
        self.input_file = 'tests/' + file_root_name + '_input.xml'
        self.output_file = 'tests/' + file_root_name + '_output.xml'
        self.expected_output_file = 'tests/' + file_root_name + '_output_expected.xml'

        # Call the function to remove unreferenced fields
        remove_unreferenced_fields(self.input_file, self.output_file)

        formatter = formatting.XmlDiffFormatter(normalize=formatting.WS_BOTH, pretty_print=True)
        differences = main.diff_files(
            self.output_file,
            self.expected_output_file,
            diff_options={'F': 0.5, 'ratio_mode': 'accurate', 'uniqueattrs': 'name'},
            formatter=formatter)

        if differences:
            print(f"Differences between XML files '{self.output_file}' and '{self.expected_output_file}':")

            print(differences)

            with open(self.output_file, 'r') as f1, open(self.expected_output_file, 'r') as f2:
                output_content = f1.read()
                expected_content = f2.read()

                # Print the contents of both files
            print(f"Contents of '{self.output_file}':")
            print(output_content)
            print()

            print(f"Contents of '{self.expected_output_file}':")
            print(expected_content)
            print()

        assert not differences, f"XML files '{self.output_file}' and '{self.expected_output_file}' are not equal"


if __name__ == '__main__':
    unittest.main()
