from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from .models import db, Message  # use relative import

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    CORS(app)

    # Routes
    @app.route("/messages", methods=["GET", "POST"])
    def messages():
        if request.method == "GET":
            msgs = Message.query.order_by(Message.created_at.asc()).all()
            return jsonify([m.to_dict() for m in msgs]), 200
        if request.method == "POST":
            data = request.get_json()
            msg = Message(body=data["body"], username=data["username"])
            db.session.add(msg)
            db.session.commit()
            return jsonify(msg.to_dict()), 201

    @app.route("/messages/<int:id>", methods=["PATCH", "DELETE"])
    def message_detail(id):
        msg = Message.query.get_or_404(id)
        if request.method == "PATCH":
            data = request.get_json()
            msg.body = data.get("body", msg.body)
            db.session.commit()
            return jsonify(msg.to_dict()), 200
        if request.method == "DELETE":
            db.session.delete(msg)
            db.session.commit()
            return "", 204

    return app

# Only run server if executed directly
if __name__ == "__main__":
    create_app().run(port=5555)
