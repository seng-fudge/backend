from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    """403 - HTTP access error"""
    code = 403
    message = 'Tried to access something you do not have permissions for'

class InputError(HTTPException):
    """400 - HTTP input error"""
    code = 400
    message = 'Input incorrect'
