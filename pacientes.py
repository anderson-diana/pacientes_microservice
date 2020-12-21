from datetime import datetime
from flask import jsonify, make_response, abort

from pymongo import MongoClient

##client = MongoClient("mongodb://localhost:27017/") # Local
#db = client.pacientes


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
    
PACIENTES = {
    "001": {
        "idpaciente": "001",
        "lname": "Jose",
        "fname": "da Silva",
        "dnasc": "03/12/2000",
        "convenio": "Itau",
        "ncart"   : "12121313131",
        "timestamp": get_timestamp(),
        
    },
      "002": {
        "idpaciente": "002",
        "lname": "Jose",
        "fname": "da Silva",
        "dnasc": "03/12/2000",
        "convenio": "Itau",
        "ncart"   : "121213131666",
        "timestamp": get_timestamp(),
    },
}

#def get_dict_from_mongodb():
    #itens_db = db.pacientes.find()
    #PACIENTES = {}
    #for i in itens_db:
     #       i.pop('_id') # retira id: criado automaticamente 
     #       item = dict(i)
    #        PACIENTES[item[i]] = (i)
    #return PACIENTES




def read_all():
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
  
    #PACIENTES = get_dict_from_mongodb()
    
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
        #db.pacientes.insert_one(item)
        PACIENTES[idpac] = item
        return make_response(
            "{lname} criado com sucesso".format(lname=lname), 201
        )
    else:
        abort(
            406,
            "Paciente com o numero {idpac} ja existe".format(idpac=idpac),
        )
        
        
def read_one(idpaciente):
    #PACIENTES = get_dict_from_mongodb()
    if idpaciente in PACIENTES:
        pacient = PACIENTES.get(idpaciente)
    else:
        abort(
            404, "paciente nao encontrado {idpaciente} nao encontrada".format(idpaciente=idpaciente)
        )
    return pacient
    
    
def delete(idpaciente):
    #PACIENTES = get_dict_from_mongodb()
#    query = { "idpac": idpac }
    if idpaciente in PACIENTES:
        #db.pacientes.delete_one(query)
        del PACIENTES[idpaciente]
        return make_response(
            "{idpaciente} deletado com sucesso".format(idpaciente=idpaciente), 200
        )
    else:
        abort(
            404, "O paciente {idpaciente} nao encontrado".format(idpaciente=idpaciente)
        )

def update(idpaciente, paciente) :
    if idpaciente in PACIENTES:
        PACIENTES[idpaciente]["idpaciente"] = consulta.get("idpaciente")
    
        PACIENTES[idpaciente]["timestamp"] = get_timestamp()
        return PACIENTES[idpaciente]
    else:
        abort(
            404, "A consulta com o identificador {idpaciente} nao foi encontrada".format(idpaciente=idpaciente)
        )    