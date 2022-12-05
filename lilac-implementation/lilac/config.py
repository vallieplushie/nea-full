"""Exports the LICONF config object"""

class LICONF:
    """Global configuration container"""
    HAD_ERROR = False
    INTERACTIVE_MODE = True

    LOG_TYPE = 'FILE' # | 'CONFIG'
    LOG_LEVEL = 'DEBUG'
    LOG_TABLE = {'TRACE':0,'DEBUG':1,'INFO':2,'WARN':3,'ERROR':4,'FATAL':5}
    LOG_PATH = '/Users/valerie/Documents/Sixth-Form/Computer-Science/nea-full-repo/lilac-implementation/log/log.txt'


