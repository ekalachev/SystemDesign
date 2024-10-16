/* CREATE the keyspace WITH simple replication */
CREATE KEYSPACE IF NOT EXISTS clickstream_ks
WITH replication = {'class':'SimpleStrategy', 'replication_factor':1};

/* Use the keyspace */
USE clickstream_ks;

/* CREATE the table FOR storing click events
   This table will store user click actions along with a timestamp */
CREATE TABLE IF NOT EXISTS clicks (
user_id text,
page text,
timestamp timestamp,
action text,
PRIMARY KEY (user_id, timestamp)
);