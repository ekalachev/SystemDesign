# Consistent Hashing

Consistent hashing is a method for distributing data across nodes in a distributed system, minimizing key reassignment when nodes are added or removed. This technique is particularly useful in systems where nodes frequently join or leave, such as caching systems, distributed databases, and load balancers.

---

## How It Works

1. **Hashing Nodes and Keys**:
   - Nodes and keys are mapped to a circular (ring) hash space using a hash function.
   - Each node and key gets a position on this ring.

2. **Assigning Keys to Nodes**:
   - Each key is assigned to the **first node** it encounters moving clockwise on the ring (its "successor node").
   - Each node is responsible for keys between itself and the previous node on the ring.

3. **Adding or Removing Nodes**:
   - **Adding a Node**: Only keys in the new node’s range are reassigned to it.
   - **Removing a Node**: Only keys from that node are reassigned, typically to the next node clockwise.
   - Minimal reassignments reduce data movement, maintaining efficient and scalable key distribution.

---

## Virtual Nodes (Replicas)

- **Purpose**: Virtual nodes represent each physical node multiple times on the ring, improving load balancing.
- **Benefits**: Virtual nodes spread each node’s responsibility across smaller segments, which helps balance the data distribution and prevents certain nodes from being overloaded.

---

## Benefits

1. **Minimal Rehashing**: Only a small subset of keys is remapped when nodes change, making it efficient and minimizing data movement.
2. **Scalability**: Nodes can be added or removed with minimal impact on the existing data distribution.
3. **Load Balancing**: Virtual nodes improve data distribution across nodes, preventing hotspots.

---

## Use Cases

### 1. Distributed Caching (e.g., Memcached, Redis)
   - Consistent hashing allows cache keys to be mapped across cache nodes. This setup enables easy addition or removal of cache nodes without a full reshuffle of keys.
   
### 2. Distributed Databases
   - **Cassandra** and **Amazon DynamoDB**: Use consistent hashing to distribute data across nodes, supporting dynamic scaling and balanced distribution.
   - **Riak**: Relies on consistent hashing to store data on nodes in a ring topology, allowing scalability and fault tolerance.
   - **Sharded Databases** (e.g., MongoDB, Redis): Consistent hashing can assign data to shards, making it easy to add or remove shards without disrupting the whole system.

### 3. Load Balancers in Microservices
   - Microservice architectures use consistent hashing in load balancers to route requests to specific backend servers consistently, which is useful for session management.

### 4. Distributed File Systems
   - Systems like **Ceph** and **GlusterFS** use consistent hashing to determine which node stores a specific file or object, supporting dynamic scaling and data redundancy.

### 5. Blockchain and Peer-to-Peer Networks
   - **Chord** and other P2P networks use consistent hashing to map data to nodes, supporting efficient and resilient data distribution across a changing network.

### 6. Real-Time Applications
   - Online gaming or live-streaming platforms use consistent hashing to balance users or sessions across servers, ensuring even load distribution and quick access times.

---

## Example

In a caching system:
   - Servers are assigned multiple virtual nodes on the hash ring.
   - Each session or cache key is mapped to the nearest virtual node.
   - When a new server is added, only the sessions or keys within the new server's range are moved, minimizing disruptions and reassignments.

---

Consistent hashing is ideal for scalable, fault-tolerant distributed systems that require balanced data distribution and minimal disruption when nodes are added or removed. It’s a powerful solution for distributed databases, caching, load balancing, and any system needing efficient, resilient scaling.
