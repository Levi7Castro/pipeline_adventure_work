with source as (

    select * from {{ source('bronze', 'person') }}

),

deduplicated as (

    select
        *,
        row_number() over (
            partition by "BusinessEntityID"
            order by "ModifiedDate" desc
        ) as _row_num
    from source

),

renamed as (

    select
        "BusinessEntityID"          as business_entity_id,

        "PersonType"                as person_type,
        "Title"                     as title,
        "FirstName"                 as first_name,
        "MiddleName"                as middle_name,
        "LastName"                  as last_name,
        "Suffix"                    as suffix,

        "EmailPromotion"            as email_promotion,

        "ModifiedDate"              as modified_date,
        _loaded_at                  as loaded_at

    from deduplicated
    where _row_num = 1

)

select * from renamed
