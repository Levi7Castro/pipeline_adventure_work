with detail as (

    select * from {{ ref('stg_sales_order_detail') }}

),

header as (

    select * from {{ ref('stg_sales_order_header') }}

),

joined as (

    select
        detail.sales_order_detail_id,
        detail.sales_order_id,
        detail.product_id,
        detail.special_offer_id,

        header.customer_id,
        header.territory_id,
        header.salesperson_id,          -- atributo degenerado, sem dimensão própria por ora
        header.ship_method_id,

        header.order_date::date         as order_date,
        header.due_date::date           as due_date,
        header.ship_date::date          as ship_date,

        detail.order_qty,
        detail.unit_price,
        detail.unit_price_discount,
        detail.line_total,

        header.is_online_order,
        header.status                   as order_status,

        detail.modified_date

    from detail
    inner join header
        on detail.sales_order_id = header.sales_order_id

)

select * from joined
