import uuid

from sqlalchemy.dialects.postgresql import JSON

from bookstore.settings import db


class DebeziumRecord(db.Model):
    __tablename__ = "debezium_outbox_records"

    id = db.Column(db.String, primary_key=True, default=uuid.uuid4)
    event_id = db.Column(db.String)
    event_unique_identifier = db.Column(db.String, nullable=False)
    payload = db.Column(JSON, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
