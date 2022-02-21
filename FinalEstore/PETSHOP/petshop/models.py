from . import db


class Product(db.Model):
    __tablename__='product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    category = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False, default = 'defaultcity.jpg')
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        str = "Id: {}, Name: {}, Category {}, Description: {}, Image: {}, Price {}\n" 
        str =str.format( self.id, self.name,self.category,self.description,self.image,self.price)
        return str

orderdetails = db.Table('orderdetails', 
    db.Column('order_id', db.Integer,db.ForeignKey('orders.id'), nullable=False),
    db.Column('product_id',db.Integer,db.ForeignKey('product.id'),nullable=False),
    db.PrimaryKeyConstraint('order_id', 'product_id') )

class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    totalcost = db.Column(db.Float)
    date = db.Column(db.DateTime)
    products = db.relationship("Product", secondary=orderdetails, backref="orders") 
    
    def get_product_details(self):
        return str(self)

    def __repr__(self):
        str = "id: {}, Status: {}, Firstname: {}, Surname: {}, Email: {}, Phone: {}, Date: {}, Total Cost: {}\n" 
        str =str.format( self.id, self.status,self.firstname,self.surname, self.email, self.phone, self.date, self.totalcost)
        return str
    
    
