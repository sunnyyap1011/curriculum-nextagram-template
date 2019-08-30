from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.donation import Donation
from models.image import Image
from money.money import Money
from money.currency import Currency
from app import gateway

donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates')


@donations_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def new():
    client_token = gateway.client_token.generate()
    image = request.form['image']
    return render_template('donations/new.html', client_token=client_token, image=image)


@donations_blueprint.route('/checkout', methods=['POST'])
@login_required
def create_purchase():
    nonce_from_the_client = request.form["payment_method_nonce"]
    amount = request.form["amount"]
    donor = current_user.id
    image = request.form['image']

    i = Image.get(id=image)
    
    m = Money(amount, Currency.USD)

    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
        "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:
        d = Donation(amount=amount, txs_id=result.transaction.id , image=image, donor=donor)
        if d.save():
            flash(f"Your donation of {m} has been successfully sent to {i.user.username}! \nTransaction_ID: {result.transaction.id}", 'success')
            return redirect(url_for('users.show', username=current_user.username))
        else:
            flash("Something went wrong, it's not saved to the database", 'danger')
            return render_template('donations/new.html')
    else: 
        for x in result.errors.deep_errors:
            flash(f"Erorr: {x.code}: {x.message} ")
            return render_template('users/show.html', user=i.user)
