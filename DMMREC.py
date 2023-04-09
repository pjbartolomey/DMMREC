#! /usr/bin/python3
#
# License: GNU General Public License (GPL) v.3
# http://www.gnu.org/licenses/gpl.html
# In short: don`t claim you wrote it, leave the copyright intact,
# give it away, modify it to fit your wishes, use it for whatever
# you want, but keep it free and the source code available.
# 
# I make no warranty or responsibility for anything associated with this program.
# Use it at your responsibility and risk.
#

"""
Really worked on 2022 and 2023
@autor: Pedro J. Bartolomey Nadal
"""

# imports:
import csv
import os.path
import serial
import serial.tools.list_ports
import simpleaudio 
import socket
import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QMessageBox
from datetime import datetime
from time import sleep, time
# GUI import:
import DMMREC_ui
from DMMREC_ui import *
# local lib import: 
import libdmmut61b
import lib_ini


# Global variables
archivo_ini = ''
C_Fail = 0
C_Pass = 0
Count = 0
fail = 0
flags_file = []
fraseglobal = ''
logpath = ''
repeatini = 0
sound = 0
step = 0
stop = 0
tablavolts_chk = []
tablavolts_ori = []
test_status = 0
valor_global = 0
verbose = 1


# class for align table
class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.Checkini()
        self.RefreshComPort()
        # Update the status bar
        self.statusBar().showMessage('Ver: 1.0          Count: ' + str(Count) + '     Pass: ' + str(C_Pass) + '     Fail: ' + str(C_Fail))
        self.Buttonrefresh.clicked.connect(self.RefreshComPort)
        self.Button_connect.clicked.connect(self.conectar)
        self.pushButton_start.clicked.connect(self.start)
        self.pushButton_next.clicked.connect(self.next)
        self.pushButton_cc.clicked.connect(self.clearcounters)
        self.cargarmodelos()
        self.comboBoxArt.currentIndexChanged.connect(self.ModelChanged)
        # Align text in table.
        delegate = AlignDelegate(self.tableWidget)
        self.tableWidget.setItemDelegate(delegate)
        # adjust widht of columns in table
        self.tableWidget.setColumnWidth(0,100)
        self.tableWidget.setColumnWidth(1,60)
        self.tableWidget.setColumnWidth(2,60)
        self.tableWidget.setColumnWidth(3,60)
        self.tableWidget.setColumnWidth(4,40)
        self.tableWidget.setColumnWidth(5,50)
        self.tableWidget.setColumnWidth(6,80)
        self.tableWidget.setColumnWidth(7,40)


    # Routine: routine that fills the combobox, exit if no file found.
    def cargarmodelos(self):
        global archivo_ini
        self.printv('Routine cargarmodelos: ' + str(archivo_ini))
        self.comboBoxArt.clear()
        path,message = lib_ini.readini(archivo_ini,'Default','Config_files')
        if (message):
            self.showdialog(str(message))
            exit()
        if (os.path.exists(path)) is False:
            self.showdialog('Cant find ' + str(path) + ', program will close')
            exit()
        dirs = os.listdir( path )
        for filename in sorted(dirs):
            basename, file_extension = os.path.splitext(filename)
            if file_extension.endswith('.ini'):
                self.printv('\t\t' + str(filename))
                self.comboBoxArt.addItem(basename)
        if (self.comboBoxArt.count() >= 1):
            self.ModelChanged()
        else:
            self.showdialog('No config files found, program will close')
            exit()


    # Routine: start button routine, initializes variables, activates the test_status flag and changes the button to stop.
    def start(self):
        global test_status
        global fraseglobal
        global step
        global tablavolts_ori
        global tablavolts_chk 
        self.printv('Routine start: ' + str(tablavolts_ori))
        self.Button_connect.setEnabled(False)
        self.comboBoxArt.setEnabled(False)
        self.spinBoxorden.setEnabled(False)
        self.pushButton_start.setText('S&top')
        self.pushButton_start.clicked.disconnect(self.start)
        self.pushButton_start.clicked.connect(self.stop)
        self.pushButton_next.setEnabled(True)
        tablavolts_chk = tablavolts_ori
        test_status = 1
        fraseglobal = ''
        step = 0
        self.label.setStyleSheet("QLabel { background-color : ; color : ; }")
        self.label.setText('Waiting ' + str(step + 1))


    # Routine: stop button routine, disable the test_status flag and change the button to start.
    def stop(self):
        global test_status
        self.printv('Routine stop')
        self.pushButton_next.setEnabled(False)
        self.pushButton_start.setText('S&tart')
        self.pushButton_start.clicked.disconnect(self.stop)
        self.pushButton_start.clicked.connect(self.start)
        self.Button_connect.setEnabled(True)
        self.comboBoxArt.setEnabled(True)
        self.spinBoxorden.setEnabled(True)
        self.label.setStyleSheet("QLabel { background-color : ; color : ; }")
        self.label.setText('')
        test_status = 0


    # Routine: next button routine, advances the step flag (if it is the last point it calls the record function) and activates the failure flag.
    def next(self):
        global valor_global
        global tablavolts_ori
        global tablavolts_chk
        global step
        global fail
        self.printv('Routine next: ' + str(step))
        tablavolts_tmp = []
        # Go through the list of points to mark fail.
        for indice in range(len(tablavolts_chk)):
            # If the index is equal to the tested point, we copy adding the fail
            if (indice == step):
                tablavolts_tmp.append([tablavolts_chk[indice][0],tablavolts_chk[indice][1],valor_global,tablavolts_chk[indice][3],tablavolts_chk[indice][4],tablavolts_chk[indice][5],tablavolts_chk[indice][6],'0'])
            else:
                tablavolts_tmp.append(tablavolts_chk[indice])
        # Overwrite the table
        tablavolts_chk = tablavolts_tmp
        # Refresh GUI table.
        self.addtotable(tablavolts_chk)
        step = step + 1
        self.label.setStyleSheet("QLabel { background-color : ; color : ; }")
        self.label.setText('Waiting ' + str(step + 1))
        fail = 1
        if (step == len (tablavolts_chk)):
            step = 0        
            self.record()
            tablavolts_chk = tablavolts_ori


    # Routine: clear counters button routine, restart counters.
    def clearcounters(self):
        global Count
        global C_Pass
        global C_Fail
        Count = 0
        C_Pass = 0
        C_Fail = 0
        self.statusBar().showMessage('Ver: 1.0          Count: ' + str(Count) + '     Pass: ' + str(C_Pass) + '     Fail: ' + str(C_Fail))


    # Routine: which receives a list of data and adds the data to the corresponding table.
    def addtotable(self,datos):
        global step
        global test_status
        self.printv('Routine addtotable')
        self.tableWidget.setRowCount(0)
        for row in datos:
            if (len(row) == 8):
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)
                for y in range (0 ,len(row)):
                    self.tableWidget.setItem(rowPosition , y, QtWidgets.QTableWidgetItem(str (row[y])))
                item = self.tableWidget.item(rowPosition , 0)
                if (rowPosition <= step) and (test_status == 1):
                    self.setColortoRow(self.tableWidget,rowPosition,(QtGui.QColor(230, 220, 100,128)))
            else:
                self.showdialog('Warning! Incorrect number of items, program will close')
                exit()


    # Routine: Change row color in table.
    def setColortoRow(self, table, rowIndex, color):
        for index in range(table.columnCount()):
            table.item(rowIndex, index).setBackground(color)


    # Routine: Read from the file loaded in the combobox the image and the data for the table.
    def ModelChanged(self):
        global archivo_ini
        global tablavolts_ori
        global tablavolts_chk 
        global flags_file
        self.printv('Routine ModelChanged')
        # We initialize some global variables
        flags_file = []
        tablavolts_ori = []
        tablavolts_chk = []
        # rebuild the path of the selected model.
        folder,message = lib_ini.readini(archivo_ini,'Default','Config_files')
        if (message):
            self.printv('\t' + str(message) + '\t' + str(folder))
            self.showdialog('Error reading Draw_files value of the ini file, program will close.')
            exit()
        name = folder + '/' + self.comboBoxArt.currentText() + '.ini'   
        archivo_model = os.path.realpath(name)
        self.printv('\t\t' + str(archivo_model)) 
        # through a library we obtain the flags of the multimeter
        flags_file,message = lib_ini.readini_dmmflags(archivo_model)
        self.printv('\t\t' + str(flags_file))
        if (flags_file == 1):
            self.showdialog(str(message))
        else:
            #through a library we obtain the points to test.
            checkdata,message = lib_ini.readini_point(archivo_model)
            self.printv('\t\t' + str(checkdata))
            if (message):
                self.showdialog(str(message))
            else:
                for indice in range(len(checkdata)):
                    Banda = round(float((checkdata[indice][2]/100)*checkdata[indice][3]), 3)
                    Vmax = round(float(checkdata[indice][2] + Banda), 3) 
                    Vmin = round(float(checkdata[indice][2] - Banda), 3) 
                    if (checkdata[indice][4] == 0):
                        rel = ''
                    else:
                        rel = int(checkdata[indice][4])
                    valor = round(float(checkdata[indice][2]),3)
                    porcentaje = round(float(checkdata[indice][3]),3)
                    tablavolts_ori.append([checkdata[indice][1],Vmax,valor,Vmin,rel,porcentaje,'',''])
                # Load the image.
                folder,message = lib_ini.readini(archivo_ini,'Default','Draw_files')
                if (message):
                    self.printv('\t' + str(message) + '\t' + str(folder))
                    self.showdialog('Error reading Draw_files value of the ini file.')
                    folder = ''
                drawname,message = lib_ini.readini(archivo_model,'header','Draw')
                if (message):
                    self.printv('\t' + str(message) + '\t' + str(drawname))
                    self.showdialog('Error reading draw value of the ini file.')
                    drawname = ''
                image =  os.path.realpath(folder + '/' + drawname)
                self.printv('\t\t' + str(image))
                if (os.path.exists(image)) is False:
                    self.showdialog('Cant find ' + str(image) + ', image will not be loaded.')
                pixmap=QtGui.QPixmap(image)
                self.label_im.setPixmap(pixmap)
                self.label_im.resize(pixmap.width(),pixmap.height())
            self.addtotable(tablavolts_ori)
        # Update the status bar
        self.statusBar().showMessage('Ver: 1.0          Count: ' \
        + str(Count) + '     Pass: ' + str(C_Pass) + '     Fail: ' \
        + str(C_Fail) + '               Device config: ' + str(flags_file.get('measure')) \
        + ', ' + str(flags_file.get('acdc')) + ', ' + str(flags_file.get('range'))) 


    # Routine: overwrites the close event to ensure that the port is closed. 
    def closeEvent(self, event):
        global stop
        self.printv('Routine closeEvent')
        stop = 1
        sleep(1)


    # Routine: disconnect button routine, close the serial port and change the button to connect
    def desconectar(self):
        global stop
        self.printv('Routine desconectar')
        self.Button_connect.setEnabled(False)
        self.Button_connect.setText('Disconnecting')
        self.label.setStyleSheet("QLabel { background-color : ; color : ; }")
        self.label.setText('Disconnecting')
        QtWidgets.QApplication.processEvents()
        stop = 1
        sleep(1)
        self.Button_connect.clicked.disconnect(self.desconectar)
        self.Button_connect.clicked.connect(self.conectar)
        self.pushButton_start.setText('S&tart')
        self.comboBoxPort.setEnabled(True)
        self.Buttonrefresh.setEnabled(True)
        self.pushButton_start.setEnabled(False)
        self.label_DMM.setText('----.--- --')
        self.label.setStyleSheet("QLabel { background-color : ; color : ; }")
        self.label.setText('')
        self.Button_connect.setText('C&onnect')
        self.Button_connect.setEnabled(True)


    # Routine: button connect routine, check connection with DMM using lib.
    def conectar(self):
        self.printv('Routine conectar')
        self.Button_connect.setEnabled(False)
        self.comboBoxPort.setEnabled(False)
        self.Buttonrefresh.setEnabled(False)
        self.Button_connect.setText('Search DMM')
        self.label.setStyleSheet("QLabel { background-color : ; color : ; }")
        self.label.setText('Search DMM')
        QtWidgets.QApplication.processEvents()
        result = libdmmut61b.dmmcheck(self.comboBoxPort.currentText())
        # if connection good go to routine conectar2
        if (result == 2):
            self.label.setStyleSheet("QLabel { background-color : ; color : ; }")
            self.label.setText('')
            self.conectar2()
        # if connection bad show message
        elif (result == 1):
            self.showdialog('DMM NOT Found,Check connection')
            self.Button_connect.setText('C&onnect')
            self.label.setStyleSheet("QLabel { background-color : ; color : ; }")
            self.label.setText('')
            self.comboBoxPort.setEnabled(True)
            self.Buttonrefresh.setEnabled(True)
            self.Button_connect.setEnabled(True)
        else:
            self.showdialog("Can't connect Serial!")
            self.Button_connect.setText('C&onnect')            
            self.label.setText('')
            self.comboBoxPort.setEnabled(True)
            self.Buttonrefresh.setEnabled(True)
            self.Button_connect.setEnabled(True)


    # Routine: open the serial port, decode each phrase and depending on the flags act.
    def conectar2(self):
        global stop
        global fraseglobal
        global test_status
        global sound
        global step
        global repeatini
        global tablavolts_ori
        global tablavolts_chk
        global ser
        global valor_global
        self.printv('Routine conectar2')
        repeat = 0
        try:
            ser = serial.Serial(port=self.comboBoxPort.currentText(),baudrate='2400',timeout =None,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,rtscts=False,dsrdtr=True,bytesize=serial.EIGHTBITS)
            ser.close()
            ser.open()
            ser.reset_input_buffer()
            ser.setDTR(1)
            ser.setRTS(0)
            self.Button_connect.setText('D&isconnect')
            self.Button_connect.setEnabled(True)
            self.Button_connect.clicked.disconnect(self.conectar)
            self.Button_connect.clicked.connect(self.desconectar)
            self.pushButton_start.setEnabled(True)
            stop = 0
            self.pushButton_start.setFocus()
            # Do the same while stop flag be 0
            while stop == 0:
                QtWidgets.QApplication.processEvents()
                # Wait imput from serial port
                while (ser.inWaiting()>0):
                    # tiempo_inicial = time()  # Timer for debug
                    try:
                        frase = ser.readline()
                        ser.reset_input_buffer()
                        # if phrase len not 14 bits means wrong data.
                        if (len(frase) == 14):
                            # If phrase is different from the previous one, we reset the counter and decode.
                            if (frase != fraseglobal):
                                self.printv('\t\tfrase: ' + str(frase))
                                repeat = 1
                                flags = libdmmut61b.dmmflags(frase[7:11])
                                valor = libdmmut61b.dmmdecode(frase[0:7])
                                # Send to a routine that represents the Multimeter data in the GUI 
                                self.iconos(flags,valor)
                                fraseglobal = frase
                                valor_global=valor
                            # if phrase is equal to the previous one we increase the counter repeat.                          
                            else:
                                repeat = repeat + 1
                                # self.printv('\t\trepeat: ' + str(repeat))
                            # If the test_status flag is active and have enough repeats, check if the value is within the values.                       
                            if (test_status == 1) and (repeat == repeatini) and (valor != 'OVERFLOW'):
                                if ((valor <= tablavolts_chk[step][1]) and (valor >= tablavolts_chk[step][3])):
                                    self.relative(valor,step)
                                    step = step + 1
                                    self.label.setStyleSheet("QLabel { background-color : ; color : ; }")
                                    self.label.setText('Waiting ' + str(step + 1))
                                    if (step == len (tablavolts_chk)):
                                        step = 0
                                        # Go to a routine that saves the data and increments the counters.
                                        if (sound == 1):
                                            self.beep('DMMREC1.wav')
                                        self.record()
                                        tablavolts_chk = tablavolts_ori
                                    else:
                                        if (sound == 1):
                                            self.beep('DMMREC2.wav')
                        else:
                            self.printv('\t\tfrase: FAIL ' + str(frase) + '\t' + str(type(frase)) + '\t' + str(len(frase)))
                        # tiempo_final = time() # timer for degug
                        # tiempo_ejecucion = tiempo_final - tiempo_inicial # calc timer for degug
                        # print("Tiempo de ejecucion:\t{:.4f}".format( tiempo_ejecucion )) # show timer for degug
                    except serial.serialutil.SerialException:
                        self.showdialog("Warning! No data on COM this time")
            ser.close()
            sleep(0.2)
            if (ser.isOpen()):
                self.showdialog("Warning! Can't close COM port, program will close")
                exit()
        except:
            self.showdialog("Warning! Can't open COM port")
            ser.close()
            sleep(0.2)
            self.stop()
            self.desconectar()


    # Routine; Beep sound.
    def beep(self,sound):
        if os.path.exists(sound):
            wave_obj = simpleaudio.WaveObject.from_wave_file(sound)
            play_obj = wave_obj.play()
        else:
            self.showdialog("Warning! Can't find " + (str(sound)))


    # Routine; When a cycle ends, saves the data.
    def record(self):
        global tablavolts_chk
        global logpath
        global Count
        global C_Pass
        global C_Fail
        global fail
        global flags_file
        self.printv('Routine record')
        flat_list = []
        # Create a variable with date and time.
        now = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        # Create the name and path of the log.
        log_file =  os.path.join(logpath , str(self.spinBoxorden.value()) + '-' + self.comboBoxArt.currentText() + '-' + socket.gethostname() + '.csv')
        self.printv('\t\t' + str(log_file))
        # Convert tablavolts_chk to a simple list.
        flat_list = [item for sublist in tablavolts_chk for item in sublist]
        flat_list.append(fail)
        flat_list.append(now)
        # If file does not exist, create it and add the header.
        if (os.path.exists(log_file)) is False:
            cabecera = []
            for y in range (len (tablavolts_chk)):
                cabecera.append('Name')
                cabecera.append('Vmax')
                cabecera.append('Value')
                cabecera.append('Vmin')
                cabecera.append('Rel')
                cabecera.append('%')
                cabecera.append('Derivation')
                cabecera.append('Pass')
            cabecera.append('Fail')
            cabecera.append('Date')
            with open(log_file, 'a+') as csvfile:
                salida = csv.writer(csvfile)
                salida.writerow(cabecera)
                salida.writerow(flat_list)
            csvfile.close()
        # File exist so only add data
        else:
            with open(log_file, 'a+') as csvfile:
                salida = csv.writer(csvfile)
                salida.writerow(flat_list)
            csvfile.close()
        # Manage the counters.
        Count = Count + 1
        if (fail == 1):
            C_Fail = C_Fail + 1
            fail = 0
            self.label.setStyleSheet("QLabel { background-color : red ; color : balck; }")
            self.label.setText('Fail.')
        else:
            C_Pass = C_Pass + 1
            self.label.setStyleSheet("QLabel { background-color: green ; color : white; }")
            self.label.setText('Test OK.')
        # Update the status bar
        self.statusBar().showMessage('Ver: 1.0          Count: ' \
        + str(Count) + '     Pass: ' + str(C_Pass) + '     Fail: ' \
        + str(C_Fail) + '               Device config: ' + str(flags_file.get('measure')) \
        + ', ' + str(flags_file.get('acdc')) + ', ' + str(flags_file.get('range'))) 


    # Routine which modifies the max/min values of the relative points
    def relative(self,valor,step):
        global tablavolts_chk
        self.printv('Routine relative')
        tablavolts_tmp = []
        desvio = abs(((valor - tablavolts_chk[step][2]) * 100) / tablavolts_chk[step][2])
        self.printv('\t\tdesvio: ' + str(desvio))
        # Go through the list of points to check.
        for indice in range(len(tablavolts_chk)):
            # If the index is equal to the tested point, we copy adding the read value
            if (indice == step):
                tablavolts_tmp.append([tablavolts_chk[indice][0],tablavolts_chk[indice][1],round(valor,3),tablavolts_chk[indice][3],tablavolts_chk[indice][4],tablavolts_chk[indice][5],round(desvio,2),'1'])
            # This index indicates that its values are relative to the read value.
            elif (tablavolts_chk[indice][4] == (step + 1)):
                proporcion = tablavolts_chk[indice][2] / tablavolts_chk[step][2]
                nuevo_teorico = round(valor * proporcion, 3) 
                Banda = (tablavolts_chk[indice][2]/100)*tablavolts_chk[indice][5]
                Vmax = round(nuevo_teorico + Banda , 3) 
                Vmin = round(nuevo_teorico - Banda , 3)
                tablavolts_tmp.append([tablavolts_chk[indice][0],Vmax,nuevo_teorico,Vmin,tablavolts_chk[indice][4],tablavolts_chk[indice][5],tablavolts_chk[indice][6],tablavolts_chk[indice][6]])
            # The rest of the indexes of the table do not need to be modified.
            else:
                tablavolts_tmp.append(tablavolts_chk[indice])
        # Overwrite the table
        tablavolts_chk = tablavolts_tmp
        # Refresh GUI table.
        self.addtotable(tablavolts_chk)


    # Routine: Change GUI:
    def iconos(self,flags,valor):
        global test_status
        global flags_file
        self.printv('Routine iconos')
        # Represent the state of the battery.
        self.printv('\t\tflags: ' + str(flags))
        self.printv('\t\tvalor: ' + str(valor))
        if (flags.get('lowbat') == 'BAT-OK'):
            pixmap = QPixmap('./Iconos/Bateria-full.png')
        elif (flags.get('lowbat') == 'LOWBAT'):
            pixmap = QPixmap('./Iconos/Bateria-empty.png')
        else:
            pixmap = QPixmap('./Iconos/ico-blank.png')
        self.label_bat.setPixmap(pixmap)
        if (valor == 'OVERFLOW'):
            self.label_DMM.setText('overflow')
        else:
            # Represent the necessary zeros.
            try:
                if (valor < 9.999): 
                    self.label_DMM.setText(str("%.3f" % valor) + ' ' + flags.get('measure'))
                elif (valor < 99.99): 
                    self.label_DMM.setText(str("%.2f" % valor) + ' ' + flags.get('measure'))
                else: 
                    self.label_DMM.setText(str("%.1f" % valor) + ' ' + flags.get('measure'))
            except:
                self.label_DMM.setText('overflow')
        # Represent the state of AC / DC.
        if (flags.get('acdc') == 'AC') or (flags.get('acdc') == 'ac'):
            pixmap = QPixmap('./Iconos/ico-ac.png')
        elif (flags.get('acdc') == 'DC') or (flags.get('acdc') == 'dc'):
            pixmap = QPixmap('./Iconos/ico-dc.png')
        else:
            pixmap = QPixmap('./Iconos/ico-blank.png')
        self.label_acdc.setPixmap(pixmap)
        # If flag test_status is on check if DMM flags are the same as loaded one.                        
        if (test_status == 1):
            if (flags.get('acdc') != flags_file.get('acdc')) \
            or (flags.get('measure') != flags_file.get('measure')) \
            or (flags.get('range') != flags_file.get('range')):
                self.stop()
                self.showdialog('Check the DMM settings.')


    # Routine: Refresh the available ports.
    def RefreshComPort(self):
        global archivo_ini
        self.printv('Routine RefreshComPort')
        defaultcom,message = lib_ini.readini(archivo_ini,'Default','Defaultcom')
        if (message):
            self.printv('\t' + str(message))
            self.showdialog('Error in the Defaultcom value of the ini file.')
        coms=[]
        self.comboBoxPort.clear()
        for potentialPort in list(serial.tools.list_ports.comports()):
            coms.append(potentialPort.device)
        self.comboBoxPort.addItems(coms)
        if coms:
            if defaultcom in coms:
                self.comboBoxPort.setCurrentIndex(coms.index(defaultcom))
        else:
            self.showdialog('No COM ports avalaible')
            exit()


    # Routine: Search the ini file of the program.
    def Checkini(self):
        global archivo_ini
        global verbose
        global sound
        global repeatini
        global logpath
        if (os.path.exists('DMMREC.ini')) is False:
            self.showdialog('DMMREC.ini is not found, essential for the application to work')
            exit()
        else:
            archivo_ini = os.path.realpath('DMMREC.ini')
        value,message = lib_ini.readini(archivo_ini,'Default','verbose')
        if (message) or ((value != '1') and (value != '0')):
            self.printv('\t' + str(message) + '\t' + str(value))
            self.showdialog('Error in the verbose value of the ini file, it is set to 0.')
            verbose = 0
        else:
            verbose = int(value)
        self.printv('verbose: ' + str(verbose))
        Defaultbatchnr,message = lib_ini.readini(archivo_ini,'Default','Defaultbatchnr')
        if (message):
            self.printv('\t' + str(message))
            self.showdialog('Error in the Defaultbatchnr value of the ini file, it is set to 0.')
            Defaultbatchnr = 0
        try:
            Defaultbatchnr = int(Defaultbatchnr)
            self.spinBoxorden.setValue(Defaultbatchnr)
        except:
            self.showdialog('Error in the Defaultbatchnr value of the ini file, it is set to 1.')
            Defaultbatchnr = 1
        self.printv('Defaultbatchnr: ' + str(Defaultbatchnr))
        value,message = lib_ini.readini(archivo_ini,'Default','sound')
        if (message) or ((value != '1') and (value != '0')):
            self.printv('\t' + str(message) + '\t' + str(value))
            self.showdialog('Error in the sound value of the ini file, it is set to 0.')
            sound = 0
        else:
            sound = int(value)
        self.printv('sound: ' + str(sound))
        logpath,message = lib_ini.readini(archivo_ini,'Default','Log_files')
        if (message):
            self.printv('\t' + str(message))
            self.showdialog('Error in the Log_files value of the ini file, program will close.')
            exit()
        if (os.path.exists(logpath)) is False:
            self.showdialog('Log_files folder dont exist, program will close')
            exit()
        self.printv('logpath: ' + str(logpath))
        repeatini,message = lib_ini.readini(archivo_ini,'Default','Repeat')
        if (message):
            self.printv('\t' + str(message))
            self.showdialog('Error in the repeat value of the ini file, it is set to 2.')
            repeatini = 2
        else:
            try:
                repeatini = int(repeatini)
            except:
                self.showdialog('Error in the repeat value of the ini file, it is set to 2.')
                repeatini = 2
        self.printv('repeatini: ' + str(repeatini))

    # Routine: Displays a dialog type message.
    def showdialog(self,a):
        msg = QtWidgets.QMessageBox()
        msg.setText(a)
        msg.setWindowTitle(' ')
        retval = msg.exec_()


    # Routine: printl, verbose info if flag is on .
    def printv(self,texto):
        global verbose
        if (verbose == 1):
            print (texto)


# Main Program Execution.
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('plastique')
    window = MyApp()
    # Hide Maximice option (comment to enable)
    window.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
    window.show()
sys.exit(app.exec_())
