import dlt
from pyspark.sql.functions import col, expr

@dlt.view
def users():
  return spark.readStream.table("cdc_data.users")

dlt.create_streaming_table("target")

dlt.apply_changes(
  target = "target",
  source = "users",
  keys = ["userId"],
  sequence_by = col("sequenceNum"),
  apply_as_deletes = expr("operation = 'DELETE'"),
  except_column_list = ["operation", "sequenceNum"],
  stored_as_scd_type = "2"
)
