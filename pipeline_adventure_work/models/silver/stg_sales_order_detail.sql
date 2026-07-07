with source as (

    select * from {{ source('bronze', 'sales_order_detail') }}

),

deduplicated as (

    select
        *,
        row_number() over (
            partition by "SalesOrderDetailID"
            order by "ModifiedDate" desc
        ) as _row_num
    from source

),

renamed as (

    select
        "SalesOrderDetailID"        as sales_order_detail_id,
        "SalesOrderID"              as sales_order_id,
        "ProductID"                 as product_id,
        "SpecialOfferID"            as special_offer_id,

        "CarrierTrackingNumber"     as carrier_tracking_number,
        "OrderQty"                  as order_qty,

        cast("UnitPrice" as numeric(19,4))          as unit_price,
        cast("UnitPriceDiscount" as numeric(19,4))  as unit_price_discount,
        cast("LineTotal" as numeric(19,4))          as line_total,

        "ModifiedDate"              as modified_date,
        _loaded_at                  as loaded_at

    from deduplicated
    where _row_num = 1

)

select * from renamed
