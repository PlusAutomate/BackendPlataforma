from marshmallow import Schema, fields, validate

class VagaSchema(Schema):
    id = fields.Int(required=True)
    titulo = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    descricao = fields.Str(required=True, validate=validate.Length(min=5, max=255))
    status = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    data_criacao = fields.DateTime(required=True)