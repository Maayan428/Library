class Members:

    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number

    def to_dict(self):
        return {
            "name": self.name,
            "phone_number": self.phone_number
        }