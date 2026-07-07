with customer as (

    select * from {{ ref('stg_customer') }}

),

person as (

    select * from {{ ref('stg_person') }}

),

joined as (

    select
        customer.customer_id,
        customer.person_id,
        customer.store_id,
        customer.territory_id,
        customer.account_number,

        person.person_type,
        person.first_name,
        person.middle_name,
        person.last_name,
        concat_ws(' ', person.first_name, person.middle_name, person.last_name) as full_name,

        customer.modified_date

    from customer
    left join person
        on customer.person_id = person.business_entity_id

)

select * from joined
