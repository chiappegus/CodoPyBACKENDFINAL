import os
from flask import Flask, jsonify, request, render_template, redirect, url_for

# import mysql.connector
from flask_cors import CORS
import db02_probado_ as basedatos
import requests
import random


from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app)

# get -> consultar

# post -> nuevo elemento en el servidor
# delete -> eliminar un elemento
# put -> actualizar completamente un elemento
# patch -> actualizar parcialmente


@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("MenuprincipalAll"))


@app.route("/DELETE/<int:id>", methods=["GET", "DELETE"])
def DELETE(id):
    nombre_viejo = basedatos.consultarImg(id)
    if os.path.join(app.config["UPLOAD_FOLDER"], nombre_viejo[0][0]):

        direccion = os.path.join(app.config["UPLOAD_FOLDER"], nombre_viejo[0][0])

        os.remove(direccion)

    return jsonify(basedatos.borrrarMenu(id))


@app.route("/consultarMenu", methods=["GET"])
def consultarMenu():

    return jsonify(basedatos.consultarMenu())


@app.route("/MenuprincipalAll", methods=["GET"])
def MenuprincipalAll():

    basedatos.consultarMenu()
    return render_template("main/index.html", menus=basedatos.consultarMenu())


basedir = os.path.abspath(os.path.dirname(__file__))

app.config["UPLOAD_FOLDER"] = os.path.join(
    basedir, "static/uploads"
)  # you'll need to create a folder named uploads
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/directorio", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            # flash('No file part')
            return redirect(request.url)
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            # flash('No selected file')
            return redirect(request.url)
        if request.form.get("descripcion") == "":
            # flash('No selected file')
            return redirect(request.url)
        if request.form.get("nombre") == "":
            # flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            nombre = request.form.get("nombre")
            descripcion = request.form.get("descripcion")
            filename = secure_filename(file.filename)
            filename = f"{round(random.random()*10000)}{filename}"
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            basedatos.agregar_pizza_menu(0, nombre, descripcion, filename)
            # return render_template('uploads/index.html',
            # filename=filename,file_url=filename,nombre=nombre)
            return render_template("main/index.html", menus=basedatos.consultarMenu())
    return render_template("uploads/index.html")


@app.route("/directorioPOST", methods=["POST"])
def directorioPOST():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            # flash('No file part')
            return redirect(request.url)
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            # flash('No selected file')
            return redirect(request.url)
        if request.form.get("descripcion") == "":
            # flash('No selected file')
            return redirect(request.url)
        if request.form.get("nombre") == "":
            # flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            nombre = request.form.get("nombre")
            descripcion = request.form.get("descripcion")
            filename = secure_filename(file.filename)
            filename = f"{round(random.random()*10000)}{filename}"
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            return basedatos.agregar_pizza_menu(0, nombre, descripcion, filename)


@app.route("/update/<int:id>", methods=["GET", "POST", "PUT"])
def update_id(id):
    if request.method == "GET":

        # datos=jsonify(basedatos.consultarMenuID(id))
        return render_template(
            "update_id/index.html", datos=basedatos.consultarMenuID(id)
        )

    if request.method == "POST" or request.method == "PUT":

        file = request.files["file"]
        if file.filename == "":

            nombre = request.form.get("nombre")
            descripcion = request.form.get("descripcion")
            id = request.form.get("id")
            file = basedatos.consultarImg(id)
            # basedatos.modificar_producto(id,nombre, descripcion, file)
            #
            basedatos.modificar_producto(id, nombre, descripcion, file[0][0])
            return redirect(url_for("consultarMenu"))

    file = request.files["file"]

    if file.filename == "":

        return redirect(url_for("consultarMenu"))
    if request.form.get("descripcion") == "":

        return redirect(request.url)
    if request.form.get("nombre") == "":
        return redirect(request.url)
    if request.form.get("descripcion") == "":
        return redirect(request.url)

    if file and allowed_file(file.filename):

        nombre = request.form.get("nombre")

        descripcion = request.form.get("descripcion")

        id = request.form.get("id")

        nombre_viejo = basedatos.consultarImg(id)
        if os.path.join(app.config["UPLOAD_FOLDER"], nombre_viejo[0][0]):
            print("hola")
            direccion = os.path.join(app.config["UPLOAD_FOLDER"], nombre_viejo[0][0])
            # Eliminar el archivo
            os.remove(direccion)

        filename = secure_filename(file.filename)
        filename = f"{round(random.random()*10000)}{filename}"

        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        basedatos.modificar_producto(id, nombre, descripcion, filename)
        return redirect(url_for("consultarMenu"))

    return render_template("update_id/index.html")


@app.route("/updatePUT/<int:id>", methods=["GET", "POST", "PUT"])
def updatePUT(id):

    if request.method == "PUT":

        if not request.files:

            nombre_viejo = basedatos.consultarImg(id)

            nombre = request.form.get("nombre")
            descripcion = request.form.get("descripcion")
            # id = request.form.get("id")
            basedatos.modificar_producto(id, nombre, descripcion, nombre_viejo[0][0])
            return jsonify(basedatos.consultarMenuID(id))

        if request.files:
            file = request.files["file"]
            if file and allowed_file(file.filename):
                nombre = request.form.get("nombre")
                descripcion = request.form.get("descripcion")
                nombre_viejo = basedatos.consultarImg(id)
                if os.path.join(app.config["UPLOAD_FOLDER"], nombre_viejo[0][0]):
                    direccion = os.path.join(
                        app.config["UPLOAD_FOLDER"], nombre_viejo[0][0]
                    )
                    os.remove(direccion)
                filename = secure_filename(file.filename)
                filename = f"{round(random.random()*10000)}{filename}"
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                basedatos.modificar_producto(id, nombre, descripcion, filename)
                return jsonify(basedatos.consultarMenuID(id))

            # return redirect(url_for("consultarMenu"))
        # return datos

    if request.method == "GET":
        return render_template(
            "update_id/index.html", datos=basedatos.consultarMenuID(id)
        )

    if request.method == "POST":

        file = request.files["file"]
        if file.filename == "":

            nombre = request.form.get("nombre")
            descripcion = request.form.get("descripcion")
            id = request.form.get("id")
            file = basedatos.consultarImg(id)
            # basedatos.modificar_producto(id,nombre, descripcion, file)
            #
            basedatos.modificar_producto(id, nombre, descripcion, file[0][0])
            return redirect(url_for("consultarMenu"))

        if request.form.get("descripcion") == "":

            return redirect(request.url)
        if request.form.get("nombre") == "":
            return redirect(request.url)

        if file and allowed_file(file.filename):

            nombre = request.form.get("nombre")

            descripcion = request.form.get("descripcion")

            id = request.form.get("id")

            nombre_viejo = basedatos.consultarImg(id)
            if os.path.join(app.config["UPLOAD_FOLDER"], nombre_viejo[0][0]):

                direccion = os.path.join(
                    app.config["UPLOAD_FOLDER"], nombre_viejo[0][0]
                )
                # Eliminar el archivo
                os.remove(direccion)

            filename = secure_filename(file.filename)
            filename = f"{round(random.random()*10000)}{filename}"

            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            basedatos.modificar_producto(id, nombre, descripcion, filename)
            return redirect(url_for("consultarMenu"))


@app.route("/consultaId/<int:id>", methods=["GET"])
def consultaId(id):

    return jsonify(basedatos.consultarMenuID(id))


if __name__ == "__main__":
    app.run(debug=True)
