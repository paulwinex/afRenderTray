from PySide.QtCore import *
from PySide.QtGui import *
import sys, os

#command
cmd = os.path.join(os.path.dirname(__file__), 'start/AFANASY/render.cmd')
#icon
icon = os.path.join(os.path.dirname(__file__),'icons/terminal.png')
#timer
reconnectTimeout = 10 #sec

class afTrayClass(QObject):
    def __init__(self):
        super(afTrayClass, self).__init__()
        #tray
        self.trayIcon = QSystemTrayIcon(QIcon(icon), self)
        self.connect(self.trayIcon, SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.trayIconActivated)
        self.proc = QProcess()
        self.w = consoleClass(self)
        self.process = QProcess()
        self.connect( self.process, SIGNAL('readyRead()'), self.toOutput)
        self.process.finished.connect(self.repeatConnect)
        self.trayIcon.show()
        self.start()

    def __del__(self):
        self.quit()

    def repeatConnect(self):
        self.w.out.clear()
        self.w.addLine('Waiting for connection ...')
        QTimer.singleShot(reconnectTimeout*1000, self.start)

    def start(self):
        self.w.addLine('Start')
        self.process.start(cmd)

    def toOutput(self):
        output = self.process.readAll()
        if not isinstance(output, str):
            if sys.version_info[0] < 3:
                output = str(output)
            else:
                output = str(output)
        output = output.strip()
        if output:
            self.w.addLine('\n'+output)

    def trayIconActivated(self, reason):
        if reason == QSystemTrayIcon.Context:
            self.openMenu()
        elif reason == QSystemTrayIcon.Trigger:
            self.w.show()

    def openMenu(self):
        m = QMenu()
        m.addAction(QAction('Quit', self, triggered=self.quit))
        m.exec_(QCursor.pos())

    def quit(self):
        os.system('taskkill /f /im afrender.exe')
        self.process.kill()
        sys.exit()

class consoleClass(QWidget):
    def __init__(self, par):
        super(consoleClass, self).__init__()
        self.setWindowIcon(QIcon(icon))
        self.setWindowTitle('CGRU Tray')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.ly = QVBoxLayout(self)
        self.setLayout(self.ly)
        self.out = QTextBrowser(self)
        self.ly.addWidget(self.out)
        self.resize(500,300)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def addLine(self, line):
        self.out.append(line)

global app
def stop():
    global app
    app.quit()

if __name__ == '__main__':
    app = QApplication([])
    myapp = afTrayClass()
    app.exec_()
