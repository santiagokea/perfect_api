from bottle import get
import x

##############################
@get("/items/<item_id>")
@get("/<language>/items/<item_id>")
def _(language = "en", item_id = ""):
  try:
    # Maybe the user enters a language that is not supported, then default to english
    # Use any key to see if the language is in the errors dictionary
    if f"{language}_server_error" not in x._errors : language = "en"
    item_id, error = x._is_uuid4(item_id, language)
    if error : return x._response(400, error)
  except Exception as ex:
    print(ex)
    return x._response(500, x._errors[f"{language}_server_error"])

  try:
    db = x._db_connect("database.sqlite")
    item = db.execute("SELECT * FROM items WHERE item_id = ?", (item_id,)).fetchone()
    if not item: return x._response(204, "")
    return item
  except Exception as ex:
    print(ex)
    return x._response(500, x._errors[f"{language}_server_error"])
  finally:
    db.close()






