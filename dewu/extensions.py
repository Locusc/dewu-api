from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_redis import FlaskRedis


db = SQLAlchemy()
moment = Moment()
redis_store = FlaskRedis()

