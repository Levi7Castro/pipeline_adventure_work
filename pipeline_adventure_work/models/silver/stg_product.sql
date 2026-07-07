with source as (

    select * from {{ source('bronze', 'product') }}

),

deduplicated as (

    select
        *,
        row_number() over (
            partition by "ProductID"
            order by "ModifiedDate" desc
        ) as _row_num
    from source

),

renamed as (

    select
        "ProductID"                 as product_id,
        "ProductSubcategoryID"      as product_subcategory_id,
        "ProductModelID"            as product_model_id,

        "Name"                      as product_name,
        "ProductNumber"             as product_number,
        "Color"                     as color,
        "Size"                      as size,
        "SizeUnitMeasureCode"       as size_unit_measure_code,
        "WeightUnitMeasureCode"     as weight_unit_measure_code,
        "ProductLine"               as product_line,
        "Class"                     as class,
        "Style"                     as style,

        "MakeFlag"                  as is_manufactured,
        "FinishedGoodsFlag"         as is_finished_good,

        "SafetyStockLevel"          as safety_stock_level,
        "ReorderPoint"              as reorder_point,
        "DaysToManufacture"         as days_to_manufacture,

        cast("StandardCost" as numeric(19,4))  as standard_cost,
        cast("ListPrice" as numeric(19,4))     as list_price,
        cast("Weight" as numeric(19,4))        as weight,

        "SellStartDate"             as sell_start_date,
        "SellEndDate"               as sell_end_date,
        "DiscontinuedDate"          as discontinued_date,

        "ModifiedDate"              as modified_date,
        _loaded_at                  as loaded_at

    from deduplicated
    where _row_num = 1

)

select * from renamed
