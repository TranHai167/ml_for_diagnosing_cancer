from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from pathlib import Path
import os
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from load_to_database import insert_data_to_db, get_data
from svm import train, getExpression, mining, call_mining
import MySQLdb

savePath = ""
settingsFilePath = Path("settings.txt")
icon = ''

if not settingsFilePath.is_file():
    f = open("settings.txt", "w")
    savePath = os.environ["HOMEPATH"] + "\\Desktop\\"
    f.write(savePath)
    f.close()
else:
    f = open("settings.txt", "r")
    savePath = f.readline()
    f.close()


def convertToPy(target):
    os.system('pyuic5 -o "' + savePath + '/convertedfile.py" "' + target + '"')


# chan_doan là chan doan cua file dau vao
# cd la chan doan mo hinh
def export_file(path, trieu_chung, data_frame, new_chan_doan, new_cd):
    # cd.append(0)
    metrx = confusion_matrix(new_chan_doan, new_cd)
    print("Confuse matrix: ")
    print(metrx)

    # Dự đoán -> Thực tế
    # [0, 0]:   Dương tính - thật
    # [0, 1]:   Dương tính - giả
    # [1, 0]:   Âm tính - giả
    # [1, 1]:   Âm tính - thật

    # Độ nhạy của một xét nghiệm là tỷ lệ những trường hợp thực sự có bệnh và có kết quả xét nghiệm dương tính trong toàn bộ các trường hợp có bệnh.
    print("Độ nhạy: " + str(metrx[1][1] / (metrx[1][1] + metrx[1][0])))

    # Độ đặc hiệu của một xét nghiệm là tỷ lệ những trường hợp thực sự không có bệnh và có kết quả xét nghiệm âm tính trong toàn bộ các trường hợp không bị bệnh.
    print("Độ đặc hiệu: " + str(metrx[0][0] / (metrx[0][0] + metrx[0][1])))
    print("-" * 50)

    print("Pre: ", len(new_cd), "; Real: ", len(new_chan_doan))
    print(len(data_frame))
    print(len(new_cd))

    data = [data_frame['MABN'], data_frame['HOTEN'], data_frame['TUOI'], data_frame['NAMSINH'], data_frame['GIOITINH'],
            data_frame['THON'], data_frame['TENPXA'], data_frame['TENQUAN'], data_frame['TENTT'], data_frame['TENNN'],
            data_frame['NGAYVK'], data_frame['TENKP'], data_frame['DOITUONG'], trieu_chung, new_cd, new_chan_doan]

    df = pd.DataFrame(data=np.array(data).T,
                      columns=['Mã BN', 'Họ tên', "Tuổi", "Năm sinh", "Giới tính", "Thôn", "Tên phường, xã", "Quận",
                               "Thị trấn", "Nghề nghiệp", "Ngày vào khám", "Tên KP", "Đối tượng", "Triệu chứng",
                               "Dự đoán", "Thực tế"])

    path = path + "/ketquachandoan.xlsx"
    print("Path: ", path)
    df.to_excel(path, index=False)
    print("Okii")


class Label(QtWidgets.QLabel):
    def __init__(self):
        super(Label, self).__init__()

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat("text/uri-list"):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        path = e.mimeData().text()
        self.setText(e.mimeData().text())
        # fileInfo = QtCore.QFileInfo(path)
        # iconProvider = QtGui.QFileIconProvider()
        # icon = iconProvider.icon(fileInfo)
        print()


