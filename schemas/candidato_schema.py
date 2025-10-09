from marshmallow import Schema, fields, validate

class CandidatoSchema(Schema):
    id = fields.Int(required=True)
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Str(required=True, validate=validate.Length(min=5, max=120))
    telefone = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    tipo = fields.Str(required=True, validate=validate.OneOf(["GESTOR","RH"]))