import pytest
from server.models import Message, db

def test_has_correct_columns(test_app):
    with test_app.app_context():
        msg = Message(body="Hello", username="Mike")
        db.session.add(msg)
        db.session.commit()
        # Check column values
        assert msg.body == "Hello"
        assert msg.username == "Mike"
        assert msg.id is not None
