import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf, to_json, struct
from pyspark.sql.types import StructType, StringType, TimestampType, IntegerType


# 1. Create Spark session
def create_spark_session(app_name: str, kafka_package: str) -> SparkSession:
    return SparkSession.builder \
        .appName(app_name) \
        .config("spark.jars.packages", kafka_package) \
        .getOrCreate()


# 2. Define the schema for incoming Kafka data
def define_clickstream_schema() -> StructType:
    return StructType() \
        .add("user_id", StringType()) \
        .add("page", StringType()) \
        .add("timestamp", StringType()) \
        .add("action", StringType()) \
        .add("session_id", StringType())


# 3. UDF to check if a page (domain) is alive by making an HTTP request
def check_if_alive(url: str) -> bool:
    try:
        response = requests.head(url, timeout=3)  # Use HEAD request to check availability
        return response.status_code == 200
    except requests.RequestException:
        return False


# 4. UDF to calculate the length of the longest substring without repeating characters
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


# 5. Register UDFs in Spark
def register_udfs(spark: SparkSession):
    # Registering the UDF for calculating the longest substring length
    spark.udf.register("length_of_longest_substring_udf", length_of_longest_substring, IntegerType())
    # The UDF for checking if the page is alive (uncomment if you want to use it)
    # spark.udf.register("is_alive_udf", check_if_alive, BooleanType())


# 6. Main Pipeline Function
def process_clickstream_data(spark: SparkSession):
    # Define the schema
    schema = define_clickstream_schema()

    # Read data from Kafka
    clickstream_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9093") \
        .option("subscribe", "website_clicks") \
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

    # Convert the resulting DataFrame to JSON format
    clickstream_json_df = clickstream_with_length_of_longest_substring_df.withColumn(
        "json_output",
        to_json(
            struct(col("user_id"), col("page"), col("timestamp"), col("action"), col("length_of_longest_substring")))
    )

    # Write the resulting JSON DataFrame to the console
    query = clickstream_json_df.select("json_output").writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", "false") \
        .start()

    query.awaitTermination()


# 7. Entry Point
if __name__ == "__main__":
    # Initialize Spark session
    spark = create_spark_session("WebsiteClickStreamProcessingWithHealthCheck",
                                 "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2")

    # Register UDFs
    register_udfs(spark)

    # Process clickstream data
    process_clickstream_data(spark)
