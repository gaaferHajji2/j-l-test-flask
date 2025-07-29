from flask import abort, make_response, jsonify

from flask.views import MethodView

from flask_smorest import Blueprint

from models import StoreModel

from schemas_shape import StoreSchema

store_blueprint = Blueprint("Store", __name__, description = "The Store's Requests")

@store_blueprint.route('/store/<int:store_id>')
class StoreResource(MethodView):
    @store_blueprint.response(status_code=200, schema=StoreSchema)
    def get(self, store_id: int):
        store_obj = StoreModel.get_store_by_id(store_id)
    
        return store_obj

    def delete(self, store_id: int):
        store_data = StoreModel.get_store_by_id(store_id=store_id)

        store_data.delete_store_from_db()

        return {
            "status": True,
            "msg": "Store Data Deleted Succeessfully",
        }

@store_blueprint.route('/store')
class StoreListResource(MethodView):

    @store_blueprint.response(status_code=200, schema=StoreSchema(many=True))
    def get(self):
        return StoreModel.get_all_stores_from_db()

    @store_blueprint.arguments(schema=StoreSchema)
    @store_blueprint.response(status_code=201, schema=StoreSchema)
    def post(self, payload):        
        store_data = StoreModel(**payload)

        t1 = StoreModel.get_store_by_name(store_data.name)

        print(t1)

        if t1:
            abort(
                make_response(
                    jsonify({"message": "Duplicate store name!"}),
            400  # HTTP status code
        ))
        
        store_data.add_store_data_to_db()

        return store_data