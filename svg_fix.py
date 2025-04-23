from xml.etree import ElementTree as ET
import os


# Read all the files inside the folder images
def recursively_remove_invalid_paths(parent):
    for child in list(parent):
        if child.tag.endswith("path"):
            d = child.attrib.get("d")
            if d is None or not d.strip():
                parent.remove(child)
        else:
            recursively_remove_invalid_paths(child)


folder_path = "images"
files = os.listdir(folder_path)
print("Files in the folder:", files)

for file in files:
    file_path = os.path.join(folder_path, file)
    print("File path:", file_path)
    # Check if the file is a valid SVG file
    if file.endswith(".svg"):
        try:
            # Try to parse the SVG file
            tree = ET.parse(file_path)
            root = tree.getroot()
            print(f"Successfully parsed {file_path}")

            recursively_remove_invalid_paths(root)
            tree.write(file_path)
            print(f"Cleaned {file_path} and saved changes.")
        except ET.ParseError:
            print(f"Failed to parse {file_path}")
        except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}")

    # Now, let's remove invalid paths from the SVG file


tree = ET.parse("results_filter_synthetic_presentation_transparent.svg")
root = tree.getroot()


recursively_remove_invalid_paths(root)

tree.write("cleaned_file.svg")
