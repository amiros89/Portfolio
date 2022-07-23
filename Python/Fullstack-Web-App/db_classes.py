from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from app import app
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    plan = db.Column(db.String(250), nullable=False)
    register_date = db.Column(db.DateTime(250), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    is_confirmed = db.Column(db.Boolean, nullable=False)
    queries = db.relationship("Query", back_populates="executed_by")
    email_notifications = db.Column(db.Boolean, nullable=False, default=True)


class Query(db.Model):
    __tablename__ = "queries"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    executed_by = relationship("User", back_populates="queries")
    runner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_time = db.Column(db.DateTime(250), nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime(250), nullable=True)
    ebay_url = db.Column(db.Text, nullable=False)
    num_of_products = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(250), nullable=False, default="In Progress")
    type = db.Column(db.String(250), nullable=False)
    products = db.relationship("Product")
    settings = db.relationship("QuerySettings", cascade="all,delete-orphan", uselist=False)


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    query_id = db.Column(UUID(as_uuid=True), db.ForeignKey('queries.id'), primary_key=True)
    amazon_title = db.Column(db.Text, nullable=False)
    amazon_link = db.Column(db.String, nullable=False)
    asin = db.Column(db.String(250), nullable=False)
    ebay_title = db.Column(db.Text, nullable=False)
    ebay_url = db.Column(db.Text, nullable=False)
    lifetime_sales = db.Column(db.Integer,nullable=False,default=0)
    recent_sales = db.Column(db.Integer,nullable=False,default=0)

class QuerySettings(db.Model):
    __tablename__ = "query_settings"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    query_id = db.Column(UUID(as_uuid=True), db.ForeignKey('queries.id'), primary_key=True)
    num_of_ebay_items = db.Column(db.Integer, nullable=False, default=1)
    num_of_seller_top_selling = db.Column(db.Integer, nullable=False, default=1)
    num_of_days_of_recent_sales = db.Column(db.Integer, nullable=False, default=30)
    num_of_days_of_most_recent_sales = db.Column(db.Integer, nullable=False, default=7)
    num_of_sales_in_recent_days = db.Column(db.Integer, nullable=False, default=5)
    num_of_sales_in_most_recent_days = db.Column(db.Integer, nullable=False, default=1)


# if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
db.create_all()
