from bottle import response
import sqlite3
import re

_errors = {
  "en_server_error":"server error",
  "dk_server_error":"server fejl",
  "en_json_error":"invalid json",
  "dk_json_error":"ugyldigt json",  
}

##############################
def _response(status = 400, error_message = "unknown error"):
  response.status = status
  return {"info":error_message}

##############################
def _is_item_name(text=None, language="en"):
  min, max = 2, 20
  errors = {
    "en":f"item_name {min} to {max} characters. No spaces", 
    "dk":f"item_name {min} til {max} tegn. Uden mellemrum"
  }
  if not text: return None, errors[language]
  if len(text) < min or len(text) > max : return None, errors[language]
  # if " " in text : return None, errors[language]
  text = text.strip().capitalize()
  return text, None

##############################
def _is_item_price(text=None, language="en"):
  errors = {
    "en":f"item_price must be a number with two decimals divided by a comma, cannot start with zero, and must be between double quotes", 
    "dk":f"item_price skal være et tal med to decimaler divideret med et komma, må ikke starte med nul, og skal stå mellem dobbelte anførselstegn"
  }
  if not text : return None, errors[language]
  if not re.match("^[1-9][0-9]*[.][0-9]{2}$", str(text)) : return None, errors[language]
  return text, None

##############################
def _is_uuid4(text=None, language="en"):
  errors = {
    "en":f"item_id must be uuid4", 
    "dk":f"item_id skal være uuid4"
  }
  if not text: return None, errors[language]
  regex_uuid4 = "^[0-9a-f]{8}-[0-9a-f]{4}-[4][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
  if not re.match(regex_uuid4, text) : return None, errors[language]
  return text, None

##############################
def create_json_from_sqlite_result(cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
    d[col[0]] = row[idx]
  return d

##############################
def _db_connect(db_name):
  db = sqlite3.connect(db_name)
  db.row_factory = create_json_from_sqlite_result
  return db

























