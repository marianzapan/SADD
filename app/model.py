import logging

#Conexión a BD
from flask_pymongo import MongoClient
client = MongoClient('localhost')

import app.static.humongolus as orm
import app.static.humongolus.field as field
logger = logging.getLogger("humongolus")
orm.settings(logger=logger, db_connection=client)

class Usuarios(orm.Document):
  _db = "sadd_db"
  _collection = "usuarios"
  user = field.Char()
  asignacion = field.Char()
  password = field.Char()
  roles = field.Char()

class FP(orm.Document):
  _db = "sadd_db"
  _collection = "fp"
  num_factura = field.Char()
  fecha_factura = field.Char()
  num_registro = field.Char()
  num_pedimento = field.Char()
  fecha_venc = field.Char()
  xml = field.File(filename="xml", metadata="text/plain", database=MongoClient().sadd_db)
  pdf = field.File(filename="pdf", metadata="application/pdf", database=MongoClient().sadd_db)

class FC(orm.Document):
  _db = "sadd_db"
  _collection = "fc"
  num_factura = field.Char()
  fecha_factura = field.Char()
  num_registro = field.Char()
  num_pedimento = field.Char()
  xml = field.File(filename="xml", metadata="text/plain", database=MongoClient().sadd_db)
  pdf = field.File(filename="pdf", metadata="application/pdf", database=MongoClient().sadd_db)

class Pedimentos(orm.Document):
  _db = "sadd_db"
  _collection = "pedimentos"
  num_pedimento = field.Char()
  fecha_pedimento = field.Char()
  fecha_venc = field.Char()
  material = field.Char()
  aduana = field.Char()
  exportador = field.Char()
  doc = field.File(filename="doc", metadata="", database=MongoClient().sadd_db)

class PL(orm.Document):
  _db = "sadd_db"
  _collection = "pl"
  num_ref = field.Char()
  num_registro = field.Char()
  fecha_recibido = field.Char()
  fecha_enviado = field.Char()
  img = field.File(filename="img", metadata="", database=MongoClient().sadd_db)
  doc = field.File(filename="doc", metadata="", database=MongoClient().sadd_db)

class Archivos(orm.Document):
  _db = "sadd_db"
  _collection = "archivos"
  num_ref = field.Char()
  fecha = field.Char()
  desc = field.Char()
  doc = field.File(filename="doc", metadata="", database=MongoClient().sadd_db)

class Catalogo(orm.Document):
  _db = "sadd_db"
  _collection = "catalogo"
  tipo = field.Char()
  num_registro = field.Char()
  nom = field.Char()
  dir = field.Char()
  tel = field.Phone()
  rfc = field.Char()
  correo = field.Email()