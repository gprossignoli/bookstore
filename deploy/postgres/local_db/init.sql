CREATE ROLE debezium_user REPLICATION LOGIN PASSWORD 'debezium_password';


CREATE ROLE outbox_replication_group;
GRANT outbox_replication_group TO db_user;
GRANT outbox_replication_group TO debezium_user;

--ALTER TABLE bookstore.public.outbox_records OWNER TO outbox_replication_group;
