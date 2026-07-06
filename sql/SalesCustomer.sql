SELECT [CustomerID]
      ,[PersonID]
      ,[StoreID]
      ,[TerritoryID]
      ,[AccountNumber]
      ,[ModifiedDate]
  FROM [Sales].[Customer]
  WHERE (:modified_since IS NULL OR ModifiedDate > :modified_since)