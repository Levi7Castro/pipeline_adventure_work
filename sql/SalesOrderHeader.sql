SELECT
     SalesOrderID
    ,RevisionNumber
    ,OrderDate
    ,DueDate
    ,ShipDate
    ,Status
    ,OnlineOrderFlag
    ,PurchaseOrderNumber
    ,AccountNumber
    ,CustomerID
    ,SalesPersonID
    ,TerritoryID
    ,BillToAddressID
    ,ShipToAddressID
    ,ShipMethodID
    ,CreditCardID
    ,CreditCardApprovalCode
    ,CurrencyRateID
    ,SubTotal
    ,TaxAmt
    ,Freight
    ,Comment
    ,ModifiedDate
FROM Sales.SalesOrderHeader
WHERE (:modified_since IS NULL OR ModifiedDate > :modified_since)
