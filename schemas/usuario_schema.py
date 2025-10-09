from marshmallow import Schema, fields, validate

class UsuarioSchema(Schema):
    id = fields.Int(required=True)
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Str(required=True, validate=validate.Length(min=5, max=120))
    senha = fields.Str(required=True, validate=validate.Length(min=1, max=45))
    tipo = fields.Str(required=True, validate=validate.OneOf(["GESTOR","RH"]))