from bottle import default_app, delete, error, get, request, response, run


##############################
# GET
import items_get_by_id
import items_get_all

# POST
##############################
import items_post

# PUT
##############################
import items_put_by_id

# DELETE
##############################
import items_delete_by_id








##############################
##############################
##############################








##############################
try:
  import production
  application = default_app()
except Exception as ex:
  run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")




