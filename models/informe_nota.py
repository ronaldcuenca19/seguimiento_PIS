from app import db

class Informe_Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(60))
    Leccion = db.Column(db.Float)
    Evaluacione = db.Column(db.Float)
    Deber = db.Column(db.Float)
    Practica = db.Column(db.Float)
    id_nota = db.Column(db.Integer, db.ForeignKey('nota.id'), nullable=False, unique=True)
    nota = db.relationship('Nota', backref=db.backref('detalle_notas', uselist=False))

    def serialize(self):
        unidad_data = None
        if self.nota:
            unidad_data = {
                'total': self.nota.nota_total
            }
        
        return  {
            'leccion':self.Leccion,
            'deber': self.Deber,
            'evaluacion': self.Evaluacione,
            'practica': unidad_data,
            'nota': unidad_data,
            'external_id':self.external_id,
        }
    
