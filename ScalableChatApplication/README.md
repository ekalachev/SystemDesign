# System Design: Scalable Chat Application (with Notification Mechanism)

## 1. High-Level Architecture

At a high level, the architecture of a scalable chat application includes the following components:

- **Client**: Front-end interface used by users to interact with the chat system.
- **Load Balancer**: Distributes incoming traffic across multiple servers.
- **Message Gateway**: Handles real-time messaging and ensures messages are properly routed.
- **Presence Service**: Tracks users' online/offline status.
- **Messaging Service**: Handles core chat functionality, including one-on-one and group chats.
- **Storage Layer**: Stores message history, user data, and metadata like timestamps and presence info.
- **Notification Service**: Sends notifications when messages are received, especially if the user is offline.
- **Authentication Service**: Ensures secure login and session management.
- **Queue/Streaming System**: For reliable message delivery (e.g., Kafka, RabbitMQ).
- **Cache**: For low-latency data retrieval (e.g., Redis, Memcached).

---

## 2. Message Ingestion and Delivery

**Ingestion**: When a user sends a message, the client sends it to the chat server via a real-time protocol like WebSockets. To scale, **message brokers** like Kafka or RabbitMQ can be introduced to ensure reliable message delivery.

- **WebSockets**: Provides real-time, low-latency message delivery with bidirectional communication.
- **Message Queues**: Messages can be written to a queue before distribution to ensure durability and resilience.

**Delivery**: 
- For **one-on-one chats**, the message is routed to the target user's WebSocket connection.
- For **group chats**, the message is sent to all users in the group via their respective WebSocket connections.

---

## 3. Real-Time Communication Protocol

**WebSockets** is the ideal protocol for real-time, persistent, low-latency connections. For scalability:
- Use multiple WebSocket servers.
- Place a **load balancer** (e.g., NGINX, Envoy) in front to distribute traffic efficiently.

---

## 4. Data Storage

For chat history, store both **one-on-one** and **group chat messages** using:

- **NoSQL Database**: Databases like **Cassandra** or **MongoDB** scale horizontally and handle high write volumes.
- **Time-Series Database**: Databases like **InfluxDB** can efficiently store messages with timestamps.
- **Cold vs. Hot Storage**: Use **hot storage** (e.g., Redis) for recent messages and **cold storage** (e.g., S3) for older messages.

---

## 5. User Presence (Online/Offline Status)

Track users’ online/offline status using a **presence service**:

- **Redis**: An in-memory database for real-time user presence tracking.
- **Heartbeat Mechanism**: Clients send periodic pings to the server to indicate they’re online.
- **Broadcast**: Presence updates (online/offline) are broadcasted to friends/groups via the message broker.

---

## 6. Scalability and Fault Tolerance

To scale to millions of users:

- **Horizontal Scaling**: Scale WebSocket servers, databases, and other components horizontally.
- **Sharding**: Messages are **sharded** across different database clusters based on user or group IDs.
- **Replication**: Use database replication for high availability and fault tolerance.
- **Global Deployment with CDNs**: Use **Content Delivery Networks (CDNs)** to reduce latency for users worldwide.
- **Load Balancers**: Distribute WebSocket connections across multiple servers and handle failover.

---

## 7. Notification Service

To notify users of new messages when they are offline or the app is in the background, integrate a **push notification service**. You can use services like **Firebase Cloud Messaging (FCM)** or **Apple Push Notification Service (APNS)**. Here’s how it works:

- **Push Notification Integration**: 
  - When a message is sent and the recipient is offline or not actively using the app, a **notification event** is triggered.
  - The chat server sends the message to the **Notification Service**.
  - The Notification Service determines if the user is online or offline using the **Presence Service**.
  - If the user is offline, the Notification Service interacts with **Firebase Cloud Messaging (FCM)** or **Apple Push Notification Service (APNS)** to send a push notification to the user’s device.
  
- **Firebase Cloud Messaging (FCM)**: 
  - FCM is ideal for Android and iOS apps and allows sending notifications to users even when they are offline.
  - It integrates well with WebSocket servers and can notify the user as soon as a message is available.

- **Apple Push Notification Service (APNS)**:
  - APNS is the push notification service provided by Apple for iOS/macOS devices.
  - When the user is offline or the app is not in the foreground, APNS sends the notification to the user’s device.

---

## 8. Handling Offline Messages

To ensure users can receive messages that are sent when they are offline, follow this approach:

- **Message Queueing**:
  - If a user is offline or disconnected, messages intended for them can be stored in a **message queue** (e.g., Kafka, RabbitMQ).
  - The queue ensures that messages are **persistently stored** and **reliable delivery** is guaranteed once the user reconnects.

- **Persisting Offline Messages**:
  - Messages for offline users are stored in the **database** (e.g., Cassandra, MongoDB).
  - Once the user comes back online, their **client retrieves the messages** from the database or the queue.
  - **Message Acknowledgment**: When a user receives the stored messages, the system can remove the messages from the queue (or mark them as delivered).

- **Notification Upon Reconnection**:
  - When an offline user reconnects, the system sends a **notification** to the user’s device informing them of any **unread messages**.
  - The **Notification Service** checks for any pending messages in the **queue** or **database** and initiates a message pull to the client.

- **Message Fetching**:
  - On reconnecting, the **client** fetches unread messages from the **NoSQL database** (for history) or the **message queue** (for more recent messages) and displays them to the user.
  - This ensures that no message is lost, even when the user was offline.

---

## 9. Security and Privacy

Ensure the security and privacy of the chat system through:

- **Encryption**: Use **TLS** for communication and **encryption at rest** for message storage.
- **Authentication**: Implement OAuth 2.0 or JWT for secure user authentication.
- **Data Privacy**: Enable **end-to-end encryption (E2EE)** to ensure only the intended recipients can read messages.
- **Rate Limiting**: Implement rate limiting to prevent abuse and maintain system stability.

---

## 10. Summary

- **Real-time communication**: Handled via WebSockets, messages pass through a queue (e.g., Kafka) for reliable delivery.
- **Message storage**: Use NoSQL databases (e.g., Cassandra or MongoDB) for chat history, and Redis/Memcached for caching.
- **Presence tracking**: Use Redis with a heartbeat mechanism to track user presence in real-time.
- **Scalability**: Achieve scalability through horizontal scaling, sharding, load balancing, and geo-distribution.
- **Notification Service**: Integrate with Firebase Cloud Messaging (FCM) and Apple Push Notification Service (APNS) to notify offline users.
- **Handling Offline Messages**: Store messages in message queues (e.g., Kafka) for reliable delivery and pull from queues/databases when users reconnect.
- **Security**: Ensure end-to-end encryption, TLS, OAuth/JWT for secure communication and authentication.

---

This scalable architecture can grow as the user base increases while ensuring reliability, low-latency, and security.

---

**NOTE**: Explanation of Handling Offline Messages:
  - Message Queueing: Use Kafka or RabbitMQ to queue messages for users who are offline. This ensures messages are reliably stored and delivered once the user reconnects.
  - Database Storage: Messages are persisted in NoSQL databases for long-term storage, ensuring even if the queue is cleared, the messages are still retrievable.
  - Message Fetching: When an offline user reconnects, the client fetches the messages from the database or queue.
  - Notifications: The system ensures users are informed of unread messages through push notifications even if they were offline when the messages arrived.
