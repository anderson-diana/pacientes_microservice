from datetime import datetime
from flask import jsonify, make_response, abort

from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/") # Local
db = client.pacientes

def get_dict_from_mongodb():
    itens_db = db.pacientes.find()
    PACIENTES = {}
    for i in itens_db:
            i.pop('_id') # retira id: criado automaticamente 
            item = dict(i)
            PACIENTES[item["idpaciente"]] = (i)
    return PACIENTES



def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def read_all():
    PACIENTES = get_dict_from_mongodb()
    dict_pacientes = [PACIENTES[key] for key in sorted(PACIENTES.keys())]
    pacientes = jsonify(dict_pacientes)
    qtd = len(dict_pacientes)
    content_range = "pacientes 0-"+str(qtd)+"/"+str(qtd)
    # Configura headers
    pacientes.headers['Access-Control-Allow-Origin'] = '*'
    pacientes.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    pacientes.headers['Content-Range'] = content_range
    return pacientes
    
def create(pacient):
    idpac = pacient.get("idpaciente", None)
    lname = pacient.get("lname", None)
    fname = pacient.get("fname", None)
    dnasc = pacient.get("dnasc", None)
    convenio = pacient.get("convenio", None)
    ncart = pacient.get("ncart", None)
  
    PACIENTES = get_dict_from_mongodb()
    
    if idpac not in PACIENTES:
        item = {
            "idpaciente": idpac,
            "lname": lname,
            "fname": fname,
            "dnasc": dnasc,
            "convenio": convenio,
            "ncart": ncart,
            "timestamp": get_timestamp(),
        }
        db.pacientes.insert_one(item)
        return make_response(
            "{lname} criado com sucesso".format(lname=lname), 201
        )
    else:
        abort(
            406,
            "Paciente com o numero {idpac} ja existe".format(idpac=idpac),
        )
        
        
def read_one(idpac):
    PACIENTES = get_dict_from_mongodb()
    if idpac in PACIENTES:
        pacient = PACIENTES.get(idpac)
    else:
        abort(
            404, "paciente nao encontrado {idpac} nao encontrada".format(idpac=idpac)
        )
    return pacient
    
    
def delete(idpac):
    PACIENTES = get_dict_from_mongodb()
    query = { "idpac": idpac }
    if idpac in PACIENTES:
        db.pacientes.delete_one(query)
        return make_response(
            "{idpac} deletado com sucesso".format(idpac=idpac), 200
        )
    else:
        abort(
            404, "O paciente {lname} nao encontrado".format(idpac=idpac)
        )





