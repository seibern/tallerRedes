#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request
import subprocess

app = Flask(__name__)

@app.route('/')
def saludo():
	return "hola mundo"

#a--Ver la lista de maquinas virtuales en el host
@app.route('/todo/api/v1.0/vms')
def listaVms():
  output = subprocess.check_output(['vboxmanage', 'list' , 'vms'])
  return jsonify({'VM':output})

#b--Ver la lista de maquinas en ejecucion en el host
@app.route('/todo/api/v1.0/runVms')
def vmsRun():
  output = subprocess.check_output(['VBoxManage', 'list', 'runningvms'])
  return jsonify({'VM en ejecucion':output})

#Dada una maquina virtual

#c--ver sus caracteristicas
@app.route('/todo/api/v1.0/info/<string:Vmachine>')
def info(Vmachine):
  output = subprocess.check_output(['VBoxManage', 'showvminfo', Vmachine])
  resultado = output.splitlines()
  return jsonify({'Informacion vm seleccionada':resultado})

#d--Ver la RAM asignada a la maquina virtual
@app.route('/vm/RAM/<string:Vmachine>')
def vmsRam(Vmachine):
  output = subprocess.check_output('vboxmanage showvminfo %s | grep "Memory"'% (Vmachine), shell=True)
  return jsonify({'RAM':output})

#e--Ver el numero de procesadores asignados a la maquina virtual
@app.route('/vm/CPUs/<string:Vmachine>')
def vmsCPU(Vmachine):
  output = subprocess.check_output('vboxmanage showvminfo %s | grep "CPU"'% (Vmachine), shell=True)
  return jsonify({'procesador':output})

#f--Brindar el numero de tarjetas de red conectadas a una maquina virtual
@app.route('/vm/NIC/<string:Vmachine>')
def vmsTarjeta(Vmachine):
  output = subprocess.check_output('vboxmanage showvminfo %s | grep "NIC"'% (Vmachine), shell=True)
  resultado = output.splitlines()
  return jsonify({'NIC':resultado})


#g--Modificar el numero de CPUs
@app.route('/modfNumCpus/<string:vmsName>/<string:numCpus>', methods=['GET'])
def set_numCpus(vmsName, numCpus):
  subprocess.check_output(['VBoxManage', 'modifyvm', vmsName,'--cpus',numCpus])
  return "Se le ha asignado "+numCpus+" Cpus a "+vmsName+"\n"

#h--Modificar la RAM asignada a la maquina virtual
@app.route('/modfRAM/<string:vmsName>/<string:newRAM>', methods=['GET'])
def set_RAM(vmsName,newRAM):
  nuevaRam = subprocess.check_output(['VBoxManage', 'modifyvm', vmsName, '--memory', newRAM])
  return "se le a asignado " +newRAM+" de RAM a "+vmsName+"\n"  

#i--Modificar la cantidad de porcentaje del procesador que se le asigna a una maquina virtual
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