import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when


def main():
    spark = (
        SparkSession.builder
            .appName("ChampionsPorraPipeline")
            .getOrCreate()
    )

    base      = os.path.dirname(os.path.dirname(__file__))
    p_path    = os.path.join(base, "data", "partidos.parquet")
    pred_path = os.path.join(base, "data", "predicciones.parquet")
    out_path  = os.path.join(base, "data", "training.parquet")

    # 1) PARTIDOS: leer directamente
    partidos_df = spark.read.parquet(p_path)

    partidos_df.printSchema()
    partidos_df.show(5, False)

    # 2) PREDICCIONES: leer directamente
    predicciones_df = spark.read.parquet(pred_path)

    predicciones_df.printSchema()
    predicciones_df.show(5, False)

    # 3) FEATURE ENGINEERING
    partidos_df = partidos_df.withColumn(
        "diff_real",
        col("goles_local") - col("goles_visitante")
    )

    joined = predicciones_df.join(
        partidos_df.select(col("id").alias("partido_id"), "diff_real"),
        on="partido_id", how="inner"
    )

    df = joined.withColumn(
        "diff_pred", col("goles_local") - col("goles_visitante")
    ).withColumn(
        "label",
        when(col("diff_real") > 0, 1)
        .when(col("diff_real") < 0, 2)
        .otherwise(0)
    )

    # 4) ESCRITURA
    df.select("diff_pred", "label") \
      .write.mode("overwrite") \
      .parquet(out_path)

    print(f"Pipeline completado: {out_path}")

    spark.stop()


if __name__ == "__main__":
    main()
