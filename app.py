import configparser
import sys
from time import sleep

import pyuipc as fs
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from pypresence import Presence

import gui

isConnectedToSim = False

config = configparser.ConfigParser()
config.read("settings.ini")
networks = config["DEFAULT"]["networks"].split(" #")[0].split(",")
defaultSimulator = config["DEFAULT"]["defaultSim"].split(" #")[0].lower()

# Exception hook for catching all errors from PyQt
sys._excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = exception_hook

clientIds = {
    "fsx": "463018682403127306",
    "p3d": "472340913302011914",
    "x-plane": "472341679844622337"
}


def connectToSim(ui):
    try:
        fs.open(0)
        ui.statusLabel.setText("Connected to simulator!")
        global isConnectedToSim  # sorry not sorry
        isConnectedToSim = True
    except Exception:
        msg = QMessageBox()
        msg.setText("Cannot connect to simulator.")
        msg.exec_()


def disconnectFromSim(ui):
    fs.close()
    ui.statusLabel.setText("Not connected to FSUIPC")
    global isConnectedToSim
    isConnectedToSim = False


def mainFunction(ui, Form):
    if not isConnectedToSim:
        confirm = QMessageBox()
        showDia = confirm.question(None, "", "Are you sure you want to proceed without connecting to the simulator?",
                                   confirm.Yes | confirm.No)
        if showDia == confirm.No:
            return

    simulator = clientIds[ui.simCombo.currentText().lower()]
    departure = ui.depLine.text()
    destination = ui.arrLine.text()
    airframe = ui.airframeLine.text()
    altitude = ui.cruiseLine.text()
    network = ui.networkCombo.currentText()
    callsign = ui.callLine.text()

    if departure == "" or destination == "" or airframe == "" or callsign == "" or altitude == "":
        msg = QMessageBox()
        msg.setText("Please enter a value in all fields")
        msg.exec()
        return

    Form.close()

    standardItems = {
        "large_image": "planeiconlarge",
        "large_text": "FSX"
    }

    rotatingItems = [
        {
            "state": f"Airframe: {airframe}"
        },
        {
            "state": f"Cruise: {altitude}ft"
        },
        {
            "state": f"Callsign: {callsign}"
        }
    ]

    if not network.lower() == "offline":
        rotatingItems.append({"state": f"Connected to: {network}"})
    else:
        rotatingItems.append({"state": f"Cruise: {altitude}ft"})

    rotatingStats = [
        {
            "text": "Ground speed: {}kts",
            "action": lambda: str(round((fs.read(fs.prepare_data([(0x02B4, "d")]))[0] / 65536) * 1.94384))
        },
        {
            "text": "Altitude: {}ft",
            "action": lambda: str(round(fs.read(fs.prepare_data([(0x6020, "f")]))[0] * 3.28084))
        },
        {
            "text": "Status: {}",
            "action": lambda: "On ground" if fs.read(fs.prepare_data([(0x0366, "b")]))[0] == 1 else "Climb" if round(
                fs.read(fs.prepare_data([(0x02C8, "d")]))[0] * 60 * 3.28084 / 256) > 20 else "Descent" if round(
                fs.read(fs.prepare_data([(0x02C8, "d")]))[0] * 60 * 3.28084 / 256) < -20 else "Levelled off"
        },
        {
            "text": "Flying {}",
            "action": lambda: f"{departure} to {destination}" if True else "no"
        }
    ]

    rp = Presence(simulator)
    rp.connect()

    print("Running")
    while True:
        for i in range(4):
            print(f"Item {i}")
            for index, item in enumerate(rotatingItems):
                print(f"  Sub-item {index}")
                for ii in range(5):
                    print(f"    Sub-sub-item {ii}")
                    if isConnectedToSim:
                        disp = {"details": rotatingStats[index]["text"].format(rotatingStats[index]["action"]())}
                    else:
                        disp = {"details": rotatingStats[-1]["text"].format(rotatingStats[-1]["action"]())}
                    rp.update(**item, **standardItems, **disp)
                    sleep(1)


app = QApplication(sys.argv)
Form = QWidget()
ui = gui.Ui_Form()
ui.setupUi(Form)

for text in networks:
    ui.networkCombo.addItem(text)

if defaultSimulator == "fsx":
    ui.simCombo.setItemText(0, "FSX")
    ui.simCombo.setItemText(1, "P3D")
    ui.simCombo.setItemText(2, "X-Plane")
elif defaultSimulator == "p3d":
    ui.simCombo.setItemText(0, "P3D")
    ui.simCombo.setItemText(1, "FSX")
    ui.simCombo.setItemText(2, "X-Plane")
elif defaultSimulator == "xp":
    ui.simCombo.setItemText(0, "X-Plane")
    ui.simCombo.setItemText(1, "P3D")
    ui.simCombo.setItemText(2, "FSX")
else:
    msg = QMessageBox()
    msg.setText("Default simulator value is invalid. Defaulting to FSX.")
    msg.exec()

ui.connectButton.clicked.connect(lambda: connectToSim(ui))
ui.disconnectButton.clicked.connect(lambda: disconnectFromSim(ui))
ui.startButton.clicked.connect(lambda: mainFunction(ui, Form))

Form.show()
sys.exit(app.exec())
