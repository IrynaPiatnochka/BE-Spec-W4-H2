import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Product as ProductModel, db


class Product(SQLAlchemyObjectType):
    class Meta:
        model = ProductModel
      
class Query(graphene.ObjectType):
    products = graphene.List(Product)
    search_products = graphene.List(Product, name=graphene.String(), category=graphene.String())

    def resolve_products(self, info):
        return db.session.query(ProductModel).all()

    def resolve_search_products(root, info, name=None, category=None):
        query = db.session.query(ProductModel)
        if name:
            query = query.filter(ProductModel.name.ilike(f"%{name}%"))
        if category:
            query = query.filter(ProductModel.category.ilike(f"%{category}%"))
        results = query.all()
        return results

class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        quantity = graphene.Int(required=True)
        category = graphene.String(required=True)

    product = graphene.Field(Product)

    def mutate(self, info, name, price, quantity, category):
        product = ProductModel(name=name, price=price, quantity=quantity, category=category)
        db.session.add(product)
        db.session.commit() 
        db.session.refresh(product)
        return CreateProduct(product=product)

class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=False)
        price = graphene.Float(required=False)
        quantity = graphene.Int(required=False)
        category = graphene.String(required=False)

    product = graphene.Field(Product)

    def mutate(self, info, id, name=None, price=None, quantity=None, category=None):
        product = db.session.get(ProductModel, id)
        if not product:
            return None
        if name:
            product.name = name
        if price:
            product.price = price
        if quantity:
            product.quantity = quantity
        if category:
            product.category = category

        db.session.add(product)
        db.session.commit()
        return UpdateProduct(product=product)

class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    product = graphene.Field(Product)

    def mutate(self, info, id):
        product = db.session.get(ProductModel, id)
        print(info.context)
        if product:
            db.session.delete(product)
            db.session.commit()
        else:
            return DeleteProduct(product=product)
        
        return DeleteProduct(product=product)

class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()

