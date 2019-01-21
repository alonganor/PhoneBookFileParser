import csv
import os
import time
from imghdr import tests as file_type_testers


def read(path):
    with open(path, 'r') as ref:
        return ref.read().split("\n")


def write(path, txt):
    with open(path, 'wb') as ref:
        ref.write(txt)


class PhoneBookFileParser(object):
    DATA_CHUNK_TYPE_HEX_DIGIT_COUNT = 4
    ID_HEX_DIGIT_COUNT = 4
    BUFFER_HEX_DIGIT_COUNT = 1
    STRING_LENGTH_HEX_DIGIT_COUNT = 4
    FIELD_NAMES = {0x86B7: "first_name",
                   0x9E60: "last_name",
                   0x5159: "phone_number", # this identifier also appears as a contact id. I'm assuming that since the phone number chunk has to have a type, the same identifier is being used in both cases.
                   0xD812: "timestamp",
                   0x6704: "image"}

    @classmethod
    def parse(cls, phone_book_file_path, output_folder_path):
        phone_book_byte_streams = read(phone_book_file_path)
        contact_id_to_record_dict = {}
        # The data of this format is divided into chunks that each has a unique meaning(I.E phone number, last name...)
        for byte_stream in phone_book_byte_streams:
            ptr = 0
            byte_stream_data_type = int(byte_stream[ptr: ptr + cls.DATA_CHUNK_TYPE_HEX_DIGIT_COUNT], 16)
            field_name = cls.FIELD_NAMES[byte_stream_data_type]
            ptr += cls.DATA_CHUNK_TYPE_HEX_DIGIT_COUNT
            while ptr < len(byte_stream):
                contact_id = int(byte_stream[ptr: ptr + cls.ID_HEX_DIGIT_COUNT], 16)
                ptr += cls.ID_HEX_DIGIT_COUNT
                ptr += cls.BUFFER_HEX_DIGIT_COUNT

                field_value_length = int(byte_stream[ptr: ptr + cls.STRING_LENGTH_HEX_DIGIT_COUNT], 16)
                ptr += cls.STRING_LENGTH_HEX_DIGIT_COUNT

                field_value = byte_stream[ptr: ptr + field_value_length]
                ptr += field_value_length

                if contact_id not in contact_id_to_record_dict:
                    contact_id_to_record_dict[contact_id] = {}

                if field_name == "image":
                    field_value = cls.export_image(field_value,
                                                   output_folder_path,
                                                   str(contact_id))

                current = None
                if field_name in contact_id_to_record_dict[contact_id]:
                    current = contact_id_to_record_dict[contact_id][field_name]

                contact_id_to_record_dict[contact_id][field_name] = cls.correct_value_for_insert(field_name, field_value, current)

        return contact_id_to_record_dict.values()

    @classmethod
    def correct_value_for_insert(cls, field_name, field_value, curr_value=None):
        field_name_to_return_value = {
            "first_name": lambda value, current: value.replace('\xa0', ' '), # Replace 'Non-breaking space' with regular space
            "last_name": lambda value, current: value,
            "phone_number": lambda value, current: [value] if curr_value is None else current + [value], # In case of multiple phone numbers
            "timestamp": lambda value, current: time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(int(value))),
            "image": lambda value, current: value
        }
        return field_name_to_return_value[field_name](field_value, curr_value)

    @classmethod
    def export_to_csv(cls, phone_book_dict, export_path):
        file_obj = open(export_path, 'a')
        csv_writer = csv.DictWriter(file_obj, cls.FIELD_NAMES.values())
        csv_writer.writeheader()
        for contact in phone_book_dict:
            # In case a person has more then one phone number
            if "phone_number" in contact:
                contact["phone_number"] = " || ".join(contact["phone_number"])

            csv_writer.writerow(contact)

    @classmethod
    def export_image(cls, encoded_byte_stream, output_folder_path, contact_id):
        byte_stream = encoded_byte_stream.decode("base64")
        phone_book_images_folder = os.path.join(output_folder_path, "profile_images")
        if not os.path.exists(phone_book_images_folder):
            os.mkdir(phone_book_images_folder)
        file_name = contact_id + "." + cls.get_file_type(byte_stream)
        out_file_path = os.path.join(phone_book_images_folder, file_name)
        write(out_file_path, byte_stream)
        return out_file_path

    @classmethod
    def get_file_type(cls, byte_stream):
        header = byte_stream[:32]
        for t in file_type_testers:
            res = t(header, None)
            if res:
                return res


def main(file_path):
    output_folder = file_path[:file_path.rfind('.')] + "_output"
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    phone_book_dict = PhoneBookFileParser.parse(file_path, output_folder)
    out_name = os.path.basename(file_path)
    out_name = out_name[:out_name.rfind('.')] + "_output.csv"
    out_path = os.path.join(output_folder, out_name)
    if not os.path.exists(out_path):
        PhoneBookFileParser.export_to_csv(phone_book_dict, out_path)


if __name__ == '__main__':
    db_file_path = r"C:\Users\aganor\Downloads\ex_v7.txt"
    main(db_file_path)
