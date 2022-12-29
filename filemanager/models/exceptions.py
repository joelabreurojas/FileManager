""""Structures oriented to the transmission of custom errors"""


class FileAlreadyExists(Exception):
    pass


class FileAlreadyUsed(Exception):
    pass


class FileNotFound(Exception):
    pass


class FileNotValid(Exception):
    pass
