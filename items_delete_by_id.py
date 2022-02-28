from bottle import delete
import x

##############################
@delete("/items/<item_id>")
@delete("/<language>/items/<item_id>")
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
    counter = db.execute("DELETE FROM items WHERE item_id = ?", (item_id,)).rowcount
    db.commit()
    if not counter : return x._response(204, "")
    return {"info":"ok"}
  except Exception as ex:
    print(ex)
    return x._response(500, x._errors[f"{language}_server_error"])
  finally:
    db.close()






