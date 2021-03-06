import pyodbc 
import logging
from src.DBConnections.expected_connection import ExpectedConnection
from src.DBConnections.connection_factory import DBConnectionFactory
from src.ClientsImpl.google_drive_impl import GoogleDriveImpl
from src.ServicesImpl.file_manager_impl import FileManagerImpl

expected_connection = ExpectedConnection()
#TODO: Evaluar mejor forma de recibir al cronear. Y controlar las entradas. 
print("Tipo de Host 1-MSSQLServer 2-MySQL 3-PostgreSQL 4-Sybase")
expected_connection.typehost = input()
print("Host:")
expected_connection.host = input()
print("Port:")
expected_connection.port = input()
print("Username:")
expected_connection.username = input()
print("password:")
expected_connection.password = input()
print("DataBase:")
expected_connection.database = input()


factory_connection = DBConnectionFactory()
logging.debug("Creación de Data Source")
logging.info("Data Source pretendido." + 
             "Tipo de Host:" + expected_connection.typehost + "Host:" + expected_connection.host +
             "Puerto:" + expected_connection.port + "Usuario:" + expected_connection.username +
             "Contraseña:" + expected_connection.password + "Base de Datos:" + expected_connection.database)

db_connection = factory_connection.create(expected_connection.get_db_type(int(expected_connection.typehost)))

print("db type connect: " + expected_connection.get_db_type(int(expected_connection.typehost)))
input()
print("db connection: " + db_connection.build_connection(expected_connection))
input()

logging.debug("Estableciendo conexión con la base de datos...")
conn = pyodbc.connect(db_connection.build_connection(expected_connection), autocommit=True)
cursor = conn.cursor()

logging.debug("Obteniendo directorio de backup...")
file_manager = FileManagerImpl()
absolute_backup_path = file_manager.get_absolute_path_backup(expected_connection.database, expected_connection.get_db_type(int(expected_connection.typehost)))

logging.debug("Ejecutando query a la base de datos...")
logging.info("Script:" + db_connection.build_query_backup(expected_connection.database, absolute_backup_path))
cursor.execute(db_connection.build_query_backup(expected_connection.database, absolute_backup_path))

print("BackUp finalizado. Enter para continuar")
input()

google_drive_manager = GoogleDriveImpl()
# file size > 5000 KB carga reanudable. file size < 5000 KB carga simple
if file_manager.get_backup_size(absolute_backup_path) > 5000:
    google_drive_manager.upload_resumable_file(absolute_backup_path)
else:
    google_drive_manager.upload_simple_file(absolute_backup_path)