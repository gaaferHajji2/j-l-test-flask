from flask import abort

from flask.views import MethodView

from flask_smorest import Blueprint

from flask_jwt_extended import jwt_required, get_jwt

from models import ItemModel

from schemas_shape import ItemSchema
from schemas_shape import ItemUpdateSchema

item_blueprint = Blueprint("Item", __name__, description= "The Item's Requests")

@item_blueprint.route('/item/<int:item_id>')
class ItemResource(MethodView):
    @item_blueprint.response(status_code=200, schema=ItemSchema)
    def get(self, item_id):
        item_data = ItemModel.get_item_by_id(item_id)
    
        if not item_data:
            abort(404, {"message": f"No Item Found For ID {item_id}"})

        return item_data

    # The Order is Important for decorator.
    @item_blueprint.arguments(schema=ItemUpdateSchema)
    @item_blueprint.response(status_code=200, schema=ItemSchema)
    def put(self, payload, item_id):
        item = ItemModel.get_item_by_id(item_id=item_id)
    
        item.update_item_in_db(**payload)
    
        return item

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()

        if not jwt.get("admin"):
            abort(403, description=f"Only Admins Can Access This Route")

        item_data = ItemModel.get_item_by_id(item_id)

        item_data.delete_item_from_db()

        return {
            "status": True,
            "msg": "Data Deleted Successfully"
        }

@item_blueprint.route('/item')
class ItemListResource(MethodView):

    @item_blueprint.response(status_code=200, 
                    schema=ItemSchema(many=True))
    def get(self):
        return ItemModel.get_all_items_in_db()

    @jwt_required(fresh=True)
    @item_blueprint.arguments(schema=ItemSchema)
    @item_blueprint.response(status_code=201, schema=ItemSchema)
    def  post(self, payload):
        item = ItemModel(**payload)

        # In Real scenario we must check the store id with
        # The Item Name, not just only the item name.
        if ItemModel.get_item_by_name(item.name):
            abort(400, description="Duplicate Item Name")

        item.add_item_data_to_db()

        return item