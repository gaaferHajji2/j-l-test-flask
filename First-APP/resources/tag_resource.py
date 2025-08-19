from flask import abort, make_response, jsonify

from flask.views import MethodView

from flask_smorest import Blueprint

from models import TagModel, StoreModel, ItemModel

from schemas_shape import TagSchema, TagsAndItemsSchema

from db import db

tag_blp = Blueprint("Tag", __name__, description="The Tag's Requests")


@tag_blp.route("/store/<int:store_id>/tag")
class TagsInStoreResource(MethodView):

    @tag_blp.response(200, schema=TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.get_store_by_id(store_id=store_id)

        # print(f"The Tags is: {store.tags}")

        return store.tags.all()

    @tag_blp.arguments(TagSchema)
    @tag_blp.response(201, schema=TagSchema)
    def post(self, tag_data, store_id):
        store = StoreModel.get_store_by_id(store_id=store_id)

        if TagModel.get_tag_by_name_and_store_if(tag_data["name"], store_id):
            # abort(401, { "message": "Duplicate Store id with Tag Name"})
            abort(
                make_response(
                    jsonify({"message": "Duplicate Store id with Tag Name"}), 401
                ),
            )

        if TagModel.get_tag_by_name(tag_data["name"]):
            # abort({"message": "Duplicate Tag Name: {tag_data.name}"})
            abort(
                make_response({"message": "Duplicate Tag Name: {tag_data.name}"}, 401),
            )

        tag_model_data = TagModel(**tag_data, store_id=store_id)  # type: ignore

        tag_model_data.save_tag_to_db()

        return tag_model_data


@tag_blp.route("/tag/<int:tag_id>")
class TagResource(MethodView):

    @tag_blp.response(200, TagSchema)
    def get(self, tag_id: int):
        tag_model_data = TagModel.get_tag_by_id(id=tag_id)

        return tag_model_data

    @tag_blp.response(
        202,
        description="Deleting Tag with No Item",
    )
    @tag_blp.alt_response(404, description="No Tag Found For This ID")
    @tag_blp.alt_response(
        400, description="Tag has at least one item, so we can't delete it"
    )
    def delete(self, tag_id: int):
        tag = TagModel.get_tag_by_id(id=tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()

            return {"message": "Successfully Deleting Tag"}, 202

        else:
            return {
                "message": "Can't Delete Tag With Items",
            }, 400


@tag_blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):

    @tag_blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.get_item_by_id(item_id=item_id)
        tag = TagModel.get_tag_by_id(id=tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except Exception as e:
            # abort(500, {"message": "Error during link item with tag"})
            abort(
                make_response({"message": "Error during link item with tag"}, 500),
            )

        return tag

    @tag_blp.response(201, TagsAndItemsSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.get_item_by_id(item_id=item_id)
        tag = TagModel.get_tag_by_id(id=tag_id)

        if item.store.id != tag.store.id:
            abort(
                make_response(
                    {
                        "message": "Make sure item and tag belong to the same store before linking.",
                    },
                    400,
                )
            )

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except Exception as e:
            abort(
                make_response({"message": "Error during delete item with tag"}, 500),
            )

        return {
            "message": "Deleting OK For Item And Tag",
            "item": item,
            "tag": tag,
        }
