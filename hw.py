import csv
import re


def read_file():
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def parse_file(contacts_list):
    update_list = []
    for contact in contacts_list:
        contacts = []
        full_name = ",".join(contact[:3])
        rslt = re.findall(r'(\w+)', full_name)
        while len(rslt) < 3:
            rslt.append('')
        contacts = contacts + rslt
        contacts.append(contact[3])
        contacts.append(contact[4])
        pattern = re.compile(r'(8|\+7)?\s*(\(*)(\d{3})(\)*)(\s*|-)(\d{3})'
                             r'(\s*|-)(\d{2})(\s*|-)(\d{2})\s*(\(*)'
                             r'(\w\w\w\.)*\s*(\d{4})*(\))*')
        change = pattern.sub(r'+7(\3)\6-\8-\10 \12\13', contact[5])
        contacts.append(change)
        contacts.append(contact[6])
        update_list.append(contacts)
    return update_list


def remove_dublicate(update_list):
    notebook = {}
    for contact in update_list:
        if contact[0] in notebook:
            contact_value = notebook[contact[0]]
            for i in range(len(contact_value)):
                if contact[i]:
                  contact_value[i] = contact[i]
        else:
            notebook[contact[0]] = contact
    return list(notebook.values())


def write_file(update_list):
    with open("phonebook.csv", "w", newline='', encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(update_list)

read_file()
parse_file(read_file())
remove_dublicate(parse_file(read_file()))
write_file(remove_dublicate(parse_file(read_file())))
