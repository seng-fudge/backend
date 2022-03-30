import re
from app.functions.error import AccessError, InputError
from app.models import Accountdata, db

def get_data(userID: int):
    """
    Gets user data from the database.
    Returns user data as a dict

    Raises issue if variables given are invalid:
        - userID

    Parameters
    ----------
    'userID' - integer

    Returns
    -------
    userData = {
        "businessName" : "company"
        "contactName" : "first last"
        "electronicMail" : "firstlast@company.com"
        "supplierID" : "123"
        "street" : "street ave"
        "city" : "city"
        "postcode" : 1256
        "country" : "Australia"
        "currency" : "AUD"
    }
    """
    accountinfo = Accountdata.query.filter(Accountdata.userId == userID).first()
    userData = {
        "businessName" : accountinfo.businessName,
        "contactName" : accountinfo.contactName,
        "electronicMail" : accountinfo.electronicMail,
        "supplierID" : accountinfo.supplierID,
        "street" : accountinfo.street,
        "city" : accountinfo.city,
        "postcode" : accountinfo.postcode,
        "country" : accountinfo.country,
        "currency" : accountinfo.currency
    }


    return userData

def update_data(userID: int, userData: object):
    """
    Updates user data in database.
    Returns user data as a dict
    Raises issue if variables given are invalid:
        - userID

    Parameters
    ----------
    'userID' - integer
    'userData' - object
        mandatory feilds:
            "businessName"
            "contactName"
            "electronicMail"
            "supplierID"
            "street"
            "city"
            "postcode"
            "country"
            "currency"

    Returns
    -------
    userData = {
        "businessName" : "company"
        "contactName" : "first last"
        "electronicMail" : "firstlast@company.com"
        "supplierID" : "123"
        "street" : "street ave"
        "city" : "city"
        "postcode" : 1256
        "country" : "Australia"
        "currency" : "AUD"
    }

    Raises
    -------
        Input error - when given bad data
    """
    good_data(userData)
    #get user
    accountinfo = Accountdata.query.filter(Accountdata.userId == userID).first()
    accountinfo.businessName = userData["businessName"]
    accountinfo.contactName = userData["contactName"]
    accountinfo.electronicMail = userData["electronicMail"]
    accountinfo.supplierID = userData["supplierID"]
    accountinfo.street = userData["street"]
    accountinfo.city = userData["city"]
    accountinfo.postcode = userData["postcode"]
    accountinfo.country = userData["country"]
    accountinfo.currency = userData["currency"]
    db.session.commit()

def good_data(userData: object):

    email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    if not re.fullmatch(email_regex, userData["electronicMail"]):
        raise InputError(description="Email is invalid")

    if type(userData["businessName"]) != str:
        raise InputError

    if type(userData["contactName"]) != str:
        raise InputError

    if type(userData["electronicMail"]) != str:
        raise InputError

    if type(userData["supplierID"]) != int:
        raise InputError

    if type(userData["street"]) != str:
        raise InputError

    if type(userData["city"]) != str:
        raise InputError

    if type(userData["postcode"]) != str:
        raise InputError

    if type(userData["country"]) != str:
        raise InputError

    if type(userData["currency"]) != str:
        raise InputError
