
# Database Scaling: Sharding, Replication, and Their Combination

### 1. Horizontal vs Vertical Scaling

**Horizontal scaling (Sharding):**
Sharding is the process of splitting a database horizontally across multiple servers, where each server stores only a subset of the data (called a shard). For instance, if you have a table with a million records, you can divide it across several servers, each holding a unique portion of the records. This helps distribute load and improve performance since queries can be handled by different servers in parallel.

**Vertical scaling:**
Vertical scaling increases the power of a single server by adding more CPU, memory, or storage. All data stays on one server. This is simpler to manage but has hardware limits and can become inefficient or expensive.

### 2. Replication

Replication involves copying the same database across multiple servers. This can improve performance (especially for read-heavy workloads) and ensure high availability. The two common types are:

- **Master-slave replication:** The master server handles all write requests, and changes are propagated to slave servers, which handle read requests.
- **Multi-master replication:** Multiple servers can handle both read and write requests, and the data is synchronized between them.

Replication improves read performance but doesn’t split data like sharding.

### 3. Combining Sharding and Replication

Sharding and replication can be combined to build highly scalable and fault-tolerant systems. Here's how:

- **Sharding** splits the data across multiple servers (shards), where each server handles a portion of the data.
- **Replication** then creates multiple copies of each shard. These replicas can handle read requests and ensure high availability.

This approach allows for:
- **Scalability** through sharding — distributing data across multiple servers.
- **Fault tolerance and read performance** through replication — providing multiple copies of the data.

This hybrid solution is used in large-scale systems such as Google Spanner and MySQL Cluster.
