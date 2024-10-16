from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StringType, TimestampType, IntegerType


# 1. Create Spark session with Kafka and Cassandra integration
def create_spark_session(app_name: str, kafka_package: str, cassandra_package: str) -> SparkSession:
    return SparkSession.builder \
        .appName("WebsiteClickStreamProcessingWithCassandra") \
        .config("spark.jars.packages", f"{kafka_package},{cassandra_package}") \
        .config("spark.cassandra.connection.host", "localhost") \
        .config("spark.cassandra.connection.port", "9042") \
        .config("spark.sql.streaming.kafka.consumer.cache.timeout", "5000") \
        .config("spark.sql.streaming.checkpointLocation", "/tmp/spark-checkpoints") \
        .config("spark.ui.showConsoleProgress", "false") \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "4g") \
        .getOrCreate()


# 2. Define the schema for incoming Kafka data
def define_clickstream_schema() -> StructType:
    return StructType() \
        .add("user_id", StringType()) \
        .add("page", StringType()) \
        .add("timestamp", StringType()) \
        .add("action", StringType()) \
        .add("session_id", StringType())


# 3. UDF to calculate the length of the longest substring without repeating characters
def length_of_longest_substring(s: str) -> int:
    start = 0
    max_len = 0
    char_index = {}

    for end in range(len(s)):
        if s[end] in char_index:
            start = max(start, char_index[s[end]] + 1)
        char_index[s[end]] = end
        max_len = max(max_len, end - start + 1)

    return max_len


# 4. Register UDFs in Spark
def register_udfs(spark: SparkSession):
    # Registering the UDF for calculating the longest substring length
    spark.udf.register("length_of_longest_substring_udf", length_of_longest_substring, IntegerType())


# 5. Main Pipeline Function
def process_clickstream_data(spark: SparkSession):
    # Define the schema
    schema = define_clickstream_schema()

    # Read data from Kafka
    clickstream_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9093") \
        .option("subscribe", "website_clicks") \
        .option("kafkaConsumer.pollTimeoutMs", "512000") \
        .load()

    # Cast the value from Kafka as string and parse JSON
    clickstream_string_df = clickstream_df.selectExpr("CAST(value AS STRING) as json_value")

    # Parse the JSON data
    clickstream_parsed_df = clickstream_string_df \
        .select(from_json(col("json_value"), schema).alias("data")) \
        .select("data.*")

    # Convert the timestamp field from string to TimestampType
    clickstream_parsed_df = clickstream_parsed_df.withColumn(
        "timestamp", clickstream_parsed_df["timestamp"].cast(TimestampType())
    )

    # Add a column to calculate the length of the longest substring from session_id
    clickstream_with_length_of_longest_substring_df = clickstream_parsed_df.withColumn(
        "length_of_longest_substring",
        udf(length_of_longest_substring, IntegerType())(col("session_id"))
    )

    # Drop the 'session_id' column as it is no longer needed
    clickstream_cleaned_df = clickstream_with_length_of_longest_substring_df.drop("session_id")

    # Write the resulting DataFrame to Cassandra
    query = clickstream_cleaned_df.writeStream \
        .outputMode("append") \
        .option("checkpointLocation", "/tmp/spark-checkpoints") \
        .foreachBatch(lambda df, epoch_id: df.write \
                      .format("org.apache.spark.sql.cassandra") \
                      .options(table="clicks", keyspace="clickstream_ks") \
                      .mode("append") \
                      .save()) \
        .start()

    query.awaitTermination()


# 6. Entry Point
if __name__ == "__main__":
    # Initialize Spark session with Kafka and Cassandra packages
    spark = create_spark_session(
        app_name="WebsiteClickStreamProcessingWithCassandra",
        kafka_package="org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2",
        cassandra_package="com.datastax.spark:spark-cassandra-connector_2.12:3.1.0"
    )

    # Register UDFs
    register_udfs(spark)

    # Process clickstream data and write to Cassandra
    process_clickstream_data(spark)
