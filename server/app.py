#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# --- ROUTES ---

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        # GET /messages: returns all messages ordered by created_at ascending
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return make_response(jsonify([m.to_dict() for m in messages]), 200)

    elif request.method == 'POST':
        # POST /messages: creates a new message from JSON or Form data
        data = request.get_json() if request.is_json else request.form
        
        try:
            new_msg = Message(
                body=data.get('body'),
                username=data.get('username')
            )
            db.session.add(new_msg)
            db.session.commit()
            return make_response(jsonify(new_msg.to_dict()), 201)
        except Exception as e:
            return make_response(jsonify({"errors": [str(e)]}), 400)

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    msg = Message.query.filter_by(id=id).first()
    
    if not msg:
        return make_response(jsonify({"error": "Message not found"}), 404)

    if request.method == 'PATCH':
        # PATCH /messages/<int:id>: updates the body
        data = request.get_json() if request.is_json else request.form
        
        if 'body' in data:
            msg.body = data.get('body')
            db.session.commit()
            return make_response(jsonify(msg.to_dict()), 200)
        return make_response(jsonify({"error": "No body provided"}), 400)

    elif request.method == 'DELETE':
        # DELETE /messages/<int:id>: deletes the message
        db.session.delete(msg)
        db.session.commit()
        # Returning an empty dict or a success message is standard
        return make_response(jsonify({}), 204)

if __name__ == '__main__':
    app.run(port=5555, debug=True)