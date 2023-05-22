import argparse
from lxml import etree


def remove_unreferenced_fields(input_file, output_file):
    # Parse the XML file
    tree = etree.parse(input_file)

    # Get the root element
    root = tree.getroot()

    # Find all fields and components
    fields = root.xpath('//field')
    components = root.xpath('//component')

    # Get the set of referenced field and component IDs
    referenced_ids = set()

    # Find all messages
    messages = root.xpath('//message')
    for message in messages:
        # Find all fields in the message
        message_fields = message.xpath('.//field')
        for field in message_fields:
            referenced_ids.add(field.get('number'))

        # Find all components in the message
        message_components = message.xpath('.//component')
        for component in message_components:
            referenced_ids.add(component.get('name'))

            # Find all fields in the component
            component_fields = component.xpath('.//field')
            for field in component_fields:
                referenced_ids.add(field.get('number'))

    # Remove unreferenced fields
    for field in fields:
        field_id = field.get('number')
        if field_id not in referenced_ids:
            field.getparent().remove(field)

    # Remove unreferenced components
    for component in components:
        component_name = component.get('name')
        if component_name not in referenced_ids:
            component.getparent().remove(component)

    # Save the modified XML file
    tree.write(output_file, pretty_print=True)


if __name__ == '__main__':
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Remove unreferenced fields and components from a QuickFIX data dictionary XML file')
    parser.add_argument('input_file', help='Path to the input data dictionary XML file')
    parser.add_argument('output_file', help='Path to save the stripped data dictionary XML file')

    # Parse the arguments
    args = parser.parse_args()

    # Run the program
    remove_unreferenced_fields(args.input_file, args.output_file)

