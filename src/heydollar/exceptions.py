
class HeydollarInvalidUploadFile(Exception):
    ''' Throw when trying to upload a file that does not exist 
        or has unexpected format (ie, headers)
    '''
    pass