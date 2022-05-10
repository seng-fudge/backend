

from app.models import Customer, Payment, Product, User, db


def add_customer(customer, user_id):

    customer_store = Customer(buyerReference=customer['buyerReference'],
                              customerName=customer['customerName'],
                              businessName=customer['businessName'],
                              email=customer['email'],
                              streetAddress=customer['streetAddress'],
                              additionalStreetAddress=customer['additionalStreetAddress'],
                              city=customer['city'], postcode=customer['postcode'],
                              country=customer['country'], userId=user_id)

    savedAlready = Customer.query.filter(Customer.userId == user_id, Customer.buyerReference == customer['buyerReference']).all();
    
    for curr in savedAlready:
        db.session.delete(curr);

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


def add_payment(payment, user_id):

    payment_store = Payment(dueDate=payment['dueDate'],
                            paymentType=payment['paymentType'],
                            paymentId=payment['paymentId'],
                            paymentTerms=payment['paymentTerms'],
                            userId=user_id)

    db.session.add(payment_store)
    db.session.commit()

    return {}


def get_payment(user_id):

    user = User.query.get(user_id)

    payments = []

    for payment in user.payments:
        payments.append({
            'dueDate': payment.dueDate,
            'paymentType': payment.paymentType,
            'paymentId': payment.paymentId,
            'paymentTerms': payment.paymentTerms
        })

    return {'payments': payments}


def add_product(product, user_id):

    product_store = Product(invoiceId=product['invoiceId'],
                            invoiceQuantity=product['invoiceQuantity'],
                            invoiceLineExtension=product['invoiceLineExtension'],
                            invoiceName=product['invoiceName'],
                            invoicePriceAmount=product['invoicePriceAmount'],
                            invoiceBaseQuantity=product['invoiceBaseQuantity'],
                            userId=user_id)

    db.session.add(product_store)
    db.session.commit()

    return {}


def get_product(user_id):

    user = User.query.get(user_id)

    products = []

    for product in user.products:
        products.append({
            'invoiceId': product.invoiceId,
            'invoiceQuantity': product.invoiceQuantity,
            'invoiceLineExtension': product.invoiceLineExtension,
            'invoiceName': product.invoiceName,
            'invoicePriceAmount': product.invoicePriceAmount,
            'invoiceBaseQuantity': product.invoiceBaseQuantity,
        })

    return {'products': products}
