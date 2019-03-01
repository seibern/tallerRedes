#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request
import subprocess

app = Flask(__name__)

@app.route('/')
def saludo():
	return "hola mundo"

@app.route('/todo/api/v1.0/vms')
def listaVms():
  output = subprocess.check_output(['vboxmanage', 'list' , 'vms'])
  return jsonify({'VM':output})

@app.route('/todo/api/v1.0/runVms')
def vmsRun():
  output = subprocess.check_output(['VBoxManage', 'list', 'runningvms'])
  return jsonify({'VM en ejecucion':output})

@app.route('/todo/api/v1.0/info/<string:Vmachine>')
def info(Vmachine):
  output = subprocess.check_output(['VBoxManage', 'showvminfo', Vmachine])
  resultado = output.splitlines()
  return jsonify({'Informacion vm seleccionada':resultado})

@app.route('/todo/api/v1.0/info/<string:Vmachine>')

if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)