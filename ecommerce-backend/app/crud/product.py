# crud/product.py
from app.database import db, to_dict
from app.models.product import ProductInDB
from bson.objectid import ObjectId
from datetime import datetime

async def create_product(product: ProductInDB) -> dict:
    product.created_at = product.updated_at = datetime.utcnow().isoformat()
    result = await db.products.insert_one(product.dict(exclude={"id"}))
    product.id = str(result.inserted_id)
    return product.dict()

async def get_product_by_id(product_id: str):
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    return to_dict(product) if product else None

async def get_all_products():
    products = await db.products.find().to_list(100)
    return [to_dict(product) for product in products]

async def update_product(product_id: str, updated_data: dict):
    updated_data["updated_at"] = datetime.utcnow().isoformat()
    await db.products.update_one({"_id": ObjectId(product_id)}, {"$set": updated_data})
    return await get_product_by_id(product_id)

async def delete_product(product_id: str):
    result = await db.products.delete_one({"_id": ObjectId(product_id)})
    return result.deleted_count == 1
