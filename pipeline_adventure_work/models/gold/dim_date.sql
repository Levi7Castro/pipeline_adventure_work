with date_spine as (

    select
        generate_series(
            (select min(order_date) from {{ ref('stg_sales_order_header') }})::date,
            (select max(order_date) from {{ ref('stg_sales_order_header') }})::date,
            interval '1 day'
        )::date as date_day

),

enriched as (

    select
        date_day,
        extract(year from date_day)::int          as year,
        extract(quarter from date_day)::int        as quarter,
        extract(month from date_day)::int          as month,
        to_char(date_day, 'Month')                 as month_name,
        extract(day from date_day)::int            as day_of_month,
        extract(dow from date_day)::int             as day_of_week,
        to_char(date_day, 'Day')                    as day_name,
        extract(week from date_day)::int            as week_of_year,
        case when extract(dow from date_day) in (0, 6) then true else false end as is_weekend

    from date_spine

)

select * from enriched
