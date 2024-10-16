/* CREATE the keyspace WITH simple replication */
CREATE KEYSPACE IF NOT EXISTS clickstream_ks
WITH replication = {'class':'SimpleStrategy', 'replication_factor':1};

/* Use the keyspace */
USE clickstream_ks;

/* CREATE the table FOR storing click events
   This table will store user click actions along with a timestamp */
CREATE TABLE IF NOT EXISTS clicks (
    user_id UUID,               -- Changed to UUID for user_id
    page TEXT,                  -- Keep page as TEXT (URL or page identifier)
    timestamp TIMESTAMP,        -- Keep timestamp for the event
    action TEXT,                -- The action performed by the user (click, scroll, etc.)
    length_of_longest_substring INT,  -- Keep this as an integer for the calculated length
    PRIMARY KEY (user_id, timestamp)  -- Partition by user_id, cluster by timestamp
);