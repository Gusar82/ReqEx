import re
import os
import csv
from pprint import pprint


def path_file_csv(file):
    base_path = os.getcwd()
    dir_csv_files = 'csv_files'
    dir_path = os.path.join(base_path, dir_csv_files)
    return os.path.join(dir_path, file)


def read_contact_list(file):
    """ Чтение адресной книги в формате CSV в список contact_list"""
    file_path = path_file_csv(file)
    with open(file_path, encoding='cp1251') as f:
      rows = csv.reader(f, delimiter=",")
      contacts_list = list(rows)
    # print(contacts_list)
    return contacts_list


def write_contact_list(file, header, contact_list):
    """Запись в файл в формате csv из contact_list"""
    file_path = path_file_csv(file)
    with open(file_path, "w", encoding='cp1251', newline="") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerow(header)
        datawriter.writerows(contact_list)


def separate_name(fullname: list):
    pattern = r'(\w+) +(\w+) +(\w*)'
    fullname_list = re.search(pattern, ' '.join(fullname)).group(1, 2, 3)
    print(f'{fullname} заменены на {fullname_list}')
    return fullname_list


# def separate_phone(phone:str):
#     phone_ext = ''
#     pattern_ext = r'(.*)доб\W*(\d*)'
#     phone_re = re.search(pattern_ext, phone)
#     if phone_re:
#         phone_ext = 'доб.' + phone_re.group(2)
#         phone = phone_re.group(1)
#     phone_list = re.findall('\d', phone)
#     code = ''.join(phone_list[1:-7])
#     phone = ''.join(phone_list[-7:-1])
#     if phone != "":
#         return f"+7({code}){phone} {phone_ext}"


def separate_phone_re(phone: str):
    pattern = r'(\+7|8)\W*(\d{3})\W*(\d{3})\W*(\d{2})\W*(\d{2})\W*(доб.|)\W*(\d*)\W*'
    phone_re = re.sub(pattern, r'+7(\2)\3-\4-\5 \6\7', phone).strip()
    if phone:
        pprint(f"{phone} заменен на {phone_re}")
    return phone_re


# def add_dict_phonebook(dict,data):
#     # (lastname, firstname, surname, organization, position, phone, email)
#     lastname, firstname, surname = separate_name(data[0:3])
#     key = lastname, firstname
#     organization = data[3]
#     position = data[4]
#     phone = separate_phone_re(data[5])
#     email = data[6]
#     if key in dict:
#         if surname:
#             dict[key][0] = surname
#         if organization:
#             dict[key][1] = organization
#         if position:
#             dict[key][2] = position
#         if phone:
#             dict[key][3] = phone
#         if email:
#             dict[key][4] = email
#     else:
#         dict_phone[key] = [surname, organization, position, phone, email]


def add_dict_phonebook(dict, data):
    # (lastname, firstname, surname, organization, position, phone, email)
    data[0], data[1], data[2] = separate_name(data[0:3])
    key = data[0], data[1]
    data[5] = separate_phone_re(data[5])
    if key in dict:
        for pos in range(2, len(data)):
            if data[pos]:
                dict[key][pos] = data[pos]
                pprint(f'добавлены данные - {data[pos]}')
    else:
        dict_phone[key] = data
        print(f' {data}')
    pprint("----------------------------")


if __name__ == '__main__':
    csv_raw_file = 'phonebook_raw.csv'
    csv_file_new = "phonebook.csv"
    dict_phone ={}
    contact_list = read_contact_list(csv_raw_file)
    header = contact_list.pop(0)
    for data_phone in contact_list:
        add_dict_phonebook(dict_phone, data_phone)
    write_contact_list(csv_file_new, header, list(dict_phone.values()))
    #write_contact_list(csv_file_new,['1','2','3'])
    # for data in read_contact_list(csv_raw_file):
    #     pprint(separate_name(data[0:3]))


