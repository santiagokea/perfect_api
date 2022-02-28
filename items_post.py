from bottle import post, request
import x
import uuid
import time
from datetime import datetime

##############################
@post("/items")
@post("/<language>/items")
def _(language = "en"):

  # Validate that the user sends JSON
  try:
    request.json.keys()
  except Exception as ex:
    print(ex)
    return x._response(500, x._errors[f"{language}_json_error"])

  try:
    # Maybe the user enters a language that is not supported, then default to english
    # Use any key to see if the language is in the errors dictionary
    if f"{language}_server_error" not in x._errors : language = "en"
    item_text, error = x._is_item_name(request.json.get("item_name"), language)
    if error : return x._response(400, error)
    item_price, error = x._is_item_price(request.json.get("item_price"), language)
    if error : return x._response(400, error)    
    item_id = str(uuid.uuid4())
    item_created_at = str(int(time.time()))
    now = datetime.now()
    item_created_at_date = now.strftime("%Y-%B-%d-%A %H:%M:%S")
    item_updated_at = ""
    item_updated_at_date = ""
    item = {
      "item_id":item_id,
      "item_name":item_text,
      "item_price":item_price,
      "item_created_at":item_created_at,
      "item_created_at_date":item_created_at_date,
      "item_updated_at":item_updated_at,
      "item_updated_at_date":item_updated_at_date
    }
  except Exception as ex:
    print(ex)
    return x._response(500, x._errors[f"{language}_server_error"])

  try:    
    db = x._db_connect("database.sqlite")
    db.execute("""INSERT INTO items 
                VALUES(:item_id, :item_name, :item_price, :item_created_at, 
                :item_created_at_date, :item_updated_at, :item_updated_at_date)""", item)
    db.commit()
    return item
  except Exception as ex:
    print(ex)
    return x._response(500, x._errors[f"{language}_server_error"])
  finally:
    db.close()