import mysql.connector
from flask import Flask, jsonify, request


def conectar():
    # mis credenciales
    conexion = mysql.connector.connect(
        
        host="", user="", password=""  # mi usuario
    )
    return conexion

def conectarbd():
    # mis credenciales
    conexion = mysql.connector.connect(
       
        host=".mysql.pythonanywhere-services.com", user="", password="",
        database="$",  # nombre de la base de datos
    )
    return conexion

def desconectar(conexion):
    # Cerrar la conexión a la base de datos
    if conexion:
        conexion.close()




def agregar_pizza_menu(id,nombre, descripcion, img):
    try: #lo segundo que se ejecuta
        conexion = conectarbd()
        cursor = conexion.cursor()

        #insertar el producto en la tabla productos
        query = "INSERT INTO menu (id,nombre, DESCRPCION, Img) VALUES (%s,%s, %s, %s)"
        datos_producto = (id,nombre, descripcion, img) #'Mouse gamer', 15, 1500
        cursor.execute(query, datos_producto) #ejecutar la query trabajando con los datos de la tupla

        conexion.commit() #guardar los cambios
        cursor.close() #cerrar la conexion
        print("PIZZA-MENU AGREGADA!")
        return "PIZZA-MENU AGREGADA!"

    except mysql.connector.Error as error: #si se produce algun error
        print(f"Error al agregar el producto -> {error}")
        return f"Error al agregar el producto -> {error}"

    finally: #lo primero que se ejecuta
        desconectar(conexion)



def consultarMenu():
    try:
        conexion = conectarbd()
        cursor = conexion.cursor()

        #obtener todos los registros y todos los campos de la tabla productos
        query = "SELECT * FROM menu"
        cursor.execute(query)
        productos = cursor.fetchall() #guardamos el resultado de ejecutar la linea anterior
        cursor.close()
        return productos

    except mysql.connector.Error as error:
        print(f"Error al obtener los menu -> {error}")

    finally:
        desconectar(conexion)


def borrrarMenu(id):
    try:
        conexion = conectarbd()
        cursor = conexion.cursor()
        query = f"DELETE    FROM menu WHERE id={id}"
        cursor.execute(query)
        conexion.commit()
        cursor.close()
        return (f"se procedera a eliminarlo al id :{id}")

    except mysql.connector.Error as error:
        print(f"Error al obtener los menu -> {error}")

    finally:
        desconectar(conexion)


def consultarMenuID(id):
    try:
        conexion = conectarbd()
        cursor = conexion.cursor()

        query = f"SELECT * FROM menu where id={id}"
        cursor.execute(query)
        productos = cursor.fetchall() #guardamos el resultado de ejecutar la linea anterior
        cursor.close()
        return productos

    except mysql.connector.Error as error:
        print(f"Error al obtener los menu -> {error}")

    finally:
        desconectar(conexion)



def modificar_producto(id,nombre,DESCRPCION,Img):

    conexion = conectarbd()
    cursor = conexion.cursor()
    cursor.execute("UPDATE menu SET nombre= %s ,  DESCRPCION= %s  , Img= %s  WHERE id = %s", (nombre,DESCRPCION,Img,id))
    conexion.commit()
    cursor.close()
    return jsonify({"mensaje":"ACTUALIZADO CON EXITO!"})


def consultarImg(id):

    conexion = conectarbd()
    cursor = conexion.cursor()
    query = f"SELECT Img FROM menu where id={id}"
    cursor.execute(query)
    img = cursor.fetchall() #guardamos el resultado de ejecutar la linea anterior
    cursor.close()
    return img















# if __name__ == "__main__":





