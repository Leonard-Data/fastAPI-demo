from fastapi import FastAPI, HTTPException, Path, Query

from .models.category import Category
from .dummy import items
from .models.item import Item

app = FastAPI(
    title="Inventory API demo site",
    description="Inventory API is the first foundation to step into FastAPI usage for further development",
    version="0.1.0",
)


@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"item": items}


@app.get("/items/{item_id}")
def get_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with Id {item_id} doesn't existed."
        )
    return items[item_id]


# Function parameters that are not path parameters can be specified as query parameters
# Ex: /items?count=100
Selection = dict[
    str, str | int | float | Category | None
]  # dictionary containing the user's query arguments


@app.get("/items/")
def get_item_by_parameters(
    name: str | None = None,
    price: float | None = None,
    count: int | None = None,
    category: Category | None = None,
) -> dict[str, Selection | list[Item]]:
    def check_item(item: Item) -> bool:
        return all(
            (
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count == count,
                category is None or item.category is category,
            )
        )

    selection = [item for item in items.values() if check_item(item)]
    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "items": selection,
    }


@app.post("/")
def add_item(item: Item) -> dict[str, Item]:

    if item.id in items:
        HTTPException(status_code=400, detail=f"Item wit {item.id} already exists.")

    items[item.id] = item
    return {"created": item}


@app.put(
    "/items/{item_id}",
    responses={
        404: {"description": "Item not found."},
        400: {"description": "No arguments specified."},
    },
)
def update_item(
    item_id: int,
    name: str | None = None,
    price: float | None = None,
    count: int | None = None,
    response_return: bool = True,
) -> dict[str, str | Item] | dict[str, Item]:

    if item_id not in items:
        HTTPException(status_code=400, detail=f"Item wit {item_id} does not exist.")
    if all(info is None for info in (name, price, count)):
        raise HTTPException(
            status_code=400, detail="No parameters provided for update."
        )

    item = items[item_id]
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if count is not None:
        item.count = count
    if not response_return:
        return {"status": f"Item {item_id} updated complete."}
    else:
        return {"status": f"Item {item_id} updated complete.", "value": item}


# We can place further restrictions on allowed arguments by using the Query and Path class
# In this case we are setting a lower bound for valid values and minimal and maximal len


@app.put("/items/{item_id}/update")
def update_item_v2(
    item_id: int = Path(ge=0),
    name: str | None = Query(default=None, min_length=1, max_length=8),
    price: float | None = Query(default=None, gt=0.0),
    count: int | None = Query(default=None, ge=0.0),
    response_return: bool = True,
) -> dict[str, str | Item] | dict[str, Item]:

    if item_id not in items:
        HTTPException(status_code=400, detail=f"Item wit {item_id} does not exist.")
    if all(info is None for info in (name, price, count)):
        raise HTTPException(
            status_code=400, detail="No parameters provided for update."
        )

    item = items[item_id]
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if count is not None:
        item.count = count
    if not response_return:
        return {"status": f"Item {item_id} updated complete."}
    else:
        return {"status": f"Item {item_id} updated complete.", "value": item}


@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> dict[str, str | Item] | dict[str, Item]:

    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with {item_id=} does not exist."
        )
    item = items.pop(Item)
    return {"status": f"Item {item_id} deleted complete.", "value": item}
