# Consistent Hashing

Consistent hashing is a method for distributing data across nodes in a distributed system, minimizing key reassignment when nodes are added or removed.

## How It Works

1. **Hashing Nodes and Keys**:
   - Nodes and keys are mapped to a circular (ring) hash space using a hash function.
   - Each node and key gets a position on this ring.

2. **Assigning Keys to Nodes**:
   - Each key is assigned to the **first node** it meets moving clockwise on the ring (its "successor node").
   - Each node is responsible for keys between itself and the previous node on the ring.

3. **Adding or Removing Nodes**:
   - **Adding a Node**: Only keys in the new node’s range are reassigned to it.
   - **Removing a Node**: Only keys from that node are reassigned, typically to the next node clockwise.
   - Minimal reassignments help reduce data movement.

## Virtual Nodes (Replicas)

- Virtual nodes (multiple positions per physical node) help balance the load.
- Virtual nodes spread each node’s responsibility across smaller segments, balancing data distribution.

## Benefits

- **Minimal Rehashing**: Only a small subset of keys is remapped when nodes change.
- **Scalability**: Easy to add or remove nodes with minimal data movement.
- **Load Balancing**: Virtual nodes improve data distribution across nodes.

## Use Cases

- **Distributed Caching** (e.g., Memcached)
- **Distributed Databases**
- **Load Balancers** in microservices

## Example

In a caching system:
   - Servers are assigned multiple virtual nodes on the hash ring.
   - A session key is mapped to the nearest virtual node on the ring.
   - Adding a new server only moves sessions within the new server's range, minimizing disruptions.

Consistent hashing is ideal for scalable, fault-tolerant distributed systems that need efficient, balanced data distribution with minimal disruption.
