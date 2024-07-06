si estas en linux o wsl debes instalar

    sudo apt install -y python3-venv

Poner cada proyecto en su propio ambiente, entrar en cada carpeta.

    python3 -m venv env

    o 

    python -m venv env


Activar el ambiente

    source env/bin/activate
    o:
    source env/Scripts/activate

verifica lo que tengas instalado .

pip freeze 
pasa lo instalado a requeriments.txt

pip freeze >  requeriments.txt
pip freeze >  requeriments_python3_12.txt


pip install mysql-connector-python
pip install Flask
pip install jsonify
pip install request
pip install flask_cors


from flask import Flask, jsonify , request 
import mysql.connector
from flask_cors import CORS 
para instalar :

pip install -r requeriments.txt

verificamos en donde esta instalado en este caso con
which pip 
which python 
which pip3
which python3


instalar dependencia de VSCODE:
vscode-drawio


API :

post : nueva pizza menú :

 chiappegus.pythonanywhere.com/directorioPOST
    datos : 
        nombre text
        descripcion text
        file :img.jpg


DELETE : BORRA pizza menú :

 chiappegus.pythonanywhere.com/DELETE/id

GET :

chiappegus.pythonanywhere.com/consultarMenu

chiappegus.pythonanywhere.com/consultaId/45


PUT

chiappegus.pythonanywhere.com/updatePUT/45

    
datos : 
        nombre text
        descripcion text
        file :img.jpg
o 
        nombre text
        descripcion text





