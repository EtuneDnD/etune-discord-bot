# Instalación de dependencias

``pip install -r requirements.txt``

# Estructura de carpetas
asdasd
## db
Todo lo relacionado con la base de datos, tanto configuración como todas las cadenas de texto literales que representan sentencias SQL.
## logic
Todo lo relacionado a lógica + ejecución de sentencias SQL
## server
Servidor REST creado con FastAPI
## bot 
Bot de discord
## database.db
Es la base de datos SQLite, es importante que esté en la raíz para que el bot de discord y el servidor rest pueden leer y escribir en ella.