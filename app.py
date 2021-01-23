from flask import  Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.debug = True
Bootstrap(app)

#configuracion para conexion con postgress
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:12345@localhost:5432/escolares'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://peounwgkfretfn:925178ef18666e1f4b0ca9221a3c76e083ace5ec9cf2a8e5aa8aef6b1eb2673a@ec2-54-144-45-5.compute-1.amazonaws.com:5432/dbek9bb3cu83a1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Modelo de datos
class Alumnos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    apellido = db.Column(db.String(100))

lista = ["Nosotros", "Contacto", "Preguntas Frecuentes"]

@app.route('/', methods=['GET', 'POST'])
def index():
    print("index")
    if request.method == "POST":
        print("request")
        campo_nombre = request.form['nombre']
        campo_apellido = request.form['apellido']
        alumno = Alumnos(nombre=campo_nombre, apellido=campo_apellido)
        db.session.add(alumno)
        db.session.commit()
        mensaje = "Alumno Registrado"
        return render_template("index.html", mensaje=mensaje)
    return render_template("index.html", variable=lista)
        #return redirect('/acerca')

@app.route('/acerca')
def acerca():
    consulta = Alumnos.query.all()
    print(consulta)
    return render_template("acerca.html", variable=consulta)

@app.route('/editar/<id>')
def editar(id):
    r=Alumnos.query.filter_by(id=int(id)).first()
    return render_template("editar.html", alumno=r)

@app.route('/actualizar', methods=['GET', 'POST'])
def actualizar():
    if request.method == 'POST':
        qry = Alumnos.query.get(request.form['id'])
        qry.nombre = request.form['nombreE']
        qry.apellido = request.form['apellidoE']
        db.session.commit()
        return redirect(url_for('acerca'))

@app.route('/eliminar/<id>')
def eliminar(id):
    q = Alumnos.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('acerca'))

if __name__ == "__main__":
    #db.create_all()
    app.run(debug=True)
