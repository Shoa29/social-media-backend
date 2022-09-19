from flask_restx import Model, fields

UserPayload = Model('UserPayload', {
    'username': fields.String(required=True)
})

FailResponse= Model('FailResponse', {
    'status': fields.String(required=True, description= 'Possible values: failure, success'),
    'reason': fields.String(required=True)
})
SuccessResponse= Model('SuccessResponse', {
    'status': fields.String(required=True, description= 'Possible values: failure, success')
})