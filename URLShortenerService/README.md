# System Design: Scalable URL Shortener Service

---

## 1. High-Level Architecture

The URL shortener service consists of the following components:

- **API Layer**: RESTful APIs for users to shorten URLs and redirect to long URLs.
- **URL Generation Service**: Generates unique short URLs for each long URL.
- **Database Layer**: Scalable storage for long URLs, short URLs, and metadata (e.g., expiration time).
- **Caching Layer**: Stores frequently accessed short-to-long URL mappings to reduce database load.
- **Redirection Service**: Handles user redirection from the short URL to the original long URL.
- **Load Balancer**: Distributes incoming traffic across multiple API servers.
- **Monitoring and Analytics**: (Optional) Tracks performance and usage statistics.

---

## 2. Key Components and How They Work

### **URL Shortening Logic**

To generate a **unique short URL** for each long URL, consider the following approaches:

- **Base62 Encoding**:
  - Generate a unique ID (e.g., auto-incremented ID or UUID).
  - Encode the ID using Base62 to create a short string.
  - This method avoids collisions and ensures shorter URLs.

- **Hashing the URL**:
  - Use hashing algorithms like MD5 or SHA-256 on the long URL.
  - Handle collisions by appending additional characters or re-hashing.

**Process:**

1. User submits a long URL via the API.
2. The system generates a unique short URL.
3. The mapping between the short URL and the long URL is stored in the database.

### **Data Storage**

- **Relational Database (SQL)**:
  - Use databases like PostgreSQL or MySQL.
  - Table schema:
    - `id` (Primary Key)
    - `short_url` (Unique)
    - `long_url`
    - `creation_time`
    - `expiration_time` (optional)

- **NoSQL Database**:
  - Use databases like Cassandra or DynamoDB for horizontal scalability.
  - Suitable for key-based lookups and large-scale data.

- **Sharding**:
  - Distribute data across multiple databases based on short URL hash or user ID.

### **API Design**

- **POST /shorten**:
  - **Request**:
    ```json
    {
      "long_url": "https://www.example.com",
      "expiration_time": "optional"
    }
    ```
  - **Response**:
    ```json
    {
      "short_url": "https://short.ly/abc123"
    }
    ```

- **GET /:short_url**:
  - Redirects to the original long URL.
  - Example: Visiting `https://short.ly/abc123` redirects the user.

---

## 3. Scalability and Fault Tolerance

### **Scaling the Service**

- **Horizontal Scaling of API Servers**:
  - Add more servers as traffic increases.
  - Use **load balancers** to distribute requests.

- **Database Partitioning**:
  - Partition or shard databases to handle billions of URLs.

- **Caching Layer**:
  - Implement caching with Redis or Memcached.
  - Cache frequently accessed short-to-long URL mappings.

### **Fault Tolerance**

- **Replication**:
  - Replicate databases across regions or availability zones.

- **Backup and Restore**:
  - Regular backups and automated restoration processes.

- **Distributed ID Generation**:
  - Use systems like **Snowflake IDs** or **UUIDs** for unique ID generation.

---

## 4. Caching

- **Purpose**:
  - Reduce database load.
  - Improve latency for redirection.

- **Implementation**:
  - Use Redis as a caching layer.
  - Cache mappings between short URLs and long URLs.
  - Set appropriate TTLs for cache entries.

---

## 5. Security

- **Prevent Malicious URLs**:
  - Validate URLs before shortening.
  - Use services like **Google Safe Browsing** for URL verification.

- **Rate Limiting**:
  - Implement limits on the number of URLs a user can shorten per hour/day.

- **HTTPS Enforcement**:
  - Serve all endpoints over HTTPS.
  - Protect against man-in-the-middle attacks.

---

## 6. Handling Expiration of URLs (Optional)

- **Expiration Time**:
  - Store `expiration_time` in the database.
  - Check expiration before redirection.

- **Cleanup Process**:
  - Use background jobs to remove or deactivate expired URLs.

---

## 7. Trade-offs and Considerations

- **Collision Handling**:
  - Ensure uniqueness in short URLs.
  - Implement collision resolution strategies if using hashing.

- **Custom Short URLs**:
  - Allow users to specify custom aliases.
  - Validate to prevent duplication or offensive terms.

---

## 8. Example Flow

### **URL Shortening**

1. User calls `POST /shorten` with a long URL.
2. System generates a short URL using Base62 encoding.
3. Mapping is stored in the database.
4. Short URL is returned to the user.

### **Redirection**

1. User visits the short URL.
2. System checks the cache for the long URL.
   - If found, redirects immediately.
   - If not found, fetches from the database, updates the cache, and redirects.

---

## 9. Conclusion

The designed URL shortener service ensures:

- **Scalability**:
  - Handles billions of URLs and millions of redirects.
  - Uses horizontal scaling and sharding.

- **High Availability**:
  - Implements replication and load balancing.

- **Low Latency**:
  - Utilizes caching mechanisms.

- **Security**:
  - Validates URLs and uses HTTPS.
  - Implements rate limiting.

- **Reliability**:
  - Provides backup and recovery options.
  - Uses fault-tolerant ID generation methods.

By following this design, the service can efficiently shorten URLs and handle high volumes of redirection traffic.