import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.orm import Session
from flask_sqlalchemy import SQLAlchemy
from traceback import format_exc

from procurement import app_logger, db, error_logger

session: Session = db.session


class BaseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at: db.Column(db.DateTime, server_default=datetime.now())
    updated_at: db.Column(db.DateTime, server_default=datetime.now())
    is_deleted: db.Column(db.Boolean, server_default=False)
    deleted_at: db.Column(db.DateTime, nullable=True)
