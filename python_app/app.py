from flask import Flask, jsonify, render_template, request, url_for, flash, redirect
import mysql.connector
from mysql.connector import errorcode
import logging

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = 'hola'

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/")
def hello():
    try:
        print("Connecting to database...")
        connection = mysql.connector.connect(
            host='db',
            user='user',
            password='user_password',
            database='my_database'
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL server version ", db_info)
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            return f"Connected to MySQL server version {db_info}. You're connected to database: {record[0]}"

    except mysql.connector.Error as err:
        print("Error: ", err)
        return f"Error: {err}"

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            return "MySQL connection is closed"

@app.route('/api/base_datos')
def bd():
    mydb = mysql.connector.connect(
            host='db',
            user='user',
            password='user_password',
            database='my_database'
    )
    TABLES = {}
    TABLES['cliente'] = (
            "CREATE TABLE `cliente` ("
            "  `id_cliente` int(11) NOT NULL AUTO_INCREMENT,"
            "  `nombre` varchar(100) NOT NULL,"
            "  `apellido` varchar(100) NOT NULL,"
            "  `celular` varchar(16) NOT NULL,"
            "  `correo` varchar(100) NOT NULL,"
            "  `direccion` varchar(100) NOT NULL,"
            "  `tipo_documento` enum('CC','TI') NOT NULL,"
            "  `no_documento` varchar(16) NOT NULL,"
            "  `fecha_nacimiento` date NOT NULL,"
            "  PRIMARY KEY (`id_cliente`)"
            ") ENGINE=InnoDB")

    TABLES['sucursal'] = (
            "CREATE TABLE `sucursal` ("
            "  `id_sucursal` char(4) NOT NULL,"
            "  `localidad` varchar(40) NOT NULL,"
            "  `direccion` varchar(40) NOT NULL,"
            "  PRIMARY KEY (`id_sucursal`)"
            ") ENGINE=InnoDB")

    cursor = mydb.cursor()
    for table_name in TABLES:
        table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            return("ya existen.")
        else:
            return(err.msg)
    else:
        return("creadas")

    cursor.close()
    cnx.close()

@app.route('/api/consultar')
def consulta():
    mydb = mysql.connector.connect(
            host='db',
            user='user',
            password='user_password',
            database='my_database'
    )
    
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cliente")
    myresult = mycursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in mycursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    mycursor.close()
    return render_template('menu.html', data=insertObject)

    



@app.route('/api/insertar', methods=('GET', 'POST'))
def insertar():
    logging.warning('entro')
    if request.method == 'POST':
        

        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        celular = request.form["celular"]
        direccion = request.form["direccion"]
        correo = request.form["correo"]
        tipo_documento = request.form["tipo_documento"]
        documento = request.form["documento"]
        fecha = '2024-02-06'
        logging.error(nombre)
        logging.error(apellido)
        logging.error(celular)
        logging.error(direccion)
        logging.error(correo)
        logging.error(tipo_documento)
        logging.error(documento)
        logging.error(fecha)
        
        if not nombre:
            flash('Title is required!')
        else:
            mydb = mysql.connector.connect(
                host='db',
                user='user',
                password='user_password',
                database='my_database'
            )
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO `cliente` (`id_cliente`, `nombre`, `apellido`, `celular`, `correo`,`direccion`, `tipo_documento`, `no_documento`, `fecha_nacimiento`)VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)",(nombre, apellido, celular, correo, direccion, tipo_documento, documento, fecha))

            mydb.commit()
            
            return redirect(url_for('consulta'))
    return render_template('menu.html')

@app.route('/api/eliminar/<string:id_cliente>')
def eliminar(id_cliente):
    mydb = mysql.connector.connect(
                host='db',
                user='user',
                password='user_password',
                database='my_database'
    )
    
    mycursor = mydb.cursor()
    sql = "DELETE FROM cliente WHERE `cliente`.`id_cliente`=%s"
    logging.error(id_cliente)
    data = (id_cliente,)
    mycursor.execute(sql, data)
    mydb.commit()
    return redirect(url_for('consulta'))


@app.route('/api/editar/<string:id_cliente>', methods=('GET', 'POST'))
def editar(id_cliente):

    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    celular = request.form["celular"]
    direccion = request.form["direccion"]
    correo = request.form["correo"]
    tipo_documento = request.form["tipo_documento"]
    documento = request.form["documento"]
    fecha = '2024-02-06'
    mydb = mydb = mysql.connector.connect(
                host='db',
                user='user',
                password='user_password',
                database='my_database'
    )
    logging.error(nombre)
    logging.error(apellido)
    logging.error(celular)
    logging.error(direccion)
    logging.error(correo)
    logging.error(tipo_documento)
    logging.error(documento)
    logging.error(fecha)
    
    mycursor = mydb.cursor()
    sql = "UPDATE `cliente` SET `nombre` = %s, `apellido` = %s, `celular` = %s, `correo` = %s, `direccion` = %s, `tipo_documento` = %s, `no_documento` = %s, `fecha_nacimiento` = %s WHERE `cliente`.`id_cliente` = %s"
    logging.error(sql)
    data = (nombre, apellido, celular, correo, direccion, tipo_documento, documento, fecha, id_cliente)
    mycursor.execute(sql, data)
    mydb.commit()
    return redirect(url_for('consulta'))

if __name__ == '__main__':
        print(app.url_map)
        app.run(host="0.0.0.0", port=4000, debug=True)




