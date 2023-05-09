import socket

import servicemanager
import win32event
import win32service
import win32serviceutil

from batch_data import Rockwell


def hello_world():
    rl = Rockwell()
    rl.start()
    # cd=ComtinuousData()
    # cd.start()
    return 'Hello World'

class Pythonservice(win32serviceutil.ServiceFramework):


    _svc_name_ = 'PC-Service'
    _svc_display_name_ = 'PC-Service'
    _svc_description_ = 'Freindly Service'

    @classmethod
    def parse_command_line(cls):

        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):

        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):

        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):

        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        self.isrunning = True

    def stop(self):
       self.isrunning = False

    def main(self):
        hello_world()




if __name__ == '__main__':
    Pythonservice.parse_command_line()