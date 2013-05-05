from datetime import datetime

def smart_parse_date(datestring, in_format=None, out_format='%Y-%m-%d'):
    ''' Convert the datestring to desired format (ie. YYYY-MM-DD)
        @param string datestring
        @param string in_format. Format of input string in strptime terms, optional
        @param string out_format. Format to set return string in strptime terms
    '''
    if in_format is None:
        in_format = '%m/%d/%Y'
    d = datetime.strptime(datestring, in_format)
    return d.strftime(out_format)