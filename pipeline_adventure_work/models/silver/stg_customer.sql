with source as (

    select * from {{ source('bronze', 'customer') }}

),

deduplicated as (

    select
        *,
        row_number() over (
            partition by "CustomerID"
            order by "ModifiedDate" desc
        ) as _row_num
    from source

),

renamed as (

    select
        "CustomerID"                as customer_id,
        "PersonID"                  as person_id,
        "StoreID"                   as store_id,
        "TerritoryID"               as territory_id,

        "AccountNumber"             as account_number,

        "ModifiedDate"              as modified_date,
        _loaded_at                  as loaded_at

    from deduplicated
    where _row_num = 1

)

select * from renamed
