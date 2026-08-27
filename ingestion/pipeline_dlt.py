import dlt
import duckdb

pipeline = dlt.pipeline(
    pipeline_name="contoso_ingestion",
    destination=dlt.destinations.duckdb("data/database/contoso_dwh.duckdb"),
    dataset_name="bronze"
)

@dlt.resource
def load_parquet_tables():
    con = duckdb.connect()
    tables = [
        "currencyexchange", "customer", "date", 
        "orderrows", "orders", "product", "sales", "store"
    ]
    for table in tables:
        file_path = f"data/raw/{table}.parquet"
        # Executa a query no DuckDB e gera o ponteiro Arrow (streaming sem Pandas/RAM)
        data = con.execute(f"SELECT * FROM '{file_path}'").arrow()
        yield dlt.mark.with_table_name(data, table)

if __name__ == "__main__":
    load_info = pipeline.run(load_parquet_tables(), write_disposition="replace")
    print(load_info)