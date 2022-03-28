from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    code = 403
    message = 'Tried to access something you do not have permissions for'

class InputError(HTTPException):
    code = 400
    message = 'Input incorrect'
