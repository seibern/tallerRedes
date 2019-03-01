#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request
import subprocess

app = Flask(__name__)

@app.route('/')
def saludo():
	return "hola mundo"

#a
@app.route('/todo/api/v1.0/vms')
def listaVms():
  output = subprocess.check_output(['vboxmanage', 'list' , 'vms'])
  return jsonify({'VM':output})
#b
@app.route('/todo/api/v1.0/runVms')
def vmsRun():
  output = subprocess.check_output(['VBoxManage', 'list', 'runningvms'])
  return jsonify({'VM en ejecucion':output})
#c
@app.route('/todo/api/v1.0/info/<string:Vmachine>')
def info(Vmachine):
  output = subprocess.check_output(['VBoxManage', 'showvminfo', Vmachine])
  resultado = output.splitlines()
  return jsonify({'Informacion vm seleccionada':resultado})

#@app.route('/todo/api/v1.0/vm/RAM/<string:Vmachine>')
#def vmsRam(Vmachine):
#  output = subprocess.check_output(['VBoxManage', 'showvminfo', Vmachine], stdout=subprocess.PIPE)

#h
@app.route('/modfNumCpus/<string:vmsName>/<string:numCpus>', methods=['GET'])
def set_numCpus(vmsName, numCpus):
  subprocess.check_output(['VBoxManage', 'modifyvm', vmsName,'--cpus',numCpus])
  return "Se le ha asignado "+numCpus+" Cpus a "+vmsName+"\n"

#i
@app.route('/modfRAM/<string:vmsName>/<string:newRAM>', methods=['GET'])
def set_RAM(vmsName,newRAM):
  nuevaRam = subprocess.check_output(['VBoxManage', 'modifyvm', vmsName, '--memory', newRAM])
  return "se le a asignado " +newRAM+" de RAM a "+vmsName+"\n"  

#j
@app.route('/modfPercent/<string:vmsName>/<int:percent>', methods=['GET'])
def sete_CpuPercent(vmsName,percent):
  if (percent<1 or percent>100):
    return "Valor invalido para el porcentaje"+"\n"

  else:
    prct = str(percent)
    subprocess.check_output(['VBoxManage','modifyvm', vmsName, '--cpuexecutioncap', prct])
    return "Se le ha asignado "+prct+" de porcentaje de cpu a"+vmsName+"\n" 

if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)