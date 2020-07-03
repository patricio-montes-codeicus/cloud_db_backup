declare @dbName varchar(100)
declare @path varchar(100)
declare @pathFile varchar(200)
declare @fileName varchar(100)
declare @sqlQuery varchar(500)

declare @comillas_simples varchar(5) = ''''

set @dbName = '[PatentesDB]'
set @path = 'C:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\MSSQL\Backup\'
set @fileName = @dbname + '.bak'
set @pathFile = @path + @fileName

set @sqlQuery = 'BACKUP DATABASE ' + @dbName + ' TO DISK = ' + @comillas_simples + @pathFile + @comillas_simples

print @sqlQuery
exec (@sqlQuery)

/* 
WITH NOFORMAT, INIT,  NAME = N'PatentesDB-Full Database Backup', SKIP, NOREWIND, NOUNLOAD,  STATS = 10
GO*/