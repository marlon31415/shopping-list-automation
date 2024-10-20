def export_to_markdown(shopping_list, filename="shopping_list.md"):
    filename = "export/" + filename
    with open(filename, "w") as file:
        file.write("# Shopping List\n\n")
        for key, value in shopping_list.items():
            file.write(f"## {key}\n")
            if isinstance(value, list):
                for item in value:
                    file.write(f"- [ ] {item}\n")
            elif isinstance(value, dict):
                for item, quantity in value.items():
                    file.write(f"- [ ] {item} (x{quantity})\n")
    print(f"Successfully exported shopping list to {filename}")


def export_to_enex(shopping_list, filename="shopping_list.enex"):
    """
    Export a shopping list to an ENEX file (Evernote format) for importing as a checkable list.

    Parameters:
    shopping_list (dict): Dictionary where keys are section names and values are dictionaries of items and quantities.
    filename (str): The name of the output ENEX file.
    """
    # ENEX file header
    enex_content = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export2.dtd">',
        '<en-export export-date="20241017T000000Z" application="Evernote" version="10.0">',
    ]

    # Create the content of the note with a checklist for each shopping item
    note_content = [
        "<note>",
        "<title>Shopping List</title>",
        '<content><![CDATA[<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
        '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">',
        "<en-note>",
    ]

    # Add each section and its items as checkable list items in the note
    for section, items in shopping_list.items():
        note_content.append(f"<h2>{section.capitalize()}</h2>")
        if isinstance(items, list):
            for item in items:
                note_content.append(f"<div><en-todo/> {item}</div>")
        elif isinstance(items, dict):
            for item, quantity in items.items():
                item_text = f"{item} (x{quantity})"
                note_content.append(f"<div><en-todo/> {item_text}</div>")
        note_content.append("<br/>")

    # Close the note content
    note_content.extend(["</en-note>", "]]></content>", "</note>"])

    # Combine the note content and append to the ENEX content
    enex_content.extend(note_content)

    # Close the ENEX file
    enex_content.append("</en-export>")

    # Write to the specified file
    filename = "export/" + filename
    with open(filename, "w") as file:
        file.write("\n".join(enex_content))

    print(f"Successfully exported shopping list to {filename}")
