TABLES = [
    {
        "name": "sales_order_header",
        "sql_filename": "SalesOrderHeader.sql",
        "watermark_column": "ModifiedDate",
        "force_full_refresh": False,
    },
    {
        "name": "sales_order_detail",
        "sql_filename": "SalesOrderDetail.sql",
        "watermark_column": "ModifiedDate",
        "force_full_refresh": False,
    },
    {
        "name": "product",
        "sql_filename": "ProductionProduct.sql",
        "watermark_column": "ModifiedDate",
        "force_full_refresh": False,
    },
    {
        "name": "customer",
        "sql_filename": "SalesCustomer.sql",
        "watermark_column": "ModifiedDate",
        # BUG CONHECIDO: filtro incremental via parâmetro bindado (pyodbc)
        # retorna resultado incorreto nesta tabela (bind duplica a base
        # inteira em vez de filtrar). Causa raiz não identificada.
        # Mitigação: full-refresh sempre, até investigar a fundo.
        "force_full_refresh": True,
    },
    {
        "name": "person",
        "sql_filename": "Person.sql",
        "watermark_column": "ModifiedDate",
        # Mesmo bug do customer, em escala menor (vaza linhas na borda
        # do watermark). Mesma mitigação.
        "force_full_refresh": True,
    },
    {
        "name": "sales_territory",
        "sql_filename": "SalesTerritory.sql",
        "watermark_column": "ModifiedDate",
        "force_full_refresh": False,
    },
]
