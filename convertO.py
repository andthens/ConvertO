#Code by Anandan Salikumar
# This code will update the Name of IC and ICF with the XML Tag. It supports the .sif extension files only.

import xml.etree.ElementTree as ET

def update_names(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for component in root.findall(".//INTEGRATION_COMPONENT"):
        xml_tag = component.get("XML_TAG")
        if xml_tag:
            component.set("NAME", xml_tag) 

        for field in component.findall(".//INTEGRATION_COMPONENT_FIELD"):
            field_xml_tag = field.get("XML_TAG")
            if field_xml_tag:
                field.set("NAME", field_xml_tag) 

    output_file = "updated_" + file_path
    tree.write(output_file, encoding="UTF-8", xml_declaration=True)
    print(f"Updated XML file saved as: {output_file}")

input_file = input("Enter the file Name with extension")
update_names(input_file)