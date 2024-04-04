import sys, os

from PyQt5.QtWidgets import QApplication, QMessageBox, QProgressBar, QFrame, QGroupBox, QDoubleSpinBox, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox, QLabel, QSpinBox, QGridLayout, QScrollBar, QDial, QPushButton

from PyQt5.QtGui import QPainter, QColor

from PyQt5.QtCore import Qt, pyqtSignal, QThread

import serial

import numpy as np

import time

import serial.tools.list_ports



     
class External(QThread):
    countChanged = pyqtSignal([int,int,int])
    finished = pyqtSignal()
    def run(self):

        while True:
            arduino_count = ser.readline().decode('ascii')
            sep = arduino_count.find("/")
            dob1 = arduino_count.find(":")
            dob2 = arduino_count.find(":",dob1+1)
            paso = int(arduino_count[:dob1])
            vuelta = int(arduino_count[sep+1:dob2])
            TIME_LIMIT = int(arduino_count[dob2+1:])*int(arduino_count[dob1+1:sep])
            self.countChanged.emit(paso,vuelta,(int(arduino_count[dob1+1:sep]))*vuelta+paso+1)
            if (int(arduino_count[dob1+1:sep]))*vuelta+paso+1 == TIME_LIMIT:
                self.finished.emit()
                self.quit()
                break
             

class MyButton(QPushButton):

    entered = pyqtSignal()

    def enterEvent(self, event):

        self.entered.emit()
        

class CheckBoxes(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("SILAR v2 Controller")

        self.p = 0

        self.initial_pos = QPushButton(self)

        self.initial_pos.setText("Autohome")

        self.initial_pos.clicked.connect(self.autohome)

        self.start = QPushButton(self)

        self.start.setText("Move SILAR")

        self.start.clicked.connect(self.move_SILAR)

        self.start_cycle = MyButton(self)

        self.start_cycle.setText("Start Process")

        self.start_cycle.clicked.connect(self.start_process)

        self.start_cycle.entered.connect(self.vel)

        self.label_main = QLabel("PhotoVoltaics Researchs Laboratory")

        self.label_workstation = QLabel("Workstations:")

        self.label_Dial_Spin_boxes = QLabel("Number of Base Steps:")

        self.label_HSpin_boxes = QLabel("Number of Crane Steps:")

        self.label_scroll_bar = QLabel("Crane Movement:")

        self.label_Dial = QLabel("Base Movement:")

        self.label_dip_sp = QLabel("Dip Speed (mm/s):")

        self.label_extra_sp = QLabel("Extraction Speed (mm/s):")

        self.label_dip_dn = QLabel("Dip Duration (sec):")

        self.label_progress_bar = QLabel("Progress Bar")

        self.label_cycles = QLabel("Number of Cycles:")

        # Agregar número de ciclos

        self.cycle = QSpinBox(self)  

        # Crear la combobox

        self.combo_box = QComboBox(self)

        self.combo_box.addItems(['1 Workstation', '2 Workstation', '3 Workstation', '4 Workstation', '5 Workstation', '6 Workstation', '7 Workstation', '8 Workstation'])

        self.combo_box.currentIndexChanged.connect(self.show_check_boxes)

        # Crear el layout vertical para el widget principal

        self.layout = QGridLayout(self)

        self.layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.layout.addWidget(self.label_main,0,0,1,2)

        self.layout.addWidget(self.label_workstation,2,5)

        self.layout.addWidget(self.label_Dial_Spin_boxes,3,5)

        self.layout.addWidget(self.label_HSpin_boxes,4,5)

        self.layout.addWidget(self.combo_box,1,6)

        self.layout.addWidget(self.cycle,1,9)

        self.layout.addWidget(self.label_dip_sp,5,5)

        self.layout.addWidget(self.label_extra_sp,6,5)

        self.layout.addWidget(self.label_dip_dn,7,5)

        self.layout.addWidget(self.label_cycles,1,8)

        # Establecer el layout horizontal para los checkboxes

        #self.h_layout = QHBoxLayout()

        #self.layout.addLayout(self.h_layout,1,0)

        # Agregar los checkboxes al layout horizontal

        if os.path.exists("archivo.txt"):

            with open("archivo.txt", mode="r") as file:
        
                data = file.readline().strip()

                data = data.replace(" ","")

                file.close()

            self.check_boxes = []

            d_point = data.find(":")

            sep_1 = data.find("/")

            data_combo = int(data[d_point+1:sep_1])

            sep_2 = data.find("/",sep_1+1)

            data_cycle = int(data[sep_1+1:sep_2])

            sep_3 = data.find("/",sep_2+1)

            data_pos = data[sep_2+1:sep_3]

            data_pos_real = convert(data_pos,data_combo)

            sep_4 = data.find("/",sep_3+1)

            data_heigth = data[sep_3+1:sep_4]

            data_heigth_real = convert(data_heigth,data_combo)        

            sep_5 = data.find("/",sep_4+1)

            data_inmersion = data[sep_4+1:sep_5]

            data_inmersion_real = convert_float(data_inmersion,data_combo)

            sep_6 = data.find("/",sep_5+1)

            data_extraction = data[sep_5+1:sep_6]

            data_extraction_real = convert_float(data_extraction,data_combo)

            sep_7 = data.find("/",sep_6+1)

            data_time = data[sep_6+1:sep_7]

            data_time_real = convert_float(data_time,data_combo)


            for i in range(8):
            
                checkbox = QCheckBox(f"Workstation {i+1}")

                checkbox.hide()

                checkbox.clicked.connect(self.on_checkbox_clicked)

                self.check_boxes.append(checkbox)

            def set_value(cont, comp, box, value):

                if cont < comp:

                    box.setValue(value[i])
            

            # Agregar los spin boxes

            self.HSpin_boxes = []

            for i in range(8):
            
                spinbox = QSpinBox(self)

                spinbox.hide()

                spinbox.setRange(0, 450)

                set_value(i,data_combo,spinbox,data_heigth_real)

                self.HSpin_boxes.append(spinbox)
        
            self.Velocity_Spin_boxes = []

            for i in range(8):
            
                spinbox = QDoubleSpinBox(self)

                spinbox.hide()

                set_value(i,data_combo,spinbox,data_inmersion_real)

                self.Velocity_Spin_boxes.append(spinbox)

            self.Velocity_Extra_Spin_boxes = []

            for i in range(8):
            
                spinbox = QDoubleSpinBox(self)

                spinbox.hide()

                set_value(i,data_combo,spinbox,data_extraction_real)

                self.Velocity_Extra_Spin_boxes.append(spinbox)

            self.Time_Spin_boxes = []

            for i in range(8):
            
                spinbox = QDoubleSpinBox(self)

                spinbox.hide()

                set_value(i,data_combo,spinbox,data_time_real)

                spinbox.setRange(0, 5000)

                self.Time_Spin_boxes.append(spinbox)

            self.Dial_Spin_boxes = []

            for i in range(8):
            
                spinbox = QSpinBox(self)

                spinbox.hide()

                spinbox.setRange(0, 199)

                set_value(i,data_combo,spinbox,data_pos_real)

                self.Dial_Spin_boxes.append(spinbox)

            # Crear el layout horizontal para los spinboxes y checkboxes

            self.combo_box.setCurrentIndex(data_combo-1)

        else:
            self.check_boxes = []

            for i in range(8):
            
                checkbox = QCheckBox(f"Workstation {i+1}")

                checkbox.hide()

                checkbox.clicked.connect(self.on_checkbox_clicked)

                self.check_boxes.append(checkbox)

            self.HSpin_boxes = []

            for i in range(8):
            
                spinbox = QSpinBox(self)

                spinbox.hide()

                spinbox.setRange(0, 450)

                self.HSpin_boxes.append(spinbox)
        
            self.Velocity_Spin_boxes = []

            for i in range(8):
            
                spinbox = QDoubleSpinBox(self)

                spinbox.hide()

                self.Velocity_Spin_boxes.append(spinbox)

            self.Velocity_Extra_Spin_boxes = []

            for i in range(8):
            
                spinbox = QDoubleSpinBox(self)

                spinbox.hide()

                self.Velocity_Extra_Spin_boxes.append(spinbox)

            self.Time_Spin_boxes = []

            for i in range(8):
            
                spinbox = QDoubleSpinBox(self)

                spinbox.hide()

                spinbox.setRange(0, 5000)

                self.Time_Spin_boxes.append(spinbox)

            self.Dial_Spin_boxes = []

            for i in range(8):
            
                spinbox = QSpinBox(self)

                spinbox.hide()

                spinbox.setRange(0, 199)

                self.Dial_Spin_boxes.append(spinbox)
        # Crear el layout horizontal para los spinboxes y checkboxes

        for i in range(8):

            self.layout.addWidget(self.check_boxes[i],2,i+6)

            self.layout.addWidget(self.Dial_Spin_boxes[i],3,i+6)        

            self.layout.addWidget(self.HSpin_boxes[i],4,i+6)

            self.layout.addWidget(self.Velocity_Spin_boxes[i],5,i+6)

            self.layout.addWidget(self.Velocity_Extra_Spin_boxes[i],6,i+6)

            self.layout.addWidget(self.Time_Spin_boxes[i],7,i+6)

        # Creamos la primera QScrollBar

        self.dial = QDial(self)

        self.dial.setRange(0, 199)

        self.dial.setNotchesVisible(True)

        self.dial.setWrapping(True)

        self.dial.setFixedWidth(100)

        self.dial.setFixedHeight(100)

        # Creamos la segunda QScrollBar

        self.scroll_bar = QScrollBar(self)

        self.scroll_bar.setMaximum(450)

        self.scroll_bar.setMaximumHeight(200)

        self.scroll_bar.setMaximumWidth(20)

        self.scroll_bar.setOrientation(0)

        #self.frame = QFrame(self)

        #self.frame.setFrameStyle(QFrame.Box)

        #self.layout.addWidget(self.frame, 1, 10, 5, 5)

        #self.layout.setContentsMargins(1, 10, 5, 5)

        # Crear la sección de movimiento

        self.group_box = QGroupBox("Movement Section")

        self.group_box_layout = QGridLayout(self)

        self.group_box_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.group_box_layout.addWidget(self.label_Dial,0,0)

        self.group_box_layout.addWidget(self.dial,1,0,4,4)

        self.group_box_layout.addWidget(self.scroll_bar,1,4,4,1)

        self.group_box_layout.addWidget(self.start,5,0)

        self.group_box_layout.addWidget(self.initial_pos,5,1)

        self.group_box_layout.addWidget(self.start_cycle,5,4)

        self.group_box_layout.addWidget(self.label_scroll_bar,0,4)

        self.group_box.setLayout(self.group_box_layout)

        self.layout.addWidget(self.group_box,1, 0, 6, 5)

        # Crear barra de progreso

        self.bar = QProgressBar(self)

        self.bar.setMinimum(0)

        # Añadir barra al layout

        self.layout.addWidget(self.label_progress_bar,8,0)

        self.layout.addWidget(self.bar,8,1,1,14)        

        self.setLayout(self.layout)

    # Función para mostrar los check_boxes seleccionados en la combobox

    def show_check_boxes(self, index):

        for i in range(8):

            if i <= index:

                self.check_boxes[i].show()

                self.HSpin_boxes[i].show()

                self.Dial_Spin_boxes[i].show()

                self.Time_Spin_boxes[i].show()

                self.Velocity_Spin_boxes[i].show()

                self.Velocity_Extra_Spin_boxes[i].show()

            else:

                self.check_boxes[i].hide()

                self.HSpin_boxes[i].hide()

                self.Dial_Spin_boxes[i].hide()

                self.Time_Spin_boxes[i].hide()

                self.Velocity_Spin_boxes[i].hide()

                self.Velocity_Extra_Spin_boxes[i].hide()

    # Función para deseleccionar los demás checkboxes

    def on_checkbox_clicked(self):

        sender = self.sender()

        for i in range(8):

            if self.check_boxes[i] != sender:

                self.check_boxes[i].setChecked(False)

                self.HSpin_boxes[i].setReadOnly(True)

                self.Dial_Spin_boxes[i].setReadOnly(True)

                self.check_boxes[i].setStyleSheet("QCheckBox { color: black; }")

                self.HSpin_boxes[i].setStyleSheet("QCheckBox { color: black; }")

                self.Dial_Spin_boxes[i].setStyleSheet("QCheckBox { color: black; }")
            else:
                self.p = i

        sender.setStyleSheet("QCheckBox { background-color: blue; color: white;}")

        self.HSpin_boxes[self.p].setReadOnly(False)

        self.Dial_Spin_boxes[self.p].setReadOnly(False)

        hreceivers = self.dial.receivers(self.dial.valueChanged)

        vreceivers = self.scroll_bar.receivers(self.scroll_bar.valueChanged)

        if vreceivers != 0 or hreceivers !=0:

            self.HSpin_boxes[self.p].disconnect()

            self.dial.disconnect()

            self.Dial_Spin_boxes[self.p].disconnect()

            self.scroll_bar.disconnect()

        self.HSpin_boxes[self.p].valueChanged.connect(self.scroll_bar.setValue)

        self.scroll_bar.valueChanged.connect(self.HSpin_boxes[self.p].setValue)

        self.Dial_Spin_boxes[self.p].valueChanged.connect(self.dial.setValue)

        self.dial.valueChanged.connect(self.Dial_Spin_boxes[self.p].setValue)

        self.scroll_bar.setValue(0)

        self.dial.setValue(0)

        #for wid in hreceivers:

        #    if wid != HSpin_boxes[self.p]:

        #        self.dial.valueChanged.disconnect(self.wid)

        #for wid in vreceivers:

        #    if wid != Dial_Spin_boxes[self.p]:

         #       self.scroll_bar.valueChanged.disconnect(self.wid)


        self.HSpin_boxes[self.p].setStyleSheet("QSpinBox{ background-color: blue; color: white; }")

        self.Dial_Spin_boxes[self.p].setStyleSheet("QSpinBox { background-color: blue; color: white; }")

    # Función que envia la información al arduino

    def move_SILAR(self):

        #print((f"[M:{self.p}/{self.dial.value()}/{self.scroll_bar.value()}/]").encode('ascii'))
        
        ser.write((f"[M:{self.p}/{self.dial.value()}/{self.scroll_bar.value()}/]").encode('ascii'))

    def autohome(self):

        #print((f"[A:/]").encode('ascii'))

        ser.write((f"[A:/]").encode('ascii'))
            
    def actualizarb(self,paso,ciclo,total):
        self.bar.setValue(total)
        max_value = self.bar.maximum()
        self.label_progress_bar.setText("Process finished step number  " + str(paso+1) + " of cycle  " + str(ciclo+1))

    def message(self):
        self.start_cycle.setDisabled(False)

        self.start.setDisabled(False)

        self.initial_pos.setDisabled(False)

        self.msg=QMessageBox(self)
        self.msg.setWindowTitle("Process Finished")
        self.msg.setText("The process has finished")
        self.msg.setIcon(QMessageBox.Information)                    
        self.x = self.msg.exec_()

    def start_process(self):

        HSpin_boxes_value = valores(self,self.HSpin_boxes)

        Velocity_Spin_boxes_value = valores(self,self.Velocity_Spin_boxes)

        Velocity_Extra_Spin_boxes_value = valores(self,self.Velocity_Extra_Spin_boxes)

        Dial_Spin_boxes_value = valores(self,self.Dial_Spin_boxes)

        Time_Spin_boxes_value = valores(self,self.Time_Spin_boxes)

        self.start_cycle.setDisabled(True)

        self.start.setDisabled(True)

        self.initial_pos.setDisabled(True)

        ser.write((f"[S:{self.combo_box.currentIndex()+1}/{self.cycle.value()}/{Dial_Spin_boxes_value}/{HSpin_boxes_value}/{Velocity_Spin_boxes_value}/{Velocity_Extra_Spin_boxes_value}/{Time_Spin_boxes_value}/]").encode('ascii'))

        with open("archivo.txt", mode="w") as file:
            # Escribir la cadena dentro del archivo
            file.write(f"[S:{self.combo_box.currentIndex()+1}/{self.cycle.value()}/{Dial_Spin_boxes_value}/{HSpin_boxes_value}/{Velocity_Spin_boxes_value}/{Velocity_Extra_Spin_boxes_value}/{Time_Spin_boxes_value}/]")


        #print(f"[S:{self.combo_box.currentIndex()+1}/{self.cycle.value()}/{Dial_Spin_boxes_value}/{HSpin_boxes_value}/{Velocity_Spin_boxes_value}/{Velocity_Extra_Spin_boxes_value}/{Time_Spin_boxes_value}/]")
        
        self.bar.setMaximum((self.combo_box.currentIndex()+1)*self.cycle.value())

        self.calc = External()

        self.calc.countChanged.connect(self.actualizarb)

        self.calc.start()
        
        self.calc.finished.connect(self.message)

    def vel(self):

        Velocity_Spin_boxes_value = valores(self,self.Velocity_Spin_boxes)

        Velocity_Extra_Spin_boxes_value = valores(self,self.Velocity_Extra_Spin_boxes)

        for i in range(self.combo_box.currentIndex()+1):

            if Velocity_Spin_boxes_value[i] == 0 or Velocity_Extra_Spin_boxes_value[i] == 0:

                self.start_cycle.setDisabled(True)

                break

            else:

                self.start_cycle.setDisabled(False)

def convert(string,num):

    array = []

    pos = 0

    for i in range(num):
        
        coma = string.find(",",pos+1)

        array.append(int(string[pos+1:coma]))

        pos = coma

    return array


def convert_float(string,num):

    array = []

    pos = 0

    for i in range(num):
        
        coma = string.find(",",pos+1)

        array.append(float(string[pos+1:coma]))

        pos = coma

    return array
            
def valores(self,lista):

    new_array=[]

    for i in range(self.combo_box.currentIndex()+1):

        new_array.append(lista[i].value())

    return new_array   


if __name__ == '__main__':

    app = QApplication(sys.argv)

    app.setStyle('Fusion')              #'Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion'

    puertos = []

    ports = serial.tools.list_ports.comports()

    for p in ports:
        puertos.append(p.device)

    if len(puertos) == 0:
        msg=QMessageBox()
        msg.setWindowTitle("Conect a device")
        msg.setText("There aren't any device conected")
        msg.setIcon(QMessageBox.Critical)                    
        x = msg.exec_()
    elif len(puertos) != 0:
        ser=serial.Serial(puertos[0],9600)      #Inicializar communicaci\'on serial

        checkboxes = CheckBoxes()

        checkboxes.show()

        sys.exit(app.exec_())

    

    