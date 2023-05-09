from threading import Thread
import time
from datetime import datetime
from model import DeviceModel, TagModel, DashboardTag, BatchModel
import json

starttime = time.time()
from pycomm3 import LogixDriver


class Rockwell(Thread):

    def get_plcData(self):

        while True:

            # try:
            dashboardList = DashboardTag().find_all_Dashboard()
            print("daaa", dashboardList)
            for k in dashboardList:
                dashboard_id = k[0]
                cool_run_bit = k[2]
                dashboard_name = k[3]
                heat_run_bit = k[4]
                plc_id = k[5]

                # Devce Data by plcId
                deviceData = DeviceModel().find_device_by_id(plc_id)

                dashboard_type = deviceData[1]
                plc_ip = deviceData[7]
                plc_type_name = deviceData[11]
                plc_status = deviceData[10]

                # try:
                heattagData = TagModel().find_by_tag_id(heat_run_bit)
                heatdatatype = heattagData[1]
                heatplc_id = heattagData[2]
                heatstatus = heattagData[3]
                heattag_address = heattagData[4]

                cooltagData = TagModel().find_by_tag_id(cool_run_bit)
                cooldatatype = cooltagData[1]
                coolplc_id = cooltagData[2]
                coolstatus = cooltagData[3]
                cooltag_address = cooltagData[4]

                # with LogixDriver(plc_ip) as plc:
                # heatingStaus = plc.read(heattag_address)
                # CoolingStatus = plc.read(cooltag_address)
                configFilePath = 'F:\\amns\\satatus.json'
                f = open(configFilePath)
                data = json.load(f)
                print("ddd",data)
                heatingStaus = data['heatingStaus']
                CoolingStatus = data['CoolingStatus']

                now = datetime.now()
                HeatingProcess = 'Heating'
                CoolingProcess = 'Cooling'

                print("Batch Process Running")
                if (heatingStaus == 'True'):
                    heating_batch_count = BatchModel().find_by_batch_name_and_process_and_dashboardid(dashboard_id,
                                                                                                      str(now.strftime(
                                                                                                          "%m-%Y")) + "_" + dashboard_name,
                                                                                                      HeatingProcess)
                    if (len(heating_batch_count) == 0):
                        batchcount = 1
                        batchname = now.strftime("%m-%Y") + "_" + dashboard_name + "_" + str(batchcount)
                        BatchModel().insert(batchname, dashboard_id, now, None, HeatingProcess)
                    else:
                        if (len(heating_batch_count) != 0):
                            # here check heating process last batch end time if it none it means yet last batch is not completed else create new batch
                            endtime = heating_batch_count[len(heating_batch_count) - 1][4]
                            if (endtime == None):
                                print("noting")
                            else:
                                batchcount = len(heating_batch_count) + 1
                                batchname = now.strftime("%m-%Y") + "_" + dashboard_name + "_" + str(batchcount)
                                BatchModel().insert(batchname, dashboard_id, now, None, HeatingProcess)
                else:
                    # if heating is false means batch complete which batch complete last batch which running
                    heating_batch_count = BatchModel().find_last_heatingprocess(dashboard_id,
                                                                                HeatingProcess)

                    # print("heating_batch_count", heating_batch_count)
                    # get heating data in desc order so we get last heating process data if it end time none so update it
                    if (len(heating_batch_count) != 0):
                        endtime = heating_batch_count[0][4]
                        if (endtime == None):
                            BatchModel().update(heating_batch_count[0][1], dashboard_id,
                                                now, HeatingProcess)

                if (CoolingStatus == 'True'):
                    # here check list of hetaing process desc order
                    heating_batch_count = BatchModel().find_last_heatingprocess(dashboard_id,
                                                                                HeatingProcess)
                    if (len(heating_batch_count) != 0):
                        # if heating data is not zero means any heating entry available get batch name
                        last_hetaing_batchName = heating_batch_count[0][1]

                        # using heating batch name dashboardId find is there any cooling process available
                        batchNameStatus = BatchModel().find_batchname_coolingprocess(dashboard_id,
                                                                                     last_hetaing_batchName,
                                                                                     CoolingProcess)

                        print("cooling_batch_count", batchNameStatus)

                        if (len(batchNameStatus) == 0):
                            # if no any entry of heating batchname wise cooling so do new entry for cooling as name heating
                            BatchModel().insert(last_hetaing_batchName, dashboard_id, now, None, CoolingProcess)

                else:
                    CoolingProcess_batch_count = BatchModel().find_last_heatingprocess(dashboard_id,
                                                                                       CoolingProcess)
                    print("CoolingProcess_batch_count", CoolingProcess_batch_count)
                    # check last enrty of cooling process is there any entry
                    if (len(CoolingProcess_batch_count) != 0):

                        endtime = CoolingProcess_batch_count[0][4]
                        # check last entry end time is none is none update it
                        if (endtime == None):
                            BatchModel().update(heating_batch_count[0][1], dashboard_id,
                                                now, CoolingProcess)

                time.sleep(1)
        # except:
        #     print("exxxx")
        #     self.get_plcData()

    def run(self) -> None:
        self.get_plcData()
