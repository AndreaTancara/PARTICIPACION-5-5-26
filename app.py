from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CONFIGURACIÓN
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ======================================
# TABLA INTERMEDIA (N-M)
# ======================================

libro_genero = db.Table(
    'libro_genero',

    db.Column(
        'libro_id',
        db.Integer,
        db.ForeignKey('libro.id'),
        primary_key=True
    ),

    db.Column(
        'genero_id',
        db.Integer,
        db.ForeignKey('genero.id'),
        primary_key=True
    )
)

# ======================================
# MODELO AUTOR
# ======================================

class Autor(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)

    nacionalidad = db.Column(db.String(100), nullable=False)

    # RELACIÓN 1-N
    libros = db.relationship(
        'Libro',
        backref='autor',
        cascade="all, delete",
        lazy=True
    )

    def __repr__(self):
        return f"<Autor {self.nombre}>"

# ======================================
# MODELO LIBRO
# ======================================

class Libro(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(150), nullable=False)

    anio = db.Column(db.Integer, nullable=False)

    # FK AUTOR
    autor_id = db.Column(
        db.Integer,
        db.ForeignKey('autor.id'),
        nullable=False
    )

    # RELACIÓN N-M
    generos = db.relationship(
        'Genero',
        secondary=libro_genero,
        backref=db.backref('libros', lazy=True)
    )

    def __repr__(self):
        return f"<Libro {self.titulo}>"

# ======================================
# MODELO GENERO
# ======================================

class Genero(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Genero {self.nombre}>"
    
# ======================================
# CREAR BASE DE DATOS
# ======================================

def init_db():

    with app.app_context():

        db.create_all()

        print("Base de datos creada correctamente")

# ======================================
# INSERTAR DATOS
# ======================================

def insertar_datos():

    with app.app_context():

        # EVITAR DUPLICADOS
        if Autor.query.count() > 0:
            print("Ya existen datos")
            return

        # =========================
        # AUTORES
        # =========================

        autor1 = Autor(
            nombre="Gabriel García Márquez",
            nacionalidad="Colombiano"
        )

        autor2 = Autor(
            nombre="Isaac Asimov",
            nacionalidad="Ruso-Americano"
        )

        autor3 = Autor(
            nombre="Mario Vargas Llosa",
            nacionalidad="Peruano"
        )

        db.session.add_all([autor1, autor2, autor3])

        # =========================
        # GÉNEROS
        # =========================

        genero1 = Genero(nombre="Ficción")
        genero2 = Genero(nombre="Ciencia")
        genero3 = Genero(nombre="Historia")
        genero4 = Genero(nombre="Tecnología")

        db.session.add_all([
            genero1,
            genero2,
            genero3,
            genero4
        ])

        # =========================
        # LIBROS
        # =========================

        libro1 = Libro(
            titulo="Cien Años de Soledad",
            anio=1967,
            autor=autor1
        )

        libro2 = Libro(
            titulo="Fundación",
            anio=1951,
            autor=autor2
        )

        libro3 = Libro(
            titulo="Yo Robot",
            anio=1950,
            autor=autor2
        )

        libro4 = Libro(
            titulo="La Ciudad y los Perros",
            anio=1963,
            autor=autor3
        )

        libro5 = Libro(
            titulo="El Sueño del Celta",
            anio=2010,
            autor=autor3
        )

        # =========================
        # ASOCIAR GÉNEROS
        # =========================

        libro1.generos.append(genero1)

        libro2.generos.extend([
            genero1,
            genero2
        ])

        libro3.generos.extend([
            genero2,
            genero4
        ])

        libro4.generos.extend([
            genero1,
            genero3
        ])

        libro5.generos.append(genero3)

        # =========================
        # GUARDAR
        # =========================

        db.session.add_all([
            libro1,
            libro2,
            libro3,
            libro4,
            libro5
        ])

        db.session.commit()

        print("Datos insertados correctamente")

# ======================================
# CONSULTAR DATOS
# ======================================

def consultar_datos():

    with app.app_context():

        print("\n========== AUTORES Y SUS LIBROS ==========\n")

        autores = Autor.query.all()

        for autor in autores:

            print(f"AUTOR: {autor.nombre}")
            print(f"NACIONALIDAD: {autor.nacionalidad}")

            for libro in autor.libros:
                print(f"   📘 {libro.titulo} ({libro.anio})")

            print("-----------------------------------")

        print("\n========== GÉNEROS Y SUS LIBROS ==========\n")

        generos = Genero.query.all()

        for genero in generos:

            print(f"GÉNERO: {genero.nombre}")

            for libro in genero.libros:
                print(f"   📚 {libro.titulo}")

            print("-----------------------------------")

# ======================================
# ACTUALIZAR DATOS
# ======================================

def actualizar_datos():

    with app.app_context():

        print("\n========== ACTUALIZANDO LIBRO ==========\n")

        libro = Libro.query.filter_by(
            titulo="Fundación"
        ).first()

        if libro:

            print(f"Título anterior: {libro.titulo}")

            libro.titulo = "Fundación - Edición Especial"

            db.session.commit()

            print(f"Nuevo título: {libro.titulo}")

        else:
            print("Libro no encontrado")

# ======================================
# ELIMINAR DATOS
# ======================================

def eliminar_datos():

    with app.app_context():

        print("\n========== ELIMINANDO AUTOR ==========\n")

        autor = Autor.query.filter_by(
            nombre="Isaac Asimov"
        ).first()

        if autor:

            print(f"Autor eliminado: {autor.nombre}")

            db.session.delete(autor)

            db.session.commit()

            print("Los libros asociados también fueron eliminados")

        else:
            print("Autor no encontrado")


if __name__ == "__main__":

    init_db()

    insertar_datos()

    consultar_datos()

    actualizar_datos()

    #eliminar_datos()

    consultar_datos()