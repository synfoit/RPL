from threading import Thread
import time
from datetime import datetime
from model import DeviceModel, TagModel, FloatModel
starttime = time.time()
from pycomm3 import LogixDriver

class ComtinuousData(Thread):

    def get_plcData(self):

        while True:
            print("kriiiiiiiiiiiiiiiiiii")
            try:
                deviceList = DeviceModel().find_all_device()
                now = datetime.now()
                for i in deviceList:

                    dashboard_type=i[1]
                    plc_type_name = i[11]
                    plc_status = i[10]
                    plc_ip = i[7]
                    device_id = i[0]
                    if (plc_type_name == 'Rockwell PLC'):
                        tagList = TagModel().find_all_tag()


                        for j in tagList:
                            tag_id=j[0]
                            datatype=j[1]
                            plc_id= j[2]
                            status=j[3]
                            tag_address= j[4]
                            tag_name=j[5]
                            tag_type=j[6]


                            if (device_id == plc_id and status == True and tag_type == 'Auto'):

                                with LogixDriver(plc_ip) as plc:
                                    data = plc.read(tag_address)
                                    val = "%.2f" % round(data[1], 2)
                                    print("Continues Process Running",now)
                                    FloatModel().insert(now, tag_id, val)
                time.sleep(31)


            except:
                print("exxxx")
                self.get_plcData()


    def run(self) -> None:
        self.get_plcData()
