from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

# Convention for naming constraints (standard in these labs to avoid migration errors)
metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    username = db.Column(db.String)
    
    # Timestamps
    # server_default=db.func.now() sets the time when the record is created in the DB
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    # onupdate=db.func.now() updates the timestamp every time the row is changed
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Serialization rules
    # This excludes these fields from the JSON output to keep it clean
    serialize_rules = ('-created_at', '-updated_at')

    def __repr__(self):
        return f'<Message {self.id} | User: {self.username}>'