from app import db

class Cuenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(60))
    correo = db.Column(db.String(100))
    clave = db.Column(db.String(250))
    estado = db.Column(db.Boolean, default=True)
    # Relación uno a muchos con Censo_Persona
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id'), nullable=False, unique=True)
    persona = db.relationship('Persona', backref=db.backref('cuenta', uselist=False))

    def getPerson(self, id_p):
        print("Recibir: ", id_p)
        from models.persona import Persona
        return Persona.query.filter_by(id=id_p).first()
