class Contact:
    def __init__(self, full_name, address="", birthday="", email="", note=""):
        self._full_name = full_name
        self._address = address
        self._birthday = birthday
        self._email = email
        self._note = note

    # Getter & Setter
    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        self._full_name = value

    @property
    def address(self):
        return self._address

    @property
    def birthday(self):
        return self._birthday

    @property
    def email(self):
        return self._email

    @property
    def note(self):
        return self._note

    def update_info(self, address=None, email=None, note=None):
        if address:
            self._address = address
        if email:
            self._email = email
        if note:
            self._note = note