class MainWindow(QtWidgets.QWidget):
    df = ''
    model = ''

    def __init__(self):
        super().__init__()
        self.windowTitle = "Demo Interface"
        self.windowSize = (438, 348)
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowTitle(self.windowTitle)
        Form.resize(self.windowSize[0], self.windowSize[1])
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelIcon = QtWidgets.QLabel(self.frame)
        self.labelIcon.setMaximumSize(QtCore.QSize(50, 50))
        self.labelIcon.setText("")
        self.labelIcon.setPixmap(QtGui.QPixmap("info.png"))
        self.labelIcon.setScaledContents(True)
        self.labelIcon.setObjectName("labelIcon")
        self.horizontalLayout.addWidget(self.labelIcon)
        self.labelInfo = QtWidgets.QLabel(self.frame)
        self.labelInfo.setWordWrap(True)
        self.labelInfo.setObjectName("labelInfo")
        self.labelInfo.setText("Phần mềm DEMO chẩn đoán ung thư đại tràng")
        self.labelInfo.setOpenExternalLinks(True)
        self.horizontalLayout.addWidget(self.labelInfo)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        # self.labelTarget = QtWidgets.QLabel(self.frame_2) -> removed, as I'm going to use a custom Label
        self.buttonBrowse_1 = QtWidgets.QPushButton(self.frame_2)
        self.buttonBrowse_1.setObjectName("buttonBrowse")
        self.buttonBrowse_1.setText("Browse")
        self.labelTarget = Label()
        font = QtGui.QFont()
        font.setFamily("Myanmar Text")
        self.labelTarget.setFont(font)
        self.labelTarget.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTarget.setObjectName("labelTarget")
        self.labelTarget.setText("Kéo thả <b>Hồ sơ bệnh nhân (*.xlxs)</b> vào đây")
        self.labelTarget.setStyleSheet("QLabel { border: 1px dotted black; }")
        self.labelTarget.setMinimumHeight(150)
        self.labelTarget.setAcceptDrops(True)
        self.verticalLayout_5.addWidget(self.labelTarget)
        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout_5.addWidget(self.buttonBrowse_1)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(Form)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.labelQuestion = QtWidgets.QLabel(self.frame_3)
        self.labelQuestion.setObjectName("labelQuestion")
        self.labelQuestion.setText("Chọn vị trí lưu file <b>EXCEL</b>")
        self.verticalLayout_3.addWidget(self.labelQuestion)
        self.frame_4 = QtWidgets.QFrame(self.frame_3)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.inputDirectory = QtWidgets.QLineEdit(self.frame_4)
        self.inputDirectory.setObjectName("inputDirectory")
        self.inputDirectory.setText(savePath)
        self.inputDirectory.setStyleSheet("QLineEdit { padding-bottom: 2px; padding-left: 2px; }")
        self.horizontalLayout_5.addWidget(self.inputDirectory)
        self.buttonBrowse = QtWidgets.QPushButton(self.frame_4)
        self.buttonBrowse.setObjectName("buttonBrowse")
        self.buttonBrowse.setText("Browse")

        # Thêm vào
        self.buttonDig = QtWidgets.QPushButton(self.frame_3)
        self.buttonDig.setObjectName("buttonDig")
        self.buttonDig.setText("Diagnose")

        self.horizontalLayout_5.addWidget(self.buttonBrowse)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.addWidget(self.frame_4)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout.addWidget(self.frame_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        # Thêm vào
        self.horizontalLayout_5.addWidget(self.buttonDig)
        self.verticalLayout_5.addWidget(self.buttonDig)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.buttonBrowse.clicked.connect(self.browsePath)
        self.buttonBrowse_1.clicked.connect(self.browsePath_1)
        self.buttonDig.clicked.connect(self.dig)

    def browsePath(self):
        savePath = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select directory"))
        self.inputDirectory.setText(savePath)
        with open(settingsFilePath, "w") as f:
            f.write(savePath)

    def browsePath_1(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        self.labelTarget.setText(path)

    def dig(self):
        path = self.labelTarget.text()
        # data_frame = pd.read_excel(self.labelTarget.text())
        insert_data_to_db(mycursor, database, path)
        print("Insert successfully")
        mycursor.close()

        # Commit transaction
        database.commit()

        # Close the db connection
        database.close()
        print("Close database")

        data_frame = pd.read_excel(self.labelTarget.text())
        print(np.shape(data_frame))

        new_feature, new_chandoan = call_mining(data_frame)
        new_chandoan.pop()
        print(np.shape(new_feature), ", ", len(new_chandoan))

        trieu_chung = []
        for i in np.array(new_feature).T:
            trieu_chung.append(getExpression(i))

        print("------------------")
        new_cd_predict = model.predict(np.array(new_feature).T)
        print("Predicted successfully!!!")
        export_file(self.inputDirectory.text(), trieu_chung, data_frame, new_chandoan, new_cd_predict)

    def setupModel(self, model):
        self.model = model


if __name__ == "__main__":
    import sys

    database = MySQLdb.connect(host='localhost', user='TranHai', passwd='16072002', db='test')
    mycursor = database.cursor()
    data = get_data(mycursor)
    print(len(data))
    feature, chandoan = mining(data)
    print("LEN: ", np.shape(feature), " : ", len(chandoan))
    model = train(feature, chandoan)
    print("model oke!")

    app = QtWidgets.QApplication(sys.argv)
    hGUI = QtWidgets.QWidget()
    ui = MainWindow()
    ui.setupUi(hGUI)
    ui.setupModel(model)

    hGUI.show()
    sys.exit(app.exec_())
