
from flask import Flask
from flask_graphql import GraphQLView
import graphene
from models import db
from schema import Query, Mutation

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bakery_db'

db.init_app(app)

schema = graphene.Schema(query=Query, mutation=Mutation) 

app.add_url_rule( 
    '/graphql',
    view_func= GraphQLView.as_view('graphql', schema=schema, graphiql=True) 
)

if __name__ == '__main__':

    with app.app_context():

        db.create_all()

    app.run(debug=True)