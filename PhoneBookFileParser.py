from PhoneBookFile import *
import time


def read(path):
    with open(path, 'r') as ref:
        return ref.read()


class PhoneBookFileParser(object):
    PART_TYPE_BYTE_COUNT = 2
    ID_BYTE_COUNT = 2
    SEPARATOR_LENGTH = 1
    STRING_LENGTH_BYTE_COUNT = 2
    FIELD_NAMES = {0x86B7: "first_name",
                   0x9E60: "last_name",
                   0x5159: "phone_number",
                   0xD812: "timestamp",
                   0x6704: "image"}

    @classmethod
    def parse(cls, x_file_path):
        x_file_bytes_stream = read(x_file_path)
        x_file_bytes_streams = x_file_bytes_stream.split("\n")
        contacts_information = cls.parse_byte_streams(x_file_bytes_streams)
        return PhoneBookFile(contacts_information)

    @classmethod
    def parse_byte_streams(cls, byte_streams):
        contact_id_to_record_dict = {}
        for byte_stream in byte_streams:
            ptr = 0
            byte_stream_data_type = int(byte_stream[ptr: ptr + cls.PART_TYPE_BYTE_COUNT * 2], 16)
            field_name = cls.FIELD_NAMES[byte_stream_data_type]
            ptr += cls.PART_TYPE_BYTE_COUNT * 2
            while ptr < len(byte_stream):
                contact_id = int(byte_stream[ptr: ptr + cls.ID_BYTE_COUNT * 2], 16)
                ptr += cls.ID_BYTE_COUNT * 2

                ptr += cls.SEPARATOR_LENGTH

                field_value_length = int(byte_stream[ptr: ptr + cls.STRING_LENGTH_BYTE_COUNT * 2], 16)
                ptr += cls.STRING_LENGTH_BYTE_COUNT * 2

                field_value = byte_stream[ptr: ptr + field_value_length]
                ptr += field_value_length

                if contact_id not in contact_id_to_record_dict:
                    contact_id_to_record_dict[contact_id] = ContactInformation(contact_id)

                contact_id_to_record_dict[contact_id] = cls.set_property(field_name,
                                                                         field_value,
                                                                         contact_id_to_record_dict[contact_id])

        return contact_id_to_record_dict.values()

    @staticmethod
    def set_property(field_name, field_value, contact):
        if field_name == "first_name":
            contact.first_name = field_value
        elif field_name == "last_name":
            contact.last_name = field_value
        elif field_name == "phone_number":
            contact.phone_number = field_value
        elif field_name == "timestamp":
            contact.timestamp = time.gmtime(int(field_value))
        elif field_name == "image":
            contact.image = field_value.decode("base64")
        return contact


def main(file_path):
    phone_book = PhoneBookFileParser.parse(file_path)


if __name__ == '__main__':
    db_file_path = r"C:\Users\aganor\Downloads\ex_v7.txt"
    main(db_file_path)
