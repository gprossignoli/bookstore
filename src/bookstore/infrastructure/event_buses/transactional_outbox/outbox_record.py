import uuid

from sqlalchemy.dialects.postgresql import JSON

from bookstore.settings import db


class OutboxRecord(db.Model):
    __tablename__ = "outbox_records"

    id = db.Column(db.String, primary_key=True, default=uuid.uuid4)
    event_id = db.Column(db.String, primary_key=True)
    event_unique_identifier = db.Column(db.String, nullable=False)
    payload = db.Column(JSON, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    delivered_at = db.Column(
        db.DateTime(timezone=True), nullable=True, default=None, server_default=None
    )
    delivery_errors = db.Column(db.Integer, nullable=False, default=0)
    delivery_paused_at = db.Column(
        db.DateTime(timezone=True), nullable=True, default=None, server_default=None
    )
