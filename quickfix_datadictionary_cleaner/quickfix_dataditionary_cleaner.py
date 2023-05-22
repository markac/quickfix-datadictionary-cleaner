import argparse
from lxml import etree


def remove_unreferenced_fields(input_file, output_file):
    # Parse the XML file
    tree = etree.parse(input_file)

    # Get the root element
    root = tree.getroot()

    # Find all fields and components
    fields = root.xpath('//fields/field')
    components = root.xpath('//components/component')

    # Get the set of referenced field and component names
    referenced_field_ids = set()
    referenced_component_ids = set()

    # Find all messages
    messages = root.xpath('//messages/message')
    for message in messages:
        find_fields_and_components(message, referenced_component_ids, referenced_field_ids)

    # Find the header block
    header = root.find('header')
    if header is not None:
        find_fields_and_components(header, referenced_component_ids, referenced_field_ids)

    # Find the trailer block
    trailer = root.find('trailer')
    if trailer is not None:
        find_fields_and_components(trailer, referenced_component_ids, referenced_field_ids)

    # Retain fields referenced from components
    for component in components:
        component_name = component.get('name')
        if component_name in referenced_component_ids:
           find_fields_and_components(component, referenced_component_ids, referenced_field_ids)

    # Remove unreferenced fields
    for field in fields:
        field_name = field.get('name')
        if field_name not in referenced_field_ids:
            field.getparent().remove(field)

    # Remove unreferenced components
    for component in components:
        component_name = component.get('name')
        if component_name not in referenced_component_ids:
            component.getparent().remove(component)

    # Save the modified XML file
    tree.write(output_file, pretty_print=True)


def find_fields_and_components(node, referenced_component_ids, referenced_field_ids):
    find_fields(node, referenced_field_ids)

    find_components(node, referenced_component_ids)


def find_components(node, referenced_component_ids):
    # Find all components in the message
    components = node.xpath('.//component')
    for component in components:
        referenced_component_ids.add(component.get('name'))


def find_fields(node, referenced_field_ids):
    # Find all fields in the message
    fields = node.xpath('.//field')
    for field in fields:
        referenced_field_ids.add(field.get('name'))
    # Find all groups in the message - group name is a field in effect
    fields = node.xpath('.//group')
    for field in fields:
        referenced_field_ids.add(field.get('name'))


if __name__ == '__main__':
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Remove unreferenced fields and components from a QuickFIX data dictionary XML file')
    parser.add_argument('input_file', help='Path to the input data dictionary XML file')
    parser.add_argument('output_file', help='Path to save the stripped data dictionary XML file')

    # Parse the arguments
    args = parser.parse_args()

    # Run the program
    remove_unreferenced_fields(args.input_file, args.output_file)