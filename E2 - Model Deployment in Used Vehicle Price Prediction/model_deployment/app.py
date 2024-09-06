
import os
from flask import Flask
from flask_restx import Api, Resource, fields
import Model_Dev

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='Predecir el Precio de Coches API - POST',
    description='API para predecir el precio de coches')

ns = api.namespace('predict', description='Precio regresión')

# Definir el modelo del cuerpo de la solicitud
input_model = api.model('InputModel', {
    'Mileage': fields.Float(required=True, description='Millas del auto'),
    'Year': fields.Integer(required=True, description='Año del auto'),
    'State': fields.String(required=True, description='Estado donde esta registrado el auto'),
    'Model': fields.String(required=True, description='Modelo del auto'),
    'Make': fields.String(required=True, description='Marca del auto')
})

resource_fields = api.model('Resource', {
    'predicted_price': fields.Float,
    'predicted_price_std': fields.Float,
})

@ns.route('/')
class PredictPrice(Resource):
    @api.expect(parser)
    @api.marshal_with(resource_fields)
    def get(self):
        # Obtener los parámetros de la URL
        args = parser.parse_args()
        mileage = args['Mileage']
        year = args['Year']
        state = args['State']
        model_name = args['Model']
        make = args['Make']

        # Realizar la predicción
        predicted_price, predicted_price_std = Model_Dev.predict_price(
            mileage=mileage, 
            year=year, 
            state=state, 
            model=model_name,  # Usar model_name en lugar de model
            make=make
        )

        return {
            "predicted_price": predicted_price,
            'predicted_price_std': predicted_price_std
        }, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
