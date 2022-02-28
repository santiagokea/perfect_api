from bottle import get, response
import x
import json

##############################
@get("/items")
@get("/<language>/items")
def _(language = "en"):
  try:
    # Maybe the user enters a language that is not supported, then default to english
    # Use any key to see if the language is in the errors dictionary
    if f"{language}_server_error" not in x._errors : language = "en"
  except Exception as ex:
    print(ex)
    return x._response(500, x._errors[f"{language}_server_error"])

  try:
    db = x._db_connect("database.sqlite")
    items = db.execute("SELECT * FROM items").fetchall()
    if not items: return x._response(204, "")
    response.content_type = "application/json"
    return json.dumps(items)
  except Exception as ex:
    print(ex)
    return x._response(500, x._errors[f"{language}_server_error"])
  finally:
    db.close()






