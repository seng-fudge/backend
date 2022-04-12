

from app.models import Customer, User, db


def add_customer(customer, user_id):

    customer_store = Customer(buyerReference=customer['buyerReference'], customerName=customer['customerName'], businessName=customer['businessName'], email=customer['email'],
                              streetAddress=customer['streetAddress'], additionalStreetAddress=customer['additionalStreetAddress'], city=customer['city'], postcode=customer['postcode'], country=customer['country'], userId=user_id)

    db.session.add(customer_store)
    db.session.commit()

    return {}


def get_customer(user_id):

    user = User.query.get(user_id)

    customers = []

    for customer in user.customers:
        customers.append({
            'buyerReference': customer.buyerReference,
            'customerName': customer.customerName,
            'businessName': customer.businessName,
            'email': customer.email,
            'streetAddress': customer.streetAddress,
            'additionalStreetAddress': customer.additionalStreetAddress,
            'city': customer.city,
            'postcode': customer.postcode,
            'country': customer.country,
        })

    return {'customers': customers}
