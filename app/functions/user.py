import re

from app.functions.error import AccessError, InputError
from app.models import Accountdata

def get_data(userID):
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

def update_data(userID, userData):

    email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    if not re.fullmatch(email_regex, userData["electronicMail"]):
        raise InputError(description="Email is invalid")
    #get user
    accountinfo = Accountdata.query.filter(Accountdata.userId == userID).first()
    accountinfo.businessName = userData["businessName"]
    accountinfo.contactName = userData["contactName"]
    accountinfo.electronicMail = userData["elecronicMail"]
    accountinfo.supplierID = userData["supplierID"]
    accountinfo.street = userData["street"]
    accountinfo.city = userData["city"]
    accountinfo.postcode = userData["postcode"]
    accountinfo.country = userData["country"]
    accountinfo.currency = userData["currency"]

