class PhoneBookFile(object):

    def __init__(self, contacts):
        self.__contacts = contacts

    @property
    def contacts(self):
        return self.__contacts

    @contacts.setter
    def contacts(self, contacts):
        self.__contacts = contacts


class ContactInformation(object):

    def __init__(self, contact_id):
        self.__contact_id = contact_id
        self.__first_name = ""
        self.__last_name = ""
        self.__phone_number = ""
        self.__timestamp = ""
        self.__image = "No image found"

    @property
    def contact_id(self):
        return self.__contact_id

    @contact_id.setter
    def contact_id(self, contact_id):
        self.__contact_id = contact_id

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name):
        self.__first_name = first_name

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name):
        self.__last_name = last_name

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        self.__phone_number = phone_number

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        self.__timestamp = timestamp

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        self.__image = image
