class HeydollarBaseException(Exception):

    def __init__(self, *args, **kwargs):
        if 'error_field' in kwargs:
            self.error_field = kwargs.pop('error_field')
        if 'error_value' in kwargs:
            self.error_value = kwargs.pop('error_value')
        return super(HeydollarBaseException, self).__init__(*args, **kwargs)


class HeydollarInvalidUploadFile(HeydollarBaseException):
    ''' Thrown when trying to upload a file that does not exist
        or has unexpected format (ie, headers)
    '''
    pass

class HeydollarDoesNotExist(HeydollarBaseException):
    ''' Thrown when trying to upload a file specifying an object
        (ie, Account) that does not exist
    '''
    pass

class HeydollarAmbiguousEntry(HeydollarBaseException):
    ''' Thrown when a field has changed on a Txn entry that cannot be
        determined from a set of duplicate entries (ie, changed Memo field)
    '''
    pass
