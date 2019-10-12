class CustomAPIException(Exception):
    """
    Extends the Exception class.
    """
    def __init__(self, message, status_code=None):
        """
        CustomAPIException constructor.
        :param message: message to return of the custom exception
        :type message: str
        :param status_code: status code of the custom exception
        :type: status: int
        """
        Exception.__init__(self)    # initializes the CustomAPIException instance as an instance of the Exception class
        self.set_message(message)   # sets message for the CustomAPIException instance
        self.set_status_code(status_code)   # sets status code  for the CustomAPIException instance

    def get_message(self):
        """
        Returns the message of the CustomAPIException instance.
        :return: message
        """
        return self.message

    def get_status_code(self):
        """
        Returns the status code of the CustomAPIException instance.
        :return: status_code
        """
        return self.status_code

    def set_message(self, message):
        """
        Sets CustomAPIException instance's message attribute.
        :param message: message of the CustomAPIException
        :type message: str
        """
        if (message is not None) and (type(message) is str):
                self.message = message

    def set_status_code(self, status_code):
        """
        Sets CustomAPIException instance's status_code attribute.
        :param status_code: status code of the CustomAPIException
        :type status_code: int
        """
        if (status_code is not None) and (type(status_code) is int):
                self.status_code = status_code
        else:
            self.status_code = 500

    def to_dict(self):
        """
        Parses the CustomAPIException instance to a dict and returns it.
        :return: exception_dict
        """
        exception_dict = dict(message=self.message)
        return exception_dict
