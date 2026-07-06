with source as (

    select * from {{ source('bronze', 'sales_order_header') }}

),

deduplicated as (

    select
        *,
        row_number() over (
            partition by "SalesOrderID"
            order by "ModifiedDate" desc
        ) as _row_num
    from source

),

renamed as (

    select
        "SalesOrderID"              as sales_order_id,
        "CustomerID"                as customer_id,
        "SalesPersonID"             as salesperson_id,
        "TerritoryID"               as territory_id,
        "BillToAddressID"           as bill_to_address_id,
        "ShipToAddressID"           as ship_to_address_id,
        "ShipMethodID"              as ship_method_id,
        "CreditCardID"              as credit_card_id,
        "CurrencyRateID"            as currency_rate_id,

        "RevisionNumber"            as revision_number,
        "Status"                    as status,
        "OnlineOrderFlag"           as is_online_order,
        "PurchaseOrderNumber"       as purchase_order_number,
        "AccountNumber"             as account_number,
        "CreditCardApprovalCode"    as credit_card_approval_code,
        "Comment"                   as comment,

        "OrderDate"                 as order_date,
        "DueDate"                   as due_date,
        "ShipDate"                  as ship_date,

        cast("SubTotal" as numeric(19,4))   as subtotal,
        cast("TaxAmt"   as numeric(19,4))   as tax_amount,
        cast("Freight"  as numeric(19,4))   as freight,
        cast("SubTotal" as numeric(19,4))
            + cast("TaxAmt" as numeric(19,4))
            + cast("Freight" as numeric(19,4)) as total_due,

        "ModifiedDate"              as modified_date,
        _loaded_at                  as loaded_at

    from deduplicated
    where _row_num = 1

)

select * from renamed
