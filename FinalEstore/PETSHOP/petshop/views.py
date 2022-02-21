from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Order, Product
from datetime import datetime
from .forms import CheckoutForm
from . import db


bp = Blueprint('main', __name__)

#Route for each Template page

@bp.route('/database')
def database():
    title = "database"
    products = Product.query.order_by(Product.name)
    return render_template('database.html', title=title, products=products)

@bp.route('/Dog_Apparel', methods=['GET','POST'])
def DogApparel():
    title = "Dog Apparel"
    dogApparel = Product.query.filter(Product.category == "Dog Apparel")
    return render_template('Dog_Apparel.html', title=title, dogApparel = dogApparel)

@bp.route('/Dog_CollarLead')
def DogCollarLead():
    dogCollarLead = Product.query.filter(Product.category == "Dog Collar")
    return render_template('Dog_CollarLead.html', dogCollarLead = dogCollarLead)

@bp.route('/Dog_Food')
def DogFood():
    dogFood = Product.query.filter(Product.category == "Dog Food")
    return render_template('Dog_Food.html', dogFood = dogFood)

@bp.route('/Sale')
def sale():
    sale = Product.query.filter(Product.category == "Dog Food")
    return render_template('sale.html', sale = sale)

@bp.route('/Cat_Food')
def CatFood():
    catFood = Product.query.filter(Product.category == "Cat Food")
    return render_template('Cat_Food.html', catFood = catFood)

@bp.route('/Cat_Apparel')
def CatApparel():
    catApparel = Product.query.filter(Product.category == "Cat Apparel")
    return render_template('Cat_Apparel.html', catApparel = catApparel)

@bp.route('/Cat_Toys')
def CatToys():
    catToys = Product.query.filter(Product.category == "Cat Toys")
    return render_template('Cat_Toys.html', catToys = catToys)

@bp.route('/PetShop')
def PetShop():
    return render_template('PetShop.html')

@bp.route('/')
def Landing():
    return render_template('PetShop.html')


#Cart

@bp.route('/Cart', methods=['POST','GET'])
def order():
    product_id = request.values.get('product_id')

    # retrieve order if there is one
    if 'order_id'in session.keys():
        order = Order.query.get(session['order_id'])
        # order will be None if order_id stale
    else:
        # there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order(status = False, firstname='', surname='', email='', phone='', totalcost=0, date=datetime.now())
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('failed at creating a new order')
            order = None
    
    # calcultate totalprice
    totalprice = 0
    if order is not None:
        for product in order.products:
            totalprice = totalprice + product.price
    
    # are we adding an item?
    if product_id is not None and order is not None:
        product = Product.query.get(product_id)
        if product not in order.products:
            try:
                order.products.append(product)
                db.session.commit()
            except:
                return 'There was an issue adding the item to your basket'
            return redirect(url_for('main.order'))
        else:
            flash('item already in basket')
            return redirect(url_for('main.order'))
    
    return render_template('Cart.html', order = order, totalprice = totalprice)


# Delete specific basket items
@bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id = request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        product_to_delete = Product.query.get(id)
        try:
            order.products.remove(product_to_delete)
            db.session.commit()
            return redirect(url_for('main.Cart'))
        except:
            flash('Problem deleting item from order - try EMPTY BASKET or contact our store.')
            
    return redirect(url_for('main.order'))

# Scrap basket
@bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.PetShop'))

# Checkout Form
@bp.route('/checkout/', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
       
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            totalcost = 0
            for product in order.products:
                totalcost = totalcost + product.price
            order.totalcost = totalcost
            order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you! One of our awesome team members will contact you soon...')
                return redirect(url_for('main.PetShop'))
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form = form)


