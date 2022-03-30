import re
from app.functions.error import AccessError, InputError
from app.models import Accountdata, db

def get_data(user_id: int):
    """
    Gets user data from the database.
    Returns user data as a dict

    Raises issue if variables given are invalid:
        - user_id

    Parameters
    ----------
    'user_id' - integer

    Returns
    -------
    user_data = {
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
    accountinfo = Accountdata.query.filter(Accountdata.userId == user_id).first()
    user_data = {
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


    return user_data

def update_data(user_id: int, user_data: object):
    """
    Updates user data in database.
    Returns user data as a dict
    Raises issue if variables given are invalid:
        - user_id

    Parameters
    ----------
    'user_id' - integer
    'user_data' - object
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
    user_data = {
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
    good_data(user_data)
    #get user
    accountinfo = Accountdata.query.filter(Accountdata.userId == user_id).first()
    accountinfo.businessName = user_data["businessName"]
    accountinfo.contactName = user_data["contactName"]
    accountinfo.electronicMail = user_data["electronicMail"]
    accountinfo.supplierID = user_data["supplierID"]
    accountinfo.street = user_data["street"]
    accountinfo.city = user_data["city"]
    accountinfo.postcode = user_data["postcode"]
    accountinfo.country = user_data["country"]
    accountinfo.currency = user_data["currency"]
    db.session.commit()

def good_data(user_data: object):

    if not isinstance(user_data["businessName"], str):
        raise InputError("businessName should be of type string")

    if not isinstance(user_data["contactName"], str):
        raise InputError("contactName should be of type string")

    if not isinstance(user_data["electronicMail"], str):
        raise InputError("electronicMail should be of type string")

    if not isinstance(user_data["supplierID"], int):
        raise InputError("supplierID should be of type integer")

    if not isinstance(user_data["street"], str):
        raise InputError("street should be of type string")

    if not isinstance(user_data["city"], str):
        raise InputError("city should be of type string")

    if not isinstance(user_data["postcode"], str):
        raise InputError("postcode should be of type string")

    if not isinstance(user_data["country"], str):
        raise InputError("country should be of type string")

    if not isinstance(user_data["currency"], str):
        raise InputError("currency should be of type string")

    email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    if not re.fullmatch(email_regex, user_data["electronicMail"]):
        raise InputError(description="Email is invalid")
