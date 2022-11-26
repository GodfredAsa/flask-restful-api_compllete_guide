from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout

app = Flask(__name__)

jwt = JWTManager(app)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

app.config["JWT_SECRET_KEY"] = "jose"

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
