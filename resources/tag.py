from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db

from models.store import StoreModel
from models.tags import TagModel
from models.item import ItemModel
from schema import TagSchema, TagAndItemSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("tags", __name__, description="Operations on tags")

@blp.route('/stores/<int:store_id>/tags/')
class TagInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A tag with that name already exists in this store.")
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag

@blp.route('/tag/<int:tag_id>/item/<int:item_id>/')
class LinkTagToItem(MethodView):
    @blp.response(200, TagAndItemSchema)
    def post(self, tag_id, item_id):
        tag = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)
        tag.items.append(item)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag
    
    @blp.response(200, TagAndItemSchema)
    def delete(self, tag_id, item_id):
        tag = TagModel.query.get_or_404(tag_id)
        item = ItemModel.query.get_or_404(item_id)
        tag.items.remove(item)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return {"message": "Item removed from tag.", "tag": tag, "item": item}


@blp.route('/tag/<int:tag_id>/')
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        return TagModel.query.get_or_404(tag_id)
    
    @blp.response(202,
                    description="Deletes a tag if no item is tagged with it.",
                    example={"message": "Tag deleted."})
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(400, description="Tag is assigned to one or more items. Cannot delete.")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(400, message="Tag is assigned to one or more items. Cannot delete.")

        return {"message": "Tag deleted."}