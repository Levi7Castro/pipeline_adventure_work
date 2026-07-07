with source as (

    select * from {{ source('bronze', 'sales_territory') }}

),

deduplicated as (

    select
        *,
        row_number() over (
            partition by "TerritoryID"
            order by "ModifiedDate" desc
        ) as _row_num
    from source

),

renamed as (

    select
        "TerritoryID"               as territory_id,

        "Name"                      as territory_name,
        "CountryRegionCode"         as country_region_code,
        "Group"                     as territory_group,

        cast("SalesYTD" as numeric(19,4))       as sales_ytd,
        cast("SalesLastYear" as numeric(19,4))  as sales_last_year,
        cast("CostYTD" as numeric(19,4))        as cost_ytd,
        cast("CostLastYear" as numeric(19,4))   as cost_last_year,

        "ModifiedDate"              as modified_date,
        _loaded_at                  as loaded_at

    from deduplicated
    where _row_num = 1

)

select * from renamed
