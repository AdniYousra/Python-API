from flask import Flask ,jsonify,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
db=SQLAlchemy(app)



class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),unique=True,nullable=False)
    codebar=db.Column(db.String(80))
    type=db.Column(db.String(80))
    price=db.Column(db.String(80))
    description=db.Column(db.String(120))
    
    def __repr__(self):
        return f"{self.id}-{self.name}-{self.codebar}-{self.type}-{self.price}-{self.description}"
    

@app.route("/")
def hello_world():
    return "<p>this is an API created for academic reasons !</p>"
@app.route("/products",methods=["GET"])
def get_produit():
    products=Product.query.all()
    output=[]
    for product in products:
        product_data={'id':product.id,
                      'name':product.name,
                      'codebar':product.codebar,
                      'type':product.type,
                      'price':product.price,
                      'description':product.description}
        output.append(product_data)
        
    return{"products":output}
@app.route('/products/<id>')
def get_prod(id):
    p=Product.query.get_or_404(id)
    return jsonify({ 'name':p.name,
                      'codebar':p.codebar,
                      'type':p.type,
                      'price':p.price,
                      'description':p.description})
@app.route('/products',methods=["POST"])
def add_prof():
    product=Product(name=request.json['name'],
                    codebar=request.json['codebar'],
                    type=request.json['type'],
                    price=request.json['price'],
                    description=request.json['description'],)
    db.session.add(product)
    db.session.commit()
    return{'id':product.id}
@app.route('/products/<id>',methods=['DELETE'])
def delete_product(id):
    product=Product.query.get(id)
    if product is None:
        return{"error":"not found"}
    db.session.delete(product)
    db.session.commit()
    return {"message","product is added successfully"}
    