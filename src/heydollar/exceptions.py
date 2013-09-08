
class HeydollarInvalidUploadFile(Exception):
    ''' Thrown when trying to upload a file that does not exist 
        or has unexpected format (ie, headers)
    '''
    pass

class HeydollarDoesNotExist(Exception):
    ''' Thrown when trying to upload a file specifying an object
        (ie, Account) that does not exist
    '''
    pass

class HeydollarAmbiguousEntry(Exception):
    ''' Thrown when a field has changed on a Txn entry that cannot be
        determined from a set of duplicate entries (ie, changed Memo field)
    '''
    pass