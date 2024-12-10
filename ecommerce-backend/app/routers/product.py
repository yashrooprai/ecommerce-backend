from fastapi import APIRouter, HTTPException, Depends
from app.models.product import Product, ProductInDB
from app.crud.product import create_product, get_product_by_id, get_all_products, update_product, delete_product
from app.utils.security import get_current_user

router = APIRouter()

# Create Product - Requires the user to be authenticated
@router.post("/products/addProduct", response_model=ProductInDB)
async def add_product(product: Product, current_user: dict = Depends(get_current_user)):
    print(product)
    if not current_user:
        raise HTTPException(status_code=401, detail="You need to sign in first")
    return await create_product(ProductInDB(**product.dict()))

# List All Products - No authentication needed
@router.get("/products", response_model=list[ProductInDB])
async def list_products():
    return await get_all_products()

# Get a Specific Product - No authentication needed
@router.get("/products/getProduct/{product_id}", response_model=ProductInDB)
async def get_product(product_id: str):
    product = await get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Edit Product - Requires the user to be authenticated
@router.put("/products/editProduct/{product_id}", response_model=ProductInDB)
async def edit_product(product_id: str, product: Product, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="You need to sign in first")
    updated_product = await update_product(product_id, product.dict(exclude={"id"}))
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

# Delete Product - Requires the user to be authenticated
@router.delete("/products/delProduct/{product_id}")
async def remove_product(product_id: str, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="You need to sign in first")
    success = await delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"msg": "Product deleted successfully"}
