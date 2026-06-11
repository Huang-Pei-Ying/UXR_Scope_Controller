import pyvisa
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk
import configparser
import os
from decimal import Decimal
import re
import time
import sys
import numpy as np
from PIL import Image
import random
import string

window_name= '[Keysight] UXR-Series Controller_v1.0.0'

# 第一個視窗取得scope id並開啟主視窗
def show_main_window(old_scope_ips):
    # 取得scope id
    selected_value = str_scope_ip.get()

    # 新增scope id
    if selected_value and selected_value not in old_scope_ips:
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(os.path.join(os.path.dirname(__file__), 'InitConfig_setup.ini'), encoding='utf-8',)
        config.set('Scope_IPs', f'IP_{len(old_scope_ips)-1}', selected_value)

        # 寫回ini
        with open(os.path.join(os.path.dirname(__file__), 'InitConfig_setup.ini'), 'w') as configfile:
            config.write(configfile)
        
    # 關閉第一個視窗
    id_window.destroy()
    
    # 創建主視窗
    main_window(scope_ip= selected_value)
    

# =====================================================================================================================================================
def main_window(scope_ip):

    def initialize():
        config_initial = configparser.ConfigParser()
        config_initial.optionxform = str
        config_initial.read(os.path.join(os.path.dirname(__file__), 'InitConfig_setup.ini'), encoding='UTF-8',)

        # RealTimeSourceChannel = config_initial['Real_Time_Eye_Wizard']['RealTimeSourceChannel']
        select_RealTimeFrequency = config_initial['Real_Time_Eye_Wizard_Selected_Values']['RealTimeFrequency']
        RealTimeSamplingRate = config_initial['Real_Time_Eye_Wizard_Selected_Values']['RealTimeSamplingRate']
        RealTimeMemoryDepth = config_initial['Real_Time_Eye_Wizard']['RealTimeMemoryDepth']

        MaskLocation = config_initial['Mask_Test']['ScopeLocation']
        MaskPath = config_initial['Mask_Test']['MaskPath']
        UICounts = config_initial['Mask_Test']['UICounts']
        StopType = config_initial['Mask_Test']['StopType']

        Dimension = config_initial['Histogram']['Dimension']
        TopLimit = config_initial['Histogram']['TopLimit']
        BottomLimit = config_initial['Histogram']['BottomLimit']
        LeftLimit = config_initial['Histogram']['LeftLimit']
        RightLimit = config_initial['Histogram']['RightLimit']

        select_VoltScale = config_initial['Real_Time_Config_Selected_Values']['VoltageScale']
        select_VoltOffset = config_initial['Real_Time_Config_Selected_Values']['VoltageOffset']
        TimebaseScale = config_initial['Real_Time_Config']['TimebaseScale']
        TimebaseOffset = config_initial['Real_Time_Config']['TimebaseOffset']
        TriggerChan = config_initial['Real_Time_Config']['TriggerChan']
        select_TriggerLevel = config_initial['Real_Time_Config_Selected_Values']['TriggerLevel']
        WfmIntensity = config_initial['Real_Time_Config']['WfmIntensity']
        LabelType = config_initial['Real_Time_Config']['LabelType']
        Label = config_initial['Real_Time_Config']['Label']

        ImageFolder = config_initial['Real_Time_Save_Image']['ImageFolder']
        ImageName = config_initial['Real_Time_Save_Image']['ImageName']
        SetupScopeLocation = config_initial['Real_Time_Setup_Files']['ScopeLocation']
        FileFolder = config_initial['Real_Time_Setup_Files']['FileFolder']
        SetupFileName = config_initial['Real_Time_Setup_Files']['SetupFileName']
        LoadLabel = config_initial['Real_Time_Setup_Files']['LoadLabel']

        # PCIeClockChannel = config_initial['PCIe_Clock_Config']['PCIeClockChannel']
        PCIeClockSamplingRate = config_initial['PCIe_Clock_Config_Selected_Values']['PCIeClockSamplingRate']
        # PCIeClockMemoryDepth = config_initial['PCIe_Clock_Config']['PCIeClockMemoryDepth']
        PCIeClockVoltageScale = config_initial['PCIe_Clock_Config_Selected_Values']['PCIeClockVoltageScale']
        PCIeClockVoltageOffset = config_initial['PCIe_Clock_Config_Selected_Values']['PCIeClockVoltageOffset']
        PCIeClockTimebaseScale = config_initial['PCIe_Clock_Config']['PCIeClockTimebaseScale']
        IsLPF = config_initial['PCIe_Clock_Config']['IsLPF']

        PCIeClockScopeLocation = config_initial['PCIe_Clock_SAve_and_Load']['PCIeClockScopeLocation']
        FileType = config_initial['PCIe_Clock_SAve_and_Load']['FileType']
        # PCFolder = config_initial['PCIe_Clock_SAve_and_Load']['PCFolder']
        ScopeFolder = config_initial['PCIe_Clock_SAve_and_Load']['ScopeFolder']
        FileName = config_initial['PCIe_Clock_SAve_and_Load']['FileName']

        # Real-time eye set value
        # str_channel.set(value= RealTimeSourceChannel)
        str_frequency.set(value= select_RealTimeFrequency)
        str_sampling_rate.set(value= RealTimeSamplingRate)
        str_memory_depth.set(value= RealTimeMemoryDepth)

        int_mask_location.set(value= int(MaskLocation))
        str_mask_path.set(value= MaskPath)
        str_ui_counts.set(value= UICounts)
        int_mask_stop_type.set(value= int(StopType))

        int_dimension.set(value= int(Dimension))
        str_top_limit.set(value= TopLimit)
        str_bottom_limit.set(value= BottomLimit)
        str_left_limit.set(value= LeftLimit)
        str_right_limit.set(value= RightLimit)

        str_voltage_scale.set(value= select_VoltScale)
        str_voltage_offset.set(value= select_VoltOffset)
        str_timebase_scale.set(value= TimebaseScale)
        str_timebase_offset.set(value= TimebaseOffset)
        str_trigger_channel.set(value= TriggerChan)
        str_trigger_level.set(value= select_TriggerLevel)
        str_wfm_intensity.set(value= WfmIntensity)
        int_label_type.set(value= LabelType)
        str_label_name.set(value= Label)

        str_save_img_pc_folder.set(value= ImageFolder)
        str_save_img_name.set(value= ImageName)
        int_setup_location.set(value= int(SetupScopeLocation))
        str_save_scope_folder.set(value= FileFolder)
        str_file_name.set(value= SetupFileName)
        boolvar_load_label.set(value= bool(LoadLabel))

        # PCIe clock set value
        # str_pcieclock_channel.set(value= PCIeClockChannel)
        str_pcieclock_samplingrate.set(value= PCIeClockSamplingRate)
        # str_pcieclock_memory_depth.set(value= PCIeClockMemoryDepth)
        str_pcieclock_voltage_scale.set(value= PCIeClockVoltageScale)
        str_pcieclock_voltage_offset.set(value= PCIeClockVoltageOffset)
        str_pcieclock_timebase_scale.set(value= PCIeClockTimebaseScale)
        boolvar_5G_LPF.set(value= bool(IsLPF))

        int_pcieclock_scope_location.set(value= int(PCIeClockScopeLocation))
        int_pcieclock_file_type.set(value= int(FileType))
        # str_pcieclock_pc_folder.set(value= PCFolder)
        str_pcieclock_scope_folder.set(value= ScopeFolder)
        str_pcieclock_file_name.set(value= FileName)

    class UXR:

        def __init__(self, scope_ip, visa_lib= r'C:\Windows\System32\visa64.dll'):
            rm = pyvisa.ResourceManager(visa_lib)
            # self.inst = rm.open_resource(f'TCPIP0::KEYSIGH-{scope_id}::inst0::INSTR')
            try:
                self.inst = rm.open_resource(f'TCPIP0::{scope_ip}::inst0::INSTR')
                self.inst.timeout = 6000
                idn = self.inst.query('*IDN?').strip()
                print(f'Connect successfully! / {idn}')
                time.sleep(0.1)
                # self.inst.write(f':ANALyze:AEDGes 0')
                # time.sleep(0.05)
            except:
                warning_root = tk.Tk()
                warning_root.withdraw()  # 隱藏主視窗
                connection_fail = messagebox.showinfo("Error", f"Connection Failed.")
                close_window()
                # sys.exit()
                
        ### Display Related ###
        def display_Chan(self, chan, bookmark, label_choose_type):
            res= self.inst.query(f':CHANnel{chan}:DISPlay?')
            time.sleep(0.05)
            if res == '1\n':
                self.inst.write(f':CHANnel{chan}:DISPlay OFF')
                time.sleep(0.05)
                try:
                    self.inst.write(f':DISPlay:BOOKmark{chan}:DELete')
                    time.sleep(0.05)
                except:
                    pass
            else:
                self.inst.write(f':CHANnel{chan}:DISPlay ON')
                time.sleep(0.05)
                self.add_bookmark(label_choose_type= label_choose_type,bookmark= bookmark, chan= chan)

        def get_display_channel(self):
            
            for channel in range(1, 5):
                query_value = self.inst.query(f':CHANnel{channel}:DISPlay?').rstrip('\n')
                time.sleep(0.1)
                if query_value == '1' or query_value == 'ON':
                    return channel
                else:
                    return False
            

        def intensity_check(self, intensity_value):
            self.inst.write(f'SYSTem:CONTrol "WaveformBrt -1 {intensity_value}"')
            time.sleep(0.05)


        ### Acquisition Related ###
        def sampling_rate_acquire(self, rate): # 科學記號
            self.inst.write(f':ACQuire:SRATe:ANALog {rate}')
            time.sleep(0.05)

        def memory_depth_acquire(self, points_value: int):
            self.inst.write(f':ACQuire:POINts:ANALog {points_value}')
            time.sleep(0.05)


        ### Scale Related ###
        def voltage_scale_check(self, voltage_scale): # 科學記號
            channel= self.get_display_channel()
            if channel == False:
                return
            self.inst.write(f':CHANnel{channel}:SCALe {voltage_scale}')
            time.sleep(0.05)

        def voltage_offset_check(self, voltage_offset): # 科學記號
            channel= self.get_display_channel()

            if channel == False:
                return

            self.inst.write(f':CHANnel{channel}:OFFSet {voltage_offset}')
            time.sleep(0.05)

        def timebase_position_check(self, timebase_position): # 科學記號
            self.inst.write(f':TIMebase:POSition {timebase_position}')
            time.sleep(0.05)

        def timebase_scale_check(self, timebase_scale): # 科學記號
            self.inst.write(f':TIMebase:SCALe {timebase_scale}')
            time.sleep(0.05)

        def trigger_check(self, trigger_channel, trigger_level):
            res= self.inst.query(f':CHANnel{trigger_channel}:DISPlay?')
            time.sleep(0.05)
            if not res == '1\n':
                self.inst.write(f':CHANnel{trigger_channel}:DISPlay ON')
                time.sleep(0.05)
            self.inst.write(f':TRIGger:EDGE:SOURce CHANnel{trigger_channel}')
            time.sleep(0.05)
            self.inst.write(f':TRIGger:LEVel CHANnel{trigger_channel},{trigger_level}')
            time.sleep(0.05)
            if not res == '1\n':
                self.inst.write(f':CHANnel{trigger_channel}:DISPlay OFF')
                time.sleep(0.05)


        ### Measurement Related ###
        def cdr_rate_measurement(self):
            channel= self.get_display_channel()

            if channel == False:
                return

            self.inst.write(f':MEASure:CDRRate CHANnel{channel}')
            time.sleep(0.1)
            
        def vpp_measurement(self):
            channel= self.get_display_channel()

            if channel == False:
                return
            self.inst.write(f':MEASure:VPP CHANnel{channel}')
            time.sleep(0.1)

        def eye_height_measurement(self):
            channel= self.get_display_channel()

            if channel == False:
                return

            self.inst.write(f':MEASure:CGRade:EHEight MEASured,CHANnel{channel}')
            time.sleep(0.1)

        def eye_width_measurement(self):
            channel= self.get_display_channel()

            if channel == False:
                return

            self.inst.write(f':MEASure:CGRade:EWIDth MEASured,CHANnel{channel}')
            time.sleep(0.1)

        def vih_measurement(self):
            channel= self.get_display_channel()

            if channel == False:
                return

            self.inst.write(f':MEASure:VTOP CHANnel{channel}')
            time.sleep(0.1)
            
        def vil_width_measurement(self):
            channel= self.get_display_channel()

            if channel == False:
                return

            self.inst.write(f':MEASure:VBASe CHANnel{channel}')
            time.sleep(0.1)


        ### Control Related ###
        def run(self):
            self.inst.write(':RUN')
            time.sleep(0.05)

        def stop(self):
            self.inst.write(':STOP')
            time.sleep(0.05)

        def single(self):
            self.inst.write(':SINGLE')
            time.sleep(0.05)

        def autoscale(self):
            self.inst.write(':AUToscale')
            time.sleep(0.05)

        def clear_diaplay(self):
            self.inst.write(':CDISplay')
            time.sleep(0.05)

        def default(self):
            self.inst.write(':SYSTem:PRESet DEFault')
            time.sleep(0.05)


        ### Trigger Related ###
        def trig_type(self):
            res= self.inst.query(f':TRIGger:SWEep?')
            time.sleep(0.05)
            if res == 'AUTO\n':
                self.inst.write(':TRIGger:SWEep TRIGgered')
                time.sleep(0.05)
            else:
                self.inst.write(':TRIGger:SWEep AUTO')
                time.sleep(0.05)
        

        ### Measurement Related (label) ###
        def delete_item(self):
            tuple_marker = (boolvar_marker_1, boolvar_marker_2, boolvar_marker_3, boolvar_marker_4, boolvar_marker_5, boolvar_marker_6, 
                            # boolvar_marker_7, boolvar_marker_8, boolvar_marker_9, boolvar_marker_10, boolvar_marker_11, boolvar_marker_12, 
                            )
            for i, boolvar in enumerate(tuple_marker):
                if boolvar.get():
                    self.inst.write(f'MEASurement{i+1}:CLEar')
                    time.sleep(0.05)

        def add_label(self, label):
            channel= self.get_display_channel()

            if channel == False:
                return

            if label == '':
                self.inst.write(f':DISPlay:LABel OFF')
                time.sleep(0.05)
            else:
                self.inst.write(f':DISPlay:LABel ON')
                time.sleep(0.05)
                self.inst.write(f':CHANnel{channel}:LABel "{label}"')
                time.sleep(0.05)

        def add_bookmark(self, label_choose_type, bookmark):

            channel= self.get_display_channel()

            if channel == False:
                return

            if label_choose_type == 1:
                self.inst.write(f':DISPlay:BOOKmark:DELete:ALL')
                time.sleep(0.05)
                self.add_label(label= bookmark)
                return
            else:
                self.inst.write(f':DISPlay:LABel OFF')
                time.sleep(0.05)
                if bookmark == '':
                    self.inst.write(f':DISPlay:BOOKmark{channel}:DELete')

                else:
                    try:
                        is_meas_area= self.inst.query(':MEASure:NAME? MEAS1') 
                        time.sleep(0.05)
                    except:
                        is_meas_area= 0
                    is_marker_area= self.inst.query(':MARKer1:ENABle?') 
                    time.sleep(0.05)
                    if not is_meas_area == '"no meas"\n' or is_marker_area == '1\n':
                        interval= 5
                    else:
                        interval= 3.5
                        
                    bookmark_display_list= []
                    count= 0
                    self.inst.write(f':DISPlay:BOOKmark{channel}:DELete')
                    time.sleep(0.05)
                    self.inst.write(f':DISPlay:BOOKmark{channel}:SET NONE,"{bookmark}",CHANnel{channel},"",1')
                    time.sleep(0.05)
                    self.inst.write(f':DISPlay:BOOKmark{channel}:XPOSition {0.01}')
                    time.sleep(0.05)
                    bookmark_display_list.append(count)
                    self.inst.write(f':DISPlay:BOOKmark{channel}:YPOSition {2+interval*count}E-02')
                    time.sleep(0.05)

        def delete_label(self):
            self.inst.write(f':DISPlay:LABel OFF')
            time.sleep(0.05)

        def delete_bookmark(self, choose_type):

            channel= self.get_display_channel()

            if channel == False:
                return

            if choose_type == 1:
                self.inst.write(f':DISPlay:LABel OFF')
                time.sleep(0.05)
            else:
                self.inst.write(f':DISPlay:BOOKmark{channel}:DELete')
                time.sleep(0.05)

        def add_marker(self):
            tuple_marker = (boolvar_marker_1, boolvar_marker_2, boolvar_marker_3, boolvar_marker_4, boolvar_marker_5, boolvar_marker_6, 
                            # boolvar_marker_7, boolvar_marker_8, boolvar_marker_9, boolvar_marker_10, boolvar_marker_11, boolvar_marker_12, 
                            )
            multe_color_list= [
                '#FFFF8A00',  # 橘
                '#FFFFE4C4',  # 膚
                '#FFFFA8BD',  # 粉
                '#FF99DAE8',  # 淡藍
                '#FFC0C0C0',  # 灰
                '#FF8FBC8F'  # 灰綠
            ]
            single_color_list= [
                '#FFFF8A00',  # 橘
                '#FFFF8A00',  # 橘
                '#FFFF8A00',  # 橘
                '#FFFF8A00',  # 橘
                '#FFFF8A00',  # 橘
                '#FFFF8A00'  # 橘
            ]

            if boolver_marker_color.get() == True:
                color_list= multe_color_list
            else:
                color_list= single_color_list

            for i, boolvar in enumerate(tuple_marker):
                self.inst.write(f':MARKer:MEASurement:MEASurement MEASurement{i+1},OFF')
                time.sleep(0.05)

            c=0
            for i, boolvar in enumerate(tuple_marker):
                if boolvar.get():
                    self.inst.write(f':MARKer:MEASurement:MEASurement MEASurement{i+1},ON')
                    time.sleep(0.05)
                    self.inst.write(f':MARKer{2*c+1}:COLor "{color_list[c]}"')
                    time.sleep(0.05)
                    self.inst.write(f':MARKer{2*c+2}:COLor "{color_list[c]}"')
                    time.sleep(0.05)
                    c+=1
                         
        def delete_marker(self):
            tuple_marker = (boolvar_marker_1, boolvar_marker_2, boolvar_marker_3, boolvar_marker_4, boolvar_marker_5, boolvar_marker_6, 
                            # boolvar_marker_7, boolvar_marker_8, boolvar_marker_9, boolvar_marker_10, boolvar_marker_11, boolvar_marker_12, 
                            )
        
            for i, boolvar in enumerate(tuple_marker):
                if boolvar.get():
                    self.inst.write(f':MARKer:MEASurement:MEASurement MEASurement{i+1},OFF')
                    time.sleep(0.05)


        ### Save Related ###
        def load_setup(self, folder, setup_name, label_choose_type, file_path_choice):

            if file_path_choice == 2:
                total_folder_path = folder
            else:
                total_folder_path = f"C:/Users/Administrator/Desktop/{folder}"
            self.inst.write(f':DISK:LOAD "{total_folder_path}/{setup_name}.set"')
            time.sleep(0.05)
            if boolvar_load_label.get() == True:
                self.add_bookmark(label_choose_type= label_choose_type, bookmark= str_label_name.get().rstrip('\n'))
        
        def save_image_pc(self, pc_folder, file_name):
            screen_data = np.array(self.inst.query_binary_values(":DISPlay:DATA? PNG", datatype = 's', container = bytes))
            time.sleep(0.05)

            if not os.path.exists(pc_folder):
                ask_root = tk.Tk()
                ask_root.withdraw()  # 隱藏主視窗
                ask_result = messagebox.askyesno("Warning", f"資料夾不存在，是否新增？")
                ask_root.destroy()
                
                if not ask_result:
                    ask_root = tk.Tk()
                    ask_root.withdraw()  # 隱藏主視窗
                    messagebox.showinfo("Warning", f'檔案未儲存')
                    # print("檔案未保存。")
                    return     
                os.mkdir(pc_folder) 

            if os.path.exists(f"{pc_folder}/{file_name}.png"):
                ask_root = tk.Tk()
                ask_root.withdraw()  # 隱藏主視窗
                ask_result = messagebox.askyesno("Warning", f"檔案已經存在，是否覆蓋？")
                ask_root.destroy()
                
                if not ask_result:
                    # print("檔案未保存。")
                    ask_root = tk.Tk()
                    ask_root.withdraw()  # 隱藏主視窗
                    messagebox.showinfo("Warning", f'檔案未儲存')
                    return     
            
            temp_img_name= ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            temp_folder= fr'{os.path.dirname(__file__)}/Temp'
            if not os.path.exists(temp_folder):
                os.mkdir(temp_folder) 
                
            f_img = open(f"{temp_folder}/{temp_img_name}.png", "wb")
            f_img.write(bytearray(screen_data))
            f_img.close()

            rgba_to_rgb_composite(f"{temp_folder}/{temp_img_name}.png", f"{pc_folder}/{file_name}.png", background=(0,0,0))

        def save_setup_file_scope(self, folder, current_file_name, path_choice, file_type_choice):
            # 清空狀態
            self.inst.write('*CLS')
            time.sleep(0.05)
            # error messenge
                # 113 This directory is not valid.
                # -256 File name not found
                # -257 File name error
                # -410 Query INTERRUPTED
                # -420 Query UNTERMINATED
                # 0 No error

            if path_choice == 2:
                folder_total_path = folder
            else:
                folder_total_path = f"C:/Users/Administrator/Desktop/{folder}"

            # 資料夾是否存在
            self.inst.query(f':DISK:DIRectory? "{folder_total_path}"')
            time.sleep(0.05)
            error_messenge=self.inst.query(f':SYSTem:ERRor?')
            time.sleep(0.05)
            # print(error_messenge)
            if error_messenge == '-256\n' or error_messenge == '113\n' or error_messenge == '-257\n':
                ask_scp_root = tk.Tk()
                ask_scp_root.withdraw()  # 隱藏主視窗
                ask_scp_result = messagebox.askyesno("Warning", f"資料夾不存在，是否新增？")
                ask_scp_root.destroy()
                
                if not ask_scp_result:
                    ask_scp_root = tk.Tk()
                    ask_scp_root.withdraw()  # 隱藏主視窗
                    messagebox.showinfo("Warning", f'檔案未儲存')
                    # print("檔案未保存。")
                    return     
                # 新建資料夾
                folder_total_path= folder_total_path.replace("/", "\\")
                # print(folder_total_path)
                split_folder_list= folder_total_path.split('\\')

                folder= split_folder_list[0]
                for split in split_folder_list[1:]:
                    folder= f'{folder}\\{split}'
                    self.inst.query(f':DISK:DIRectory? "{folder}"')
                    time.sleep(0.05)
                    response= self.inst.query(f':SYSTem:ERRor?')
                    time.sleep(0.05)
                    # print(response)
                    if response == '-256\n' or response == '113\n' or response == '-257\n':
                        self.inst.write(f':DISK:MDIRectory "{folder}"')
                        time.sleep(0.05)

            # 資料夾全部內容
            folder_content= self.inst.query(f':DISK:DIRectory? "{folder_total_path}"')
            time.sleep(0.05)

            if file_type_choice == 1:
                channel= self.get_display_channel()

                # if channel == False:
                #     return

                # 使用正則表達式來匹配所有 .bin 檔案名稱
                files = re.findall(r'\b[\w-]+\.(?:bin)\b', folder_content)
                ext= 'bin'
                command= f':DISK:SAVE:WAVeform CHANnel{channel},"{folder_total_path}/{current_file_name}",BIN,OFF'
            else:
                #   使用正則表達式來匹配所有 .set 檔案名稱
                files = re.findall(r'\b[\w-]+\.(?:set)\b', folder_content)
                ext= 'set'
                command= f':DISK:SAVE:SETup "{folder_total_path}/{current_file_name}"'

            for file_name in files:
                if f'{current_file_name}.{ext}' == file_name:
                    ask_scp_root = tk.Tk()
                    ask_scp_root.withdraw()  # 隱藏主視窗
                    ask_scp_result = messagebox.askyesno("Warning", f"檔案已經存在，是否覆蓋？")
                    ask_scp_root.destroy()
                    
                    if not ask_scp_result:
                        # print("檔案未保存。")
                        ask_scp_root = tk.Tk()
                        ask_scp_root.withdraw()  # 隱藏主視窗
                        messagebox.showinfo("Warning", f'檔案未儲存')
                        return     

            self.inst.write(command)
            time.sleep(0.05)


        ### Result Related ###
        def get_results(self):
            meas_name= ['', '', '', '', '', '']
            result1= ['', '', '', '', '', '']
            result2= ['', '', '', '', '', '']
            all_results= self.inst.query(f':MEASure:RESults?')
            time.sleep(0.05)
            for index, value in enumerate(all_results.split(',')):
                if divmod(index, 7)[1] == 0:
                    try:
                        meas_name[divmod(index, 7)[0]]= value
                    except:
                        # l_meas_name_1.config(text=f'484超過3個??')
                        continue
                    if value[0] == 'V':  # 0: Voltage, 1: Time, 2: Slew Rate, 3: Frequency, 4: Duty cycle
                        measurement_type = 0 
                    elif 'Slew Rate' in value:
                        measurement_type = 2
                    elif 'Freq' in value:
                        measurement_type = 3
                    elif 'Duty cycle' in value:
                        measurement_type = 4
                    elif value == '\n':
                        meas_name[divmod(index, 7)[0]] = ''
                        continue
                    else:
                        measurement_type = 1
                
                if intvar_result_type.get() == 1:  # 選擇Mean Value
                    if divmod(index, 7)[1] == 4:
                        if measurement_type == 0:
                            final_result_1= self.judge_volt_unit(value= value)
                            final_result_2= ''
                        elif measurement_type == 1:
                            slew= False
                            final_result_1= self.judge_time_unit(value= value, slew= slew)
                            final_result_2= ''
                        elif measurement_type == 2:
                            slew= True
                            final_result_1= self.judge_time_unit(value= value, slew= slew)
                            final_result_2= ''
                        elif measurement_type == 3:
                            final_result_1= self.judge_freq_unit(value= value)
                            final_result_2= ''
                        elif measurement_type == 4:
                            final_result_1 = f"{float(value):.3f}"+' %'
                            final_result_2= ''

                        try:
                            result1[divmod(index, 7)[0]]= final_result_1
                            result2[divmod(index, 7)[0]]= final_result_2
                        except:
                            continue

                elif intvar_result_type.get() == 2:  # 選擇Min & Max Value
                    if divmod(index, 7)[1] == 2:
                        if measurement_type == 0:
                            final_result_1= self.judge_volt_unit(value= value)
                        elif measurement_type == 1:
                            slew= False
                            final_result_1= self.judge_time_unit(value= value, slew= slew)
                        elif measurement_type == 2:
                            slew= True
                            final_result_1= self.judge_time_unit(value= value, slew= slew)
                        elif measurement_type == 3:
                            final_result_1= self.judge_freq_unit(value= value)
                        elif measurement_type == 4:
                            final_result_1 = f"{float(value):.3f}"+' %'

                        try:
                            result1[divmod(index, 7)[0]]= final_result_1
                        except:
                            continue

                    if divmod(index, 7)[1] == 3:
                        if measurement_type == 0:
                            final_result_2= self.judge_volt_unit(value= value)
                        elif measurement_type == 1:
                            slew= False
                            final_result_2= self.judge_time_unit(value= value, slew= slew)
                        elif measurement_type == 2:
                            slew= True
                            final_result_2= self.judge_time_unit(value= value, slew= slew)
                        elif measurement_type == 3:
                            final_result_2= self.judge_freq_unit(value= value)
                        elif measurement_type == 4:
                            final_result_2 = f"{float(value):.3f}"+' %'

                        try:
                            result2[divmod(index, 7)[0]]= final_result_2
                        except:
                            continue

            label_meas_name_1.config(text=f'{meas_name[0]}')
            text_result1_1.config(state=tk.NORMAL)  # 先啟用Text小部件的編輯狀態
            text_result1_1.delete(1.0, tk.END)  # 清空當前內容
            text_result1_1.insert(tk.END, f"{result1[0]}")
            text_result1_1.config(state=tk.DISABLED)  # 設置為只讀狀態
            text_result2_1.config(state=tk.NORMAL)  # 先啟用Text小部件的編輯狀態
            text_result2_1.delete(1.0, tk.END)  # 清空當前內容
            text_result2_1.insert(tk.END, f"{result2[0]}")
            text_result2_1.config(state=tk.DISABLED)  # 設置為只讀狀態

            label_meas_name_2.config(text=f'{meas_name[1]}')
            text_result1_2.config(state=tk.NORMAL)  # 先啟用Text小部件的編輯狀態
            text_result1_2.delete(1.0, tk.END)  # 清空當前內容
            text_result1_2.insert(tk.END, f"{result1[1]}")
            text_result1_2.config(state=tk.DISABLED)  # 設置為只讀狀態
            text_result2_2.config(state=tk.NORMAL)  # 先啟用Text小部件的編輯狀態
            text_result2_2.delete(1.0, tk.END)  # 清空當前內容
            text_result2_2.insert(tk.END, f"{result2[1]}")
            text_result2_2.config(state=tk.DISABLED)  # 設置為只讀狀態
            
            label_meas_name_3.config(text=f'{meas_name[2]}')
            text_result1_3.config(state=tk.NORMAL)  # 先啟用Text小部件的編輯狀態
            text_result1_3.delete(1.0, tk.END)  # 清空當前內容
            text_result1_3.insert(tk.END, f"{result1[2]}")
            text_result1_3.config(state=tk.DISABLED)  # 設置為只讀狀態
            text_result2_3.config(state=tk.NORMAL)  # 先啟用Text小部件的編輯狀態
            text_result2_3.delete(1.0, tk.END)  # 清空當前內容
            text_result2_3.insert(tk.END, f"{result2[2]}")
            text_result2_3.config(state=tk.DISABLED)  # 設置為只讀狀態
            
            label_meas_name_4.config(text=f'{meas_name[3]}')
            text_result1_4.config(state=tk.NORMAL)  # 先啟用Text小部件的編輯狀態
            text_result1_4.delete(1.0, tk.END)  # 清空當前內容
            text_result1_4.insert(tk.END, f"{result1[3]}")
            text_result1_4.config(state=tk.DISABLED)  # 設置為只讀狀態
            text_result2_4.config(state=tk.NORMAL)  # 先啟用Text小部件的編輯狀態
            text_result2_4.delete(1.0, tk.END)  # 清空當前內容
            text_result2_4.insert(tk.END, f"{result2[3]}")
            text_result2_4.config(state=tk.DISABLED)  # 設置為只讀狀態
            
            label_meas_name_5.config(text=f'{meas_name[4]}')
            text_result1_5.config(state=tk.NORMAL)  # 先啟用Text小部件的編輯狀態
            text_result1_5.delete(1.0, tk.END)  # 清空當前內容
            text_result1_5.insert(tk.END, f"{result1[4]}")
            text_result1_5.config(state=tk.DISABLED)  # 設置為只讀狀態
            text_result2_5.config(state=tk.NORMAL)  # 先啟用Text小部件的編輯狀態
            text_result2_5.delete(1.0, tk.END)  # 清空當前內容
            text_result2_5.insert(tk.END, f"{result2[4]}")
            text_result2_5.config(state=tk.DISABLED)  # 設置為只讀狀態
            
            label_meas_name_6.config(text=f'{meas_name[5]}')
            text_result1_6.config(state=tk.NORMAL)  # 先啟用Text小部件的編輯狀態
            text_result1_6.delete(1.0, tk.END)  # 清空當前內容
            text_result1_6.insert(tk.END, f"{result1[5]}")
            text_result1_6.config(state=tk.DISABLED)  # 設置為只讀狀態
            text_result2_6.config(state=tk.NORMAL)  # 先啟用Text小部件的編輯狀態
            text_result2_6.delete(1.0, tk.END)  # 清空當前內容
            text_result2_6.insert(tk.END, f"{result2[5]}")
            text_result2_6.config(state=tk.DISABLED)  # 設置為只讀狀態


        ### Unit Related ###
        def judge_time_unit(self, value, slew):
            pattern = r'([+-]?\d*\.?\d+)E([+-]?\d+)'
            match = re.search(pattern, value)
            # 提取基數和指數
            base = float(match.group(1))
            exponent = int(match.group(2))
            if slew:
                if exponent == 3:
                    return f"{base} V/ms"
                elif exponent == 4:
                    return f"{base * 10} V/ms"
                elif exponent == 5:
                    return f"{base * 100} V/ms"
                elif exponent == 6:
                    return f"{base} V/us"
                elif exponent == 7:
                    return f"{base * 10} V/us"
                elif exponent == 8:
                    return f"{base * 100} V/us"
                elif exponent == 9:
                    return f"{base} V/ns"
                elif exponent == 10:
                    return f"{base * 10} V/ns"
                elif exponent == 11:
                    return f"{base * 100} V/ns"
                elif exponent == 12:
                    return f"{base} V/ps"
                elif exponent == 13:
                    return f"{base * 10} V/ps"
                elif exponent == 14:
                    return f"{base * 100} V/ps"
                elif exponent == 15:
                    return f"{base} V/fs"
                elif exponent == 16:
                    return f"{base * 10} V/fs"
                elif exponent == 17:
                    return f"{base * 100} V/fs"
                else:
                    # 如果指數不在指定的範圍内，返回原始字串
                    return f"{base} V/s"
            else:
                if exponent == -9:
                    return f"{base} ns"
                elif exponent == -8:
                    return f"{base * 10} ns"
                elif exponent == -7:
                    return f"{base * 100} ns"
                elif exponent == -6:
                    return f"{base} us"
                elif exponent == -5:
                    return f"{base * 10} us"
                elif exponent == -4:
                    return f"{base * 100} us"
                elif exponent == -3:
                    return f"{base} ms"
                elif exponent == -2:
                    return f"{base * 10} ms"
                elif exponent == -1:
                    return f"{base * 100} ms"
                elif exponent == -12:
                    return f"{base} ps"
                elif exponent == -11:
                    return f"{base * 10} ps"
                elif exponent == -10:
                    return f"{base * 100} ps"
                elif exponent == -15:
                    return f"{base} fs"
                elif exponent == -14:
                    return f"{base * 10} fs"
                elif exponent == -13:
                    return f"{base * 100} fs"
                else:
                    # 如果指數不在指定的範圍内，返回原始字串
                    return f'{base} s'
                
        def judge_volt_unit(self, value):
            pattern = r'([+-]?\d*\.?\d+)E([+-]?\d+)'
            match = re.search(pattern, value)
            # 提取基數和指數
            base = float(match.group(1))
            exponent = int(match.group(2))
            # 基于不同的指数值进行不同的转换
            if exponent == -3:
                return f"{base} mV"
            elif exponent == -2:
                return f"{base * 10} mV"
            elif exponent == -1:
                return f"{base * 100} mV"
            else:
                # 如果指数不在指定的范围内，返回原始文本
                return f"{base} V"

        def judge_freq_unit(self, value):
            pattern = r'([+-]?\d*\.?\d+)E([+-]?\d+)'
            match = re.search(pattern, value)
            # 提取基數和指數
            base = float(match.group(1))
            exponent = int(match.group(2))
            # 基于不同的指数值进行不同的转换
            if exponent == 9:
                return f"{base} GHz"
            elif exponent == 8:
                return f"{base * 100} MHz"
            elif exponent == 7:
                return f"{base * 10} MHz"
            elif exponent == 6:
                return f"{base} MHz"
            elif exponent == 5:
                return f"{base * 100} kHz"
            elif exponent == 4:
                return f"{base * 10} kHz"
            elif exponent == 3:
                return f"{base} kHz"
            elif exponent == 2:
                return f"{base * 100} Hz"
            elif exponent == 1:
                return f"{base * 10} Hz"
            else:
                # 如果指数不在指定的范围内，返回原始文本
                return f"{base} Hz"


        ### Real-time eye ###
        def setup_real_time_eye(self, sampling_rate, acquire_points, frequency):
            
            channel= self.get_display_channel()

            if channel == False:
                return

            self.inst.write(f':AUToscale')
            time.sleep(0.05)

            if sampling_rate == '':
                sampling_rate = '256E+09'
            self.sampling_rate_acquire(rate= sampling_rate)
            # self.inst.write(f':ACQuire:SRATe:ANALog {sampling_rate}')
            # time.sleep(0.05)
            if acquire_points == '':
                acquire_points = '1E+06'
            self.memory_depth_acquire(points_value= acquire_points)
            # self.inst.write(f':ACQuire:POINts:ANALog {acquire_points}')
            # time.sleep(0.05)
            self.inst.write(f':MEASure:THResholds:GENeral:METHod CHANnel{channel},HYSTeresis')
            time.sleep(0.1)
            self.inst.write(f':MEASure:THResholds:GENAUTO CHANnel{channel}')
            time.sleep(0.1)
            self.inst.write(f':MTESt:FOLDing ON,CHANnel{channel}')
            time.sleep(0.1)
            # self.inst.write(f':ANALyze:CLOCk ON,CHANnel1')
            # time.sleep(0.1)
            self.inst.write(f':MEASure:CLOCk:METHod SOPLL,{frequency}')
            time.sleep(0.1)


        ### mask test ###
        def setup_mask_test(self, mask_path, mask_name, ui_counts):

            channel= self.get_display_channel()

            if channel == False:
                return

            self.inst.write(f':MTESt:FOLDing ON,CHANnel{channel}')
            time.sleep(0.1)
            self.inst.write(f':MTESt1:ENABle ON')
            time.sleep(0.1)

            if int_mask_location.get() == 1:
                self.inst.write(fr':MTESt1:LOAD "C:\Users\Administrator\Desktop\{mask_path}\{mask_name}.msk"')
                time.sleep(0.1)
            else:
                self.inst.write(fr':MTESt1:LOAD "{mask_path}\{mask_name}.msk"')
                time.sleep(0.1)
            
            if int_mask_stop_type.get() == 1:
                self.inst.write(f':MTESt:RUMode WAVeforms,{ui_counts}')
                time.sleep(0.1)
            elif int_mask_stop_type.get() == 2:
                self.inst.write(f':MTESt:RUMode:SOFailure 1')
                time.sleep(0.1)
            elif int_mask_stop_type.get() == 3:
                self.inst.write(f':MTESt:RUMode FORever')
                time.sleep(0.1)

            self.inst.write(f':MTESt:STOP')
            time.sleep(0.1)

            # self.inst.write(f':MTESt1:SCALe:DRAW ON')
            # time.sleep(0.1)
            # self.inst.write(f':MTESt1:SCALe:X1 ')
            # time.sleep(0.1)

        def run_mask_test(self):
            self.inst.write(f':MTESt:STARt')

        def stop_mask_test(self):
            self.inst.write(f':MTESt:STOP')
            time.sleep(0.1)

        def disable_mask_test(self):
            self.inst.write(f':MTESt1:ENABle OFF')
            time.sleep(0.1)


        ### histogram test ###
        def setup_histogram(self, top_limit, bottom_limit, left_limit, right_limit):

            channel= self.get_display_channel()

            if channel == False:
                return

            self.inst.write(f':HISTogram:WINDow:DEFault')
            time.sleep(0.1)
            self.inst.write(f':HISTogram:AXIS HORizontal')
            time.sleep(0.1)
            self.inst.write(f':HISTogram:MODE WAVeforms')
            time.sleep(0.1)
            self.inst.write(f':HISTogram:WINDow:SOURce CHANnel{channel}')
            time.sleep(0.1)

            self.inst.write(f':HISTogram:WINDow:LLIMit {left_limit}')
            time.sleep(0.1)
            self.inst.write(f':HISTogram:WINDow:RLIMit {right_limit}')
            time.sleep(0.1)
            self.inst.write(f':HISTogram:WINDow:BLIMit {bottom_limit}')
            time.sleep(0.1)
            self.inst.write(f':HISTogram:WINDow:TLIMit {top_limit}')
            time.sleep(0.1)

        def disable_histogram(self):
            self.inst.write(f':HISTogram:MODE OFF')
            time.sleep(0.1)


        ### pcie clock test ###
        def setup_pcieclock_test(self, sampling_rate, time_required, is_low_pass_filter, voltage_scale):

            self.sampling_rate_acquire(rate= sampling_rate)
            # self.inst.write(f':ACQuire:SRATe:ANALog 2.56E+11')
            # time.sleep(0.05)
            acquire_points= round(float(sampling_rate)*float(time_required))
            self.memory_depth_acquire(points_value= acquire_points)
            # self.inst.write(f':ACQuire:POINts:ANALog {acquire_points}')
            # time.sleep(0.05)
            self.inst.write(f':ACQuire:INTerpolate OFF')
            time.sleep(0.05)

            channel= self.get_display_channel()
            if channel == False:
                return

            self.inst.write(f':CHANnel{channel}:ISIM:BWLimit ON')
            time.sleep(0.05)
            self.inst.write(f':CHANnel{channel}:ISIM:BWLimit:TYPE WALL')
            time.sleep(0.05)
            if is_low_pass_filter:
                self.inst.write(f':CHANnel{channel}:ISIM:BANDwidth 5000000000')
                time.sleep(0.05)

            self.inst.write(f':CHANnel{channel}:SCALe {voltage_scale}')
            time.sleep(0.05)

            self.inst.write(f':TIMebase:SCALe {time_required}')
            time.sleep(0.05)


     ### Close Window Related ###
    def close_window():
        if messagebox.askyesno('Message', 'Exit?'):
            config = configparser.ConfigParser()
            config.optionxform = str
            config.read( os.path.join(os.path.dirname(__file__), 'InitConfig_setup.ini'), encoding='utf-8',)
            
            # config.set('Real_Time_Eye_Wizard', 'RealTimeSourceChannel', str_channel.get())
            config.set('Real_Time_Eye_Wizard_Selected_Values', 'RealTimeFrequency', str_frequency.get())
            config.set('Real_Time_Eye_Wizard_Selected_Values', 'RealTimeSamplingRate', str_sampling_rate.get())
            config.set('Real_Time_Eye_Wizard', 'RealTimeMemoryDepth', str_memory_depth.get())

            config.set('Mask_Test', 'ScopeLocation', str(int_mask_location.get()))
            config.set('Mask_Test', 'MaskPath', str_mask_path.get())
            config.set('Mask_Test', 'UICounts', str_ui_counts.get())
            config.set('Mask_Test', 'StopType', str(int_mask_stop_type.get()))

            config.set('Histogram', 'Dimension', str(int_dimension.get()))
            config.set('Histogram', 'TopLimit', str_top_limit.get())
            config.set('Histogram', 'BottomLimit', str_bottom_limit.get())
            config.set('Histogram', 'LeftLimit', str_left_limit.get())
            config.set('Histogram', 'RightLimit', str_right_limit.get())

            config.set('Real_Time_Config_Selected_Values', 'VoltageScale', str_voltage_scale.get())
            config.set('Real_Time_Config_Selected_Values', 'VoltageOffset', str_voltage_offset.get())
            config.set('Real_Time_Config', 'TimebaseScale', str_timebase_scale.get())
            config.set('Real_Time_Config', 'TimebaseOffset', str_timebase_offset.get())
            config.set('Real_Time_Config', 'TriggerChan', str_trigger_channel.get())
            config.set('Real_Time_Config_Selected_Values', 'TriggerLevel', str_trigger_level.get())
            config.set('Real_Time_Config', 'WfmIntensity', str_wfm_intensity.get())
            config.set('Real_Time_Config', 'LabelType', str(int_label_type.get()))
            config.set('Real_Time_Config', 'Label', str_label_name.get())

            config.set('Real_Time_Save_Image', 'ImageFolder', str_save_img_pc_folder.get())
            config.set('Real_Time_Save_Image', 'ImageName', str_save_img_name.get())
            config.set('Real_Time_Setup_Files', 'ScopeLocation', str(int_setup_location.get()))
            config.set('Real_Time_Setup_Files', 'FileFolder', str_save_scope_folder.get())
            config.set('Real_Time_Setup_Files', 'SetupFileName', str_file_name.get())
            config.set('Real_Time_Setup_Files', 'LoadLabel', str(boolvar_load_label.get()))

            # config.set('PCIe_Clock_Config', 'PCIeClockChannel', str_pcieclock_channel.get())
            config.set('PCIe_Clock_Config_Selected_Values', 'PCIeClockSamplingRate', str_pcieclock_samplingrate.get())
            # config.set('PCIe_Clock_Config', 'PCIeClockMemoryDepth', str_pcieclock_memory_depth.get())
            config.set('PCIe_Clock_Config_Selected_Values', 'PCIeClockVoltageScale', str_pcieclock_voltage_scale.get())
            config.set('PCIe_Clock_Config_Selected_Values', 'PCIeClockVoltageOffset', str_pcieclock_voltage_offset.get())
            config.set('PCIe_Clock_Config', 'PCIeClockTimebaseScale', str_pcieclock_timebase_scale.get())
            config.set('PCIe_Clock_Config', 'IsLPF', str(boolvar_5G_LPF.get()))

            config.set('PCIe_Clock_SAve_and_Load', 'PCIeClockScopeLocation', str(int_pcieclock_scope_location.get()))
            config.set('PCIe_Clock_SAve_and_Load', 'FileType', str(int_pcieclock_file_type.get()))
            # config.set('PCIe_Clock_SAve_and_Load', 'PCFolder', str_pcieclock_pc_folder.get())
            config.set('PCIe_Clock_SAve_and_Load', 'ScopeFolder', str_pcieclock_scope_folder.get())
            config.set('PCIe_Clock_SAve_and_Load', 'FileName', str_pcieclock_file_name.get())

            config.write(open(os.path.join(os.path.dirname(__file__), 'InitConfig_setup.ini'), 'w'))

            window.destroy()
            sys.exit()


    ### Comobobox and .ini Related ###
    def combo_ini():
        config_initial = configparser.ConfigParser()
        config_initial.optionxform = str
        config_file = os.path.join(os.path.dirname(__file__), 'InitConfig_setup.ini')
        config_initial.read(config_file, encoding='UTF-8')
        
        # Scale
        RealTimeSamplingRate_options = config_initial['Real_Time_Eye_Wizard'].get('RealTimeSamplingRate', '').split(',')
        RealTimeFrequency_options = config_initial['Real_Time_Eye_Wizard'].get('RealTimeFrequency', '').split(',')

        RealTimeVoltScale_options = config_initial['Real_Time_Config'].get('VoltageScale', '').split(',')
        RealTimeVoltOffset_options = config_initial['Real_Time_Config'].get('VoltageOffset', '').split(',')
        RealTimeTriggerLevel_options = config_initial['Real_Time_Config'].get('TriggerLevel', '').split(',')
        
        PCIeClockSamplingRate_options = config_initial['PCIe_Clock_Config'].get('PCIeClockSamplingRate', '').split(',')
        PCIeClockVoltageScale_options = config_initial['PCIe_Clock_Config'].get('PCIeClockVoltageScale', '').split(',')
        PCIeClockVoltageOffset_options = config_initial['PCIe_Clock_Config'].get('PCIeClockVoltageOffset', '').split(',')
        
        # 從這裡返回值供其他部分調用
        return {
            'RealTimeSamplingRate': RealTimeSamplingRate_options, 
            'RealTimeFrequency': RealTimeFrequency_options, 

            'VoltageScale': RealTimeVoltScale_options, 
            'VoltageOffset': RealTimeVoltOffset_options, 
            'TriggerLevel': RealTimeTriggerLevel_options, 

            'PCIeClockSamplingRate': PCIeClockSamplingRate_options, 
            'PCIeClockVoltageScale': PCIeClockVoltageScale_options, 
            'PCIeClockVoltageOffset': PCIeClockVoltageOffset_options, 
            
            'config_file': config_file,  # 儲存config文件路徑以便後續使用

            'selected_values': {
                'RealTimeSamplingRate': config_initial['Real_Time_Eye_Wizard_Selected_Values'].get('RealTimeSamplingRate', ''),
                'RealTimeFrequency': config_initial['Real_Time_Eye_Wizard_Selected_Values'].get('RealTimeFrequency', ''),
                
                'VoltageScale': config_initial['Real_Time_Config_Selected_Values'].get('VoltageScale', ''),
                'VoltageOffset': config_initial['Real_Time_Config_Selected_Values'].get('VoltageOffset', ''),
                'TriggerLevel': config_initial['Real_Time_Config_Selected_Values'].get('TriggerLevel', ''),
                
                'PCIeClockSamplingRate': config_initial['PCIe_Clock_Config_Selected_Values'].get('PCIeClockSamplingRate', ''),
                'PCIeClockVoltageScale': config_initial['PCIe_Clock_Config_Selected_Values'].get('PCIeClockVoltageScale', ''),
                'PCIeClockVoltageOffset': config_initial['PCIe_Clock_Config_Selected_Values'].get('PCIeClockVoltageOffset', ''),
                }        
        }

    def add_option(combobox, combobox_value, options, config_file, section, key, selected_section):
        new_option = combobox_value.get().strip()
        if new_option and new_option not in options:
            options.append(new_option)
            combobox['values'] = options
            save_to_ini(config_file, section, key, options, selected_section, combobox.get())

    def delete_option(combobox, combobox_value, options, config_file, section, key, selected_section):
        selected_option = combobox_value.get().strip()
        if selected_option in options:
            options.remove(selected_option)
            combobox['values'] = options
            combobox_value.set('')  # 清空當前選擇
            save_to_ini(config_file, section, key, options, selected_section, combobox.get())

    def save_to_ini(config_file, section, key, updated_options, selected_section, selected_value):
        config = configparser.ConfigParser()
        config.optionxform = str  # 保持大小寫
        config.read(config_file)
        if section not in config:
            config.add_section(section)
        
        # 更新指定的選項值
        config[section][key] = ','.join(updated_options)

        if selected_section not in config:
            config.add_section(selected_section)
        
        config[selected_section][key] = selected_value
        
        # 寫回INI文件
        with open(config_file, 'w') as configfile:
            config.write(configfile)


    ### Waveform Color Realted ###
    def update_color(value):
        """根據數值改變文字顏色"""
        if value == 50:
            entry_wfm_intensity.config(fg="black")
        else:
            entry_wfm_intensity.config(fg="red")

    def validate_number(new_value):
        """限制只能輸入數字 (允許空白)"""
        if new_value == "":  # 空白允許
            entry_wfm_intensity.config(fg="red")
            return True
        if new_value.isdigit():
            num = int(new_value)
            # 限制範圍
            if wfm_intensity_MIN_VALUE <= num <= wfm_intensity_MAX_VALUE:
                update_color(num)
            else:
                entry_wfm_intensity.config(fg="red")
            return True
        return False  # 阻擋非數字字元

    def on_mouse_wheel(event):
        try:
            value = int(entry_wfm_intensity.get())
        except ValueError:
            value = 0

        if event.delta > 0:
            value += wfm_intensity_STEP
        else:
            value -= wfm_intensity_STEP

        value = max(wfm_intensity_MIN_VALUE, min(wfm_intensity_MAX_VALUE, value))
        entry_wfm_intensity.delete(0, tk.END)
        entry_wfm_intensity.insert(0, str(value))
        update_color(value)

    def set_to_50():
        value = 50
        entry_wfm_intensity.delete(0, tk.END)
        entry_wfm_intensity.insert(0, str(value))
        update_color(value)
        uxr.intensity_check(intensity_value= 50)


    ### Change Label Text Related ###
    def select1_change_label_text():
        label_result_type_1.config(text= "Mean")
        label_result_type_2.config(text= "--")

    def select2_change_label_text():
        label_result_type_1.config(text= "Min")
        label_result_type_2.config(text= "Max")   

    def rgba_to_rgb_composite(in_path, out_path, background=(0, 0, 0)):
        img = Image.open(in_path)
        # 確保有 alpha 通道用 RGBA
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        # 建一個同尺寸的背景（含不透明 alpha）
        bg = Image.new('RGBA', img.size, background + (255,))
        # 將原圖疊在背景上，並去掉 alpha
        composed = Image.alpha_composite(bg, img).convert('RGB')
        composed.save(out_path, format='PNG')


    class ToolTip:
        def __init__(self, widget, text):
            self.widget = widget
            self.text = text
            self.tip_window = None
            self.widget.bind("<Enter>", self.show_tip)
            self.widget.bind("<Leave>", self.hide_tip)

        def show_tip(self, event=None):
            "Display text in tooltip window"
            if self.tip_window or not self.text:
                return
            x, y, cx, cy = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 57
            y += self.widget.winfo_rooty() + 21
            self.tip_window = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry("+%d+%d" % (x, y))
            label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                            background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                            font=("tahoma", "8", "normal"))
            label.pack(ipadx=1)

        def hide_tip(self, event=None):
            if self.tip_window:
                self.tip_window.destroy()
                self.tip_window = None


    # 獲取ini數據
    config_data = combo_ini()
    config_file_path = config_data['config_file']


    def commbobox_function(combobox, combobox_var, ini_dict_key, ini_option_section, ini_option_key, ini_selected_section):
        combobox['values'] = config_data[ini_dict_key]  # 設置初始選項
        combobox.bind('<Return>', lambda event: add_option(combobox, combobox_var, config_data[ini_dict_key], config_file_path, ini_option_section, ini_option_key, ini_selected_section))
        combobox.bind('<Delete>', lambda event: delete_option(combobox, combobox_var, config_data[ini_dict_key], config_file_path, ini_option_section, ini_option_key, ini_selected_section))

    def select_folder(entry_var):
        # 打開檔案瀏覽器以選擇資料夾
        folder_selected = filedialog.askdirectory()
        # 將選擇的資料夾路徑填入 Entry
        entry_var.set(folder_selected)



    window = tk.Tk()
    window.title(window_name)
    # window.geometry('1500x760+2+2')
    window.geometry('+2+2')
    window.configure(bg= "#868686")

    frame_bg_color_1= "#b5b5b5"
    frame_bg_color_2= "#A5A5A5"
    labelframe_word_color= "#FCFCFC"
    label_word_color= "#252525"
    selected_notebook_tab_color= "#5F5F5F"
    unselected_notebook_tab_color= "#C9C9C9"
    text_name_color= "#4D4D4D"
    text_result_color= "#313131"

    # 設定wfm intensity參數
    wfm_intensity_STEP = 1
    wfm_intensity_MIN_VALUE = 0
    wfm_intensity_MAX_VALUE = 100

    s = ttk.Style()
    s.theme_create( "MyStyle", 
                parent="xpnative",  # ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
                settings={
                    "TNotebook": {"configure": {"tabmargins": [5, 5, 0, 0], 
                                                "relief": 'alt',
                                                "borderwidth": 0, 
                                                }
                                    },
                    "TNotebook.Tab": {"configure": {"padding": [10, 10],
                                                    "font" : ('Cambria', '15', 'bold'),
                                                    "foreground": unselected_notebook_tab_color,
                                                    # "background": 'blue'
                                                    },
                                        "map": {"foreground": [("selected", selected_notebook_tab_color)],
                                                # "background": [("selected", 'green'),],
                                                },
                                        "expand": [("selected", [1, 1, 1, 0])] 
                                        },
                    }
                )
    s.theme_use("MyStyle")
    s.configure('TNotebook', 
                # tabposition='ns', 
                background= "#868686", 
                borderwidth= 0)
    s.configure('TNotebook.Tab', relief= 'flat', borderwidth= 0)


    notebook=ttk.Notebook(window)

    notebook_frame_realtime= tk.Frame()
    notebook_frame_pcieclock= tk.Frame()
    
    ##### Notebook - Real-time eye ##### 
    # Real-time Eye Wizard Frame ===================================================================================================================================
    label_frame_realtime_eye_wizard= tk.LabelFrame(notebook_frame_realtime, text= 'Real-time Eye Wizard', background= frame_bg_color_2, fg= labelframe_word_color, font= ('Candara', 11, 'bold'),)

    button_chan1 = tk.Button(label_frame_realtime_eye_wizard, text='Channel 1', width= 20, height= 2, command= lambda: uxr.display_Chan(chan= 1, bookmark= str_label_name.get(), label_choose_type= int_label_type.get()))
    button_chan2 = tk.Button(label_frame_realtime_eye_wizard, text='Channel 2', width= 20, height= 2, command= lambda: uxr.display_Chan(chan= 2, bookmark= str_label_name.get(), label_choose_type= int_label_type.get()))
    button_chan3 = tk.Button(label_frame_realtime_eye_wizard, text='Channel 3', width= 20, height= 2, command= lambda: uxr.display_Chan(chan= 3, bookmark= str_label_name.get(), label_choose_type= int_label_type.get()))
    button_chan4 = tk.Button(label_frame_realtime_eye_wizard, text='Channel 4', width= 20, height= 2, command= lambda: uxr.display_Chan(chan= 4, bookmark= str_label_name.get(), label_choose_type= int_label_type.get()))

    # label_channel = tk.Label(label_frame_realtime_eye_wizard, text= 'Channel', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12,),)
    # str_channel = tk.StringVar()
    # combobox_channel = ttk.Combobox(label_frame_realtime_eye_wizard, width= 5, textvariable= str_channel, values= ['1', '2', '3', '4'])

    label_frequency = tk.Label(label_frame_realtime_eye_wizard, text= 'Frequency (Hz)', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12,),)
    str_frequency = tk.StringVar()
    combobox_frequency = ttk.Combobox(label_frame_realtime_eye_wizard, width= 5, textvariable= str_frequency)
    commbobox_function(combobox= combobox_frequency, combobox_var= str_frequency, ini_dict_key= 'RealTimeFrequency', ini_option_section= 'Real_Time_Eye_Wizard', ini_option_key= 'RealTimeFrequency', ini_selected_section= 'Real_Time_Eye_Wizard_Selected_Values')

    label_sampling_rate = tk.Label(label_frame_realtime_eye_wizard, text= 'Sampling Rate (Sa/s)', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12,),)
    str_sampling_rate = tk.StringVar()
    combobox_sampling_rate = ttk.Combobox(label_frame_realtime_eye_wizard, width= 5, textvariable= str_sampling_rate)
    commbobox_function(combobox= combobox_sampling_rate, combobox_var= str_sampling_rate, ini_dict_key= 'RealTimeSamplingRate', ini_option_section= 'Real_Time_Eye_Wizard', ini_option_key= 'RealTimeSamplingRate', ini_selected_section= 'Real_Time_Eye_Wizard_Selected_Values')

    label_memory_depth = tk.Label(label_frame_realtime_eye_wizard, text= 'Memory Depth (pts)', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12,),)
    str_memory_depth = tk.StringVar()
    enrty_memory_depth = tk.Entry(label_frame_realtime_eye_wizard, width= 7, textvariable= str_memory_depth)

    button_reai_time_eye_setup = tk.Button(label_frame_realtime_eye_wizard, text= 'Setup', width= 20, height= 2, command= lambda: uxr.setup_real_time_eye(
        sampling_rate= str_sampling_rate.get(), 
        acquire_points= str_memory_depth.get(), 
        frequency= str_frequency.get()
    ))

    # Mask Test Frame ===================================================================================================================================
    label_frame_mask_test= tk.LabelFrame(notebook_frame_realtime, text= 'Mask Test', background= frame_bg_color_1, fg= labelframe_word_color, font= ('Candara', 11, 'bold'),)
    
    label_mask_locaiton= tk.Label(label_frame_mask_test, text= 'Scope Location', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 12,),)
    int_mask_location = tk.IntVar()    
    radiobutton_mask_location_desktop= tk.Radiobutton(label_frame_mask_test, text= 'Desktop', variable= int_mask_location, value= 1, background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)
    radiobutton_mask_location_desktop.select()
    radiobutton_mask_location_server= tk.Radiobutton(label_frame_mask_test, text= 'Server', variable= int_mask_location, value= 2, background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)
    
    label_mask_path = tk.Label(label_frame_mask_test, text= 'Mask Path', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 12,),)
    str_mask_path = tk.StringVar()
    enrty_mask_path = tk.Entry(label_frame_mask_test, width= 48, textvariable= str_mask_path)

    button_mask_path_browse = tk.Button(label_frame_mask_test, text= 'Browse', width= 12, height= 1, command= lambda: select_folder(entry_var= str_mask_path))

    label_mask_name = tk.Label(label_frame_mask_test, text= 'Mask Name', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 12,),)
    str_mask_name = tk.StringVar()
    enrty_mask_name = tk.Entry(label_frame_mask_test, width= 48, textvariable= str_mask_name)

    label_ui_counts = tk.Label(label_frame_mask_test, text= 'UI Counts (UI)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 12,),)
    str_ui_counts = tk.StringVar()
    enrty_ui_counts = tk.Entry(label_frame_mask_test, width= 20, textvariable= str_ui_counts)

    int_mask_stop_type = tk.IntVar()    
    radiobutton_stop_on_ui= tk.Radiobutton(label_frame_mask_test, text= 'Stop on UI counts', variable= int_mask_stop_type, value= 1, background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)
    radiobutton_stop_on_ui.select()
    radiobutton_stop_on_failure= tk.Radiobutton(label_frame_mask_test, text= 'Stop on failure', variable= int_mask_stop_type, value= 2, background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)
    radiobutton_forever= tk.Radiobutton(label_frame_mask_test, text= 'Forever', variable= int_mask_stop_type, value= 3, background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)
    
    button_mask_test_setup = tk.Button(label_frame_mask_test, text= 'Setup', width= 20, height= 2, command= lambda: uxr.setup_mask_test(
        mask_name= str_mask_path.get(), 
        ui_counts= str_ui_counts.get()
    ))
    button_mask_test_run = tk.Button(label_frame_mask_test, text= 'Run', width= 20, height= 2, command= lambda: uxr.run_mask_test())
    button_mask_test_stop = tk.Button(label_frame_mask_test, text= 'Stop', width= 20, height= 2, command= lambda: uxr.stop_mask_test())
    button_mask_window_close = tk.Button(label_frame_mask_test, text= 'Close', width= 20, height= 2, command= lambda: uxr.disable_mask_test())

    # Histogram Frame ===================================================================================================================================
    label_frame_histogram= tk.LabelFrame(notebook_frame_realtime, text= 'Histogram', background= frame_bg_color_2, fg= labelframe_word_color, font= ('Candara', 11, 'bold'),)

    label_dimension= tk.Label(label_frame_histogram, text= 'Dimension', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12,),)
    int_dimension = tk.IntVar()    
    radiobutton_horizontal= tk.Radiobutton(label_frame_histogram, text= 'Horizontal', variable= int_dimension, value= 1, background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 11, 'bold'),)
    radiobutton_horizontal.select()
    radiobutton_vertical= tk.Radiobutton(label_frame_histogram, text= 'Vertical', variable= int_dimension, value= 2, background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 11, 'bold'),)

    label_top_limit = tk.Label(label_frame_histogram, text= 'Top Limits (mV)', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12,),)
    str_top_limit = tk.StringVar()
    enrty_top_limit = tk.Entry(label_frame_histogram, width= 12, textvariable= str_top_limit)

    label_bottom_limit = tk.Label(label_frame_histogram, text= 'Bottom Limits (mV)', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12,),)
    str_bottom_limit = tk.StringVar()
    enrty_bottom_limit = tk.Entry(label_frame_histogram, width= 12, textvariable= str_bottom_limit)

    label_left_limit = tk.Label(label_frame_histogram, text= 'Left Limits (s)', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12,),)
    str_left_limit = tk.StringVar()
    enrty_left_limit = tk.Entry(label_frame_histogram, width= 12, textvariable= str_left_limit)

    label_right_limit = tk.Label(label_frame_histogram, text= 'Right Limits (s)', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12,),)
    str_right_limit = tk.StringVar()
    enrty_right_limit = tk.Entry(label_frame_histogram, width= 12, textvariable= str_right_limit)

    button_histogram_setup = tk.Button(label_frame_histogram, text= 'Setup', width= 20, height= 2, command= lambda: uxr.setup_histogram(
        top_limit= str_top_limit.get(), 
        bottom_limit= str_bottom_limit.get(), 
        left_limit= str_left_limit.get(), 
        right_limit= str_right_limit.get()
    ))
    button_histogram_window_close = tk.Button(label_frame_histogram, text= 'Close', width= 20, height= 2, command= lambda: uxr.disable_histogram())

    # Measurement Frame ===================================================================================================================================
    label_frame_measurement= tk.LabelFrame(notebook_frame_realtime, text= 'Measurement', background= frame_bg_color_1, fg= labelframe_word_color, font= ('Candara', 11, 'bold'),)
    
    button_Vpp = tk.Button(label_frame_measurement, text= 'Vpp', width= 20, height= 2, command= lambda: uxr.vpp_measurement())
    button_VIH = tk.Button(label_frame_measurement, text= 'VIH', width= 20, height= 2, command= lambda: uxr.vih_measurement())
    button_VIL = tk.Button(label_frame_measurement, text= 'VIL', width= 20, height= 2, command= lambda: uxr.vil_width_measurement())
    button_eye_height = tk.Button(label_frame_measurement, text= 'Eye Height', width= 20, height= 2, command= lambda: uxr.eye_height_measurement())
    button_eye_width = tk.Button(label_frame_measurement, text= 'Eye Width', width= 20, height= 2, command= lambda: uxr.eye_width_measurement())
    button_cdrrate = tk.Button(label_frame_measurement, text= 'CDR rate', width= 20, height= 2, command= lambda: uxr.cdr_rate_measurement())

    # Control Frame ===================================================================================================================================
    label_frame_control= tk.LabelFrame(notebook_frame_realtime, text= 'Control', background= frame_bg_color_2, fg= labelframe_word_color, font= ('Candara', 11, 'bold'),)

    button_run = tk.Button(label_frame_control, text='RUN', width= 20, height= 2, command= lambda: uxr.run())
    button_stop = tk.Button(label_frame_control, text='STOP', width= 20, height= 2, command= lambda: uxr.stop())
    button_single = tk.Button(label_frame_control, text='SINGLE', width= 20, height= 2, command= lambda: uxr.single())
    button_clear_display = tk.Button(label_frame_control, text='Clear', width= 20, height= 2, command= lambda: uxr.clear_diaplay())
    button_clear_display.config(state= 'disabled')
    button_autoscale = tk.Button(label_frame_control, text='Auto Scale', width= 20, height= 2, command= lambda: uxr.autoscale())
    button_autoscale.config(state= 'disabled')
    button_default = tk.Button(label_frame_control, text='Default', width= 20, height= 2, command= lambda: uxr.default())
    button_default.config(state= 'disabled')
    button_trigger_type = tk.Button(label_frame_control, text='Trigger Type', width= 20, height= 2, command= lambda: uxr.trig_type())
    button_del_meas = tk.Button(label_frame_control, text='Delete item', width= 20, height= 2, command= lambda: uxr.delete_item())
    button_add_marker = tk.Button(label_frame_control, text='Add Marker', width= 20, height= 2, command= lambda: uxr.add_marker())
    button_del_marker = tk.Button(label_frame_control, text='Del Marker', width= 20, height= 2, command= lambda: uxr.delete_marker())

    boolver_marker_color = tk.BooleanVar()
    checkbutton_marker_color= tk.Checkbutton(label_frame_control, text= 'Multi-Marker Color', variable= boolver_marker_color, background= frame_bg_color_2, fg= label_word_color, font= ('Calibri', 11, 'bold'))

    def disable_button():
        if button_autoscale["state"] == 'normal':
            button_autoscale.config(state="disabled")
        else:
            button_autoscale.config(state="normal")
        if button_default["state"] == 'normal':
            button_default.config(state="disabled")
        else:
            button_default.config(state="normal")
        if button_clear_display["state"] == 'normal':
            button_clear_display.config(state="disabled")
        else:
            button_clear_display.config(state="normal")

    button_disable = tk.Button(label_frame_control, text= 'Disable', width= 20, height= 2, command= disable_button)

    boolvar_marker_1 = tk.BooleanVar()    
    checkbutton_marker_1= tk.Checkbutton(label_frame_control, text= 'Meas 1', variable= boolvar_marker_1, background= frame_bg_color_2, fg= label_word_color)
    boolvar_marker_2 = tk.BooleanVar()    
    checkbutton_marker_2= tk.Checkbutton(label_frame_control, text= 'Meas 2', variable= boolvar_marker_2, background= frame_bg_color_2, fg= label_word_color)
    boolvar_marker_3 = tk.BooleanVar()    
    checkbutton_marker_3= tk.Checkbutton(label_frame_control, text= 'Meas 3', variable= boolvar_marker_3, background= frame_bg_color_2, fg= label_word_color)
    boolvar_marker_4 = tk.BooleanVar()    
    checkbutton_marker_4= tk.Checkbutton(label_frame_control, text= 'Meas 4', variable= boolvar_marker_4, background= frame_bg_color_2, fg= label_word_color)
    boolvar_marker_5 = tk.BooleanVar()    
    checkbutton_marker_5= tk.Checkbutton(label_frame_control, text= 'Meas 5', variable= boolvar_marker_5, background= frame_bg_color_2, fg= label_word_color)
    boolvar_marker_6 = tk.BooleanVar()    
    checkbutton_marker_6= tk.Checkbutton(label_frame_control, text= 'Meas 6', variable= boolvar_marker_6, background= frame_bg_color_2, fg= label_word_color)

    # Config Frame ===================================================================================================================================
    label_frame_config= tk.LabelFrame(notebook_frame_realtime, text= 'Config.', background= frame_bg_color_1, fg= labelframe_word_color, font= ('Candara', 11, 'bold'),)

    label_voltage_scale = tk.Label(label_frame_config, text= 'Voltage Scale (V)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)
    str_voltage_scale = tk.StringVar()
    combobox_voltage_scale = ttk.Combobox(label_frame_config, width= 12, textvariable= str_voltage_scale)
    commbobox_function(combobox= combobox_voltage_scale, combobox_var= str_voltage_scale, ini_dict_key= 'VoltageScale', ini_option_section= 'Real_Time_Config', ini_option_key= 'VoltageScale', ini_selected_section= 'Real_Time_Config_Selected_Values')

    button_voltage_scale_check = tk.Button(label_frame_config, text='Check', width= 12, height= 1, command= lambda: uxr.voltage_scale_check(
        voltage_scale= str_voltage_scale.get(), 
    ))

    label_voltage_offset = tk.Label(label_frame_config, text= 'Voltage Offset (V)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)
    str_voltage_offset = tk.StringVar()
    combobox_voltage_offset = ttk.Combobox(label_frame_config, width= 12, textvariable= str_voltage_offset)
    commbobox_function(combobox= combobox_voltage_offset, combobox_var= str_voltage_offset, ini_dict_key= 'VoltageOffset', ini_option_section= 'Real_Time_Config', ini_option_key= 'VoltageOffset', ini_selected_section= 'Real_Time_Config_Selected_Values')

    button_voltage_offset_check = tk.Button(label_frame_config, text='Check', width= 12, height= 1, command= lambda: uxr.voltage_offset_check(
        voltage_offset= str_voltage_offset.get()
    ))

    label_timebase_scale = tk.Label(label_frame_config, text= 'Timebase Scale (s)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)
    str_timebase_scale = tk.StringVar()
    enrty_timebase_scale = tk.Entry(label_frame_config, width= 12, textvariable= str_timebase_scale)

    button_timebase_scale_check = tk.Button(label_frame_config, text='Check', width= 12, height= 1, command= lambda: uxr.timebase_scale_check(
        timebase_scale= str_timebase_scale.get()
    ))

    label_timebase_offset = tk.Label(label_frame_config, text= 'Timebase Offset (s)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)
    str_timebase_offset = tk.StringVar()
    enrty_timebase_offset = tk.Entry(label_frame_config, width= 12, textvariable= str_timebase_offset)

    button_timebase_offset_check = tk.Button(label_frame_config, text='Check', width= 12, height= 1, command= lambda: uxr.timebase_position_check(
        timebase_position= str_timebase_offset.get()
    ))

    label_trigger_channel = tk.Label(label_frame_config, text= 'Trigger Channel', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)
    str_trigger_channel = tk.StringVar()
    combobox_trigger_channel = ttk.Combobox(label_frame_config, width= 12, textvariable= str_trigger_channel, values= ['1', '2', '3', '4'])
    # commbobox_function(combobox= combobox_trigger_channel, combobox_var= str_trigger_channel, ini_dict_key= 'TriggerChan', ini_option_section= 'Real_Time_Config', ini_option_key= 'TriggerChan', ini_selected_section= 'Real_Time_Config')

    label_trigger_level = tk.Label(label_frame_config, text= 'Trigger Level (V)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)
    str_trigger_level = tk.StringVar()
    combobox_trigger_level = ttk.Combobox(label_frame_config, width= 12, textvariable= str_trigger_level)
    commbobox_function(combobox= combobox_trigger_level, combobox_var= str_trigger_level, ini_dict_key= 'TriggerLevel', ini_option_section= 'Real_Time_Config', ini_option_key= 'TriggerLevel', ini_selected_section= 'Real_Time_Config_Selected_Values')

    button_trigger_check = tk.Button(label_frame_config, text='Check', width= 12, height= 1, command= lambda: uxr.trigger_check(
        trigger_channel= str_trigger_channel.get(), 
        trigger_level= str_trigger_level.get()
    ))

    label_wfm_intensity = tk.Label(label_frame_config, text= 'Waveform Intensity', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)
    vcmd = (notebook_frame_realtime.register(validate_number), "%P") # %P = 輸入後字串
    str_wfm_intensity = tk.StringVar()
    entry_wfm_intensity = tk.Entry(label_frame_config, width= 12, justify="center", textvariable= str_wfm_intensity, validate="key", validatecommand=vcmd)
    update_color(value= str_wfm_intensity.get())
    button_wfm_intensity = tk.Button(label_frame_config, text= 'Check', width= 12, height= 1, command= lambda: uxr.intensity_check(
        intensity_value= str_wfm_intensity.get()
    ))
    
    button_set_intensity_50 = tk.Button(label_frame_config, text="Set Intensity 50", command= set_to_50, font=("Candara", 10))

    entry_wfm_intensity.bind("<MouseWheel>", on_mouse_wheel)
    entry_wfm_intensity.bind("<Button-4>", lambda e: on_mouse_wheel(type("Event", (), {"delta": 120})))
    entry_wfm_intensity.bind("<Button-5>", lambda e: on_mouse_wheel(type("Event", (), {"delta": -120})))

    label_label_type= tk.Label(label_frame_config, text= 'Label Type', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 12,),)
    int_label_type = tk.IntVar()    
    radiobutton_label= tk.Radiobutton(label_frame_config, text= 'Label', variable= int_label_type, value= 1, background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)
    radiobutton_label.select()
    radiobutton_bookmark= tk.Radiobutton(label_frame_config, text= 'Bookmark', variable= int_label_type, value= 2, background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)

    label_label_name= tk.Label(label_frame_config, text= 'Label Name', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 12,),)
    str_label_name = tk.StringVar()
    enrty_label_name = tk.Entry(label_frame_config, width= 18, textvariable= str_label_name)
    button_add_label = tk.Button(label_frame_config, text='Add Label', width= 12, height= 1, command= lambda: uxr.add_bookmark(
        choose_type= int_label_type.get(), 
        bookmark= str_label_name.get()
    ))
    button_del_label = tk.Button(label_frame_config, text='Delete Label', width= 12, height= 1, command= lambda: uxr.delete_bookmark(
        label_choose_type= int_label_type.get()
    ))

    # Save Image Frame ===================================================================================================================================
    label_frame_save_image= tk.LabelFrame(notebook_frame_realtime, text= 'Save Image.', background= frame_bg_color_2, fg= labelframe_word_color, font= ('Candara', 11, 'bold'),)

    label_save_img_pc_folder = tk.Label(label_frame_save_image, text= 'Image Folder (PC)', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 11),)
    str_save_img_pc_folder = tk.StringVar()
    enrty_save_img_pc_folder = tk.Entry(label_frame_save_image, width= 60, textvariable= str_save_img_pc_folder)

    button_img_pc_folder_browse = tk.Button(label_frame_save_image, text='Browse', width= 12, height= 1, command= lambda: select_folder(entry_var= str_save_img_pc_folder))

    label_save_img_name = tk.Label(label_frame_save_image, text= 'Image Name', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 11),)
    str_save_img_name = tk.StringVar()
    enrty_save_img_name = tk.Entry(label_frame_save_image, width= 60, textvariable= str_save_img_name)

    button_img_name_save = tk.Button(label_frame_save_image, text='Save', width= 12, height= 1, command= lambda: uxr.save_image_pc(
        pc_folder= str_save_img_pc_folder.get(), 
        file_name= str_save_img_name.get()
    ))

    # Setup File Frame ===================================================================================================================================
    label_frame_setup_file= tk.LabelFrame(notebook_frame_realtime, text= 'Setup Files', background= frame_bg_color_1, fg= labelframe_word_color, font= ('Candara', 11, 'bold'),)

    label_setup_locaiton= tk.Label(label_frame_setup_file, text= 'Scope Location', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 12,),)
    int_setup_location = tk.IntVar()    
    radiobutton_setup_location_desktop= tk.Radiobutton(label_frame_setup_file, text= 'Desktop', variable= int_setup_location, value= 1, background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)
    radiobutton_setup_location_desktop.select()
    radiobutton_setup_location_server= tk.Radiobutton(label_frame_setup_file, text= 'Server', variable= int_setup_location, value= 2, background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)

    label_save_scope_folder = tk.Label(label_frame_setup_file, text= 'Scope Folder', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11),)
    str_save_scope_folder = tk.StringVar()
    enrty_save_scope_folder = tk.Entry(label_frame_setup_file, width= 40, textvariable= str_save_scope_folder)

    button_scope_folder_browse = tk.Button(label_frame_setup_file, text='Browse', width= 12, height= 1, command= lambda: select_folder(
        entry_var= str_save_scope_folder.get()
    ))

    label_file_name = tk.Label(label_frame_setup_file, text= 'File Name', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)
    str_file_name = tk.StringVar()
    enrty_file_name = tk.Entry(label_frame_setup_file, width= 40, textvariable= str_file_name)

    button_file_name_save = tk.Button(label_frame_setup_file, text='Save', width= 12, height= 1, command= lambda: uxr.save_setup_file_scope(
        folder= str_save_scope_folder.get(), 
        current_file_name= str_file_name.get(), 
        path_choice= int_setup_location.get(), 
        file_type_choice= 2
    ))
    button_file_name_load = tk.Button(label_frame_setup_file, text='Load', width= 12, height= 1, command= lambda: uxr.load_setup(
        folder= str_save_scope_folder.get(), 
        setup_name= str_file_name.get(), 
        label_choose_type= int_label_type.get(), 
        file_path_choice= int_setup_location.get()
    ))

    boolvar_load_label = tk.BooleanVar()    
    cbheckbutton_setup_label= tk.Checkbutton(label_frame_setup_file, text= 'Label', variable= boolvar_load_label, background= frame_bg_color_1, fg= label_word_color)
    cbheckbutton_setup_label.select()

    # Extract Results Frame ===================================================================================================================================
    label_frame_extract_results= tk.LabelFrame(notebook_frame_realtime, text= 'Extract Results', background= frame_bg_color_2, fg= labelframe_word_color, font= ('Candara', 11, 'bold'),)

    button_get_results = tk.Button(label_frame_extract_results, text= 'Get Results\n(最多取6個)', width= 20, height= 2, command= lambda: uxr.get_results())
    
    intvar_result_type = tk.IntVar()   
    rb_mean_result = tk.Radiobutton(label_frame_extract_results, text= 'Mean', variable= intvar_result_type, value= 1, background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 11,), command= lambda: select1_change_label_text())
    rb_minmax_result = tk.Radiobutton(label_frame_extract_results, text= 'Min & Max', variable= intvar_result_type, value= 2, background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 11,), command= lambda: select2_change_label_text())
    intvar_result_type.set(value= 1)

    label_result_type_0 = tk.Label(label_frame_extract_results, text= 'Name', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12, 'bold'),)
    label_result_type_1 = tk.Label(label_frame_extract_results, text= 'Mean', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12, 'bold'),)
    label_result_type_2 = tk.Label(label_frame_extract_results, text= '', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12, 'bold'),)
    
    label_meas_name_1 = tk.Label(label_frame_extract_results, text= '', background= frame_bg_color_2, fg= '#516464', font= ('Candara', 11, 'bold'),)
    text_result1_1 = tk.Text(label_frame_extract_results, width= 22, height= 1, background= "#EEEEEE", fg= '#375050', font= ('Calibri', 11, 'bold'),)
    text_result1_1.config(state=tk.DISABLED)
    text_result2_1 = tk.Text(label_frame_extract_results, width= 22, height= 1, background= "#EEEEEE", fg= '#375050', font= ('Calibri', 11, 'bold'),)
    text_result2_1.config(state=tk.DISABLED)
    
    label_meas_name_2 = tk.Label(label_frame_extract_results, text= '', background= frame_bg_color_2, fg= '#516464', font= ('Candara', 11, 'bold'),)
    text_result1_2 = tk.Text(label_frame_extract_results, width= 22, height= 1, background= '#EEEEEE', fg= '#375050', font= ('Calibri', 11, 'bold'),)
    text_result1_2.config(state=tk.DISABLED)
    text_result2_2 = tk.Text(label_frame_extract_results, width= 22, height= 1, background= "#EEEEEE", fg= '#375050', font= ('Calibri', 11, 'bold'),)
    text_result2_2.config(state=tk.DISABLED)
    
    label_meas_name_3 = tk.Label(label_frame_extract_results, text= '', background= frame_bg_color_2, fg= '#516464', font= ('Candara', 11, 'bold'),)
    text_result1_3 = tk.Text(label_frame_extract_results, width= 22, height= 1, background= '#EEEEEE', fg= '#375050', font= ('Calibri', 11, 'bold'),)
    text_result1_3.config(state=tk.DISABLED)
    text_result2_3 = tk.Text(label_frame_extract_results, width= 22, height= 1, background= "#EEEEEE", fg= '#375050', font= ('Calibri', 11, 'bold'),)
    text_result2_3.config(state=tk.DISABLED)
    
    label_meas_name_4 = tk.Label(label_frame_extract_results, text= '', background= frame_bg_color_2, fg= '#516464', font= ('Candara', 11, 'bold'),)
    text_result1_4 = tk.Text(label_frame_extract_results, width= 22, height= 1, background= '#EEEEEE', fg= '#375050', font= ('Calibri', 11, 'bold'),)
    text_result1_4.config(state=tk.DISABLED)
    text_result2_4 = tk.Text(label_frame_extract_results, width= 22, height= 1, background= "#EEEEEE", fg= '#375050', font= ('Calibri', 11, 'bold'),)
    text_result2_4.config(state=tk.DISABLED)
    
    label_meas_name_5 = tk.Label(label_frame_extract_results, text= '', background= frame_bg_color_2, fg= '#516464', font= ('Candara', 11, 'bold'),)
    text_result1_5 = tk.Text(label_frame_extract_results, width= 22, height= 1, background= '#EEEEEE', fg= '#375050', font= ('Calibri', 11, 'bold'),)
    text_result1_5.config(state=tk.DISABLED)
    text_result2_5 = tk.Text(label_frame_extract_results, width= 22, height= 1, background= "#EEEEEE", fg= '#375050', font= ('Calibri', 11, 'bold'),)
    text_result2_5.config(state=tk.DISABLED)
    
    label_meas_name_6 = tk.Label(label_frame_extract_results, text= '', background= frame_bg_color_2, fg= '#516464', font= ('Candara', 11, 'bold'),)
    text_result1_6 = tk.Text(label_frame_extract_results, width= 22, height= 1, background= '#EEEEEE', fg= '#375050', font= ('Calibri', 11, 'bold'),)
    text_result1_6.config(state=tk.DISABLED)
    text_result2_6 = tk.Text(label_frame_extract_results, width= 22, height= 1, background= "#EEEEEE", fg= '#375050', font= ('Calibri', 11, 'bold'),)
    text_result2_6.config(state=tk.DISABLED)
    

    # Real-time eye Grid ===================================================================================================================================

    # LabelFrame grid
    label_frame_realtime_eye_wizard.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'nsew')
    label_frame_mask_test.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'nsew')
    label_frame_histogram.grid(row= 2, column= 0, padx= 5, pady= 2, sticky= 'nsew')
    label_frame_measurement.grid(row= 3, column= 0, padx= 5, pady= 2, sticky= 'nsew')
    label_frame_control.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'nsew')
    label_frame_config.grid(row= 1, column= 1, padx= 5, pady= 2, sticky= 'nsew')
    label_frame_save_image.grid(row= 2, column= 1, padx= 5, pady= 2, sticky= 'nsew')
    label_frame_setup_file.grid(row= 3, column= 1, padx= 5, pady= 2, sticky= 'nsew')
    label_frame_extract_results.grid(row= 4, column= 0, padx= 5, pady= 2, sticky= 'nsew', columnspan= 2)

    # Real-time Eye Wizard grid
    button_chan1.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    button_chan2.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'w')
    button_chan3.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'w')
    button_chan4.grid(row= 0, column= 3, padx= 5, pady= 2, sticky= 'w')

    # label_channel.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'w')
    # combobox_channel.grid(row= 1, column= 1, padx= 5, pady= 2, sticky= 'ew')

    label_frequency.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'w')
    combobox_frequency.grid(row= 1, column= 1, padx= 5, pady= 2, sticky= 'ew')

    label_sampling_rate.grid(row= 2, column= 0, padx= 5, pady= 2, sticky= 'w')
    combobox_sampling_rate.grid(row= 2, column= 1, padx= 5, pady= 2, sticky= 'ew')

    label_memory_depth.grid(row= 3, column= 0, padx= 5, pady= 2, sticky= 'w')
    enrty_memory_depth.grid(row= 3, column= 1, padx= 5, pady= 2, sticky= 'ew')

    button_reai_time_eye_setup.grid(row= 2, column= 3, padx= 5, pady= 2, sticky= 'w', columnspan= 2)

    # Mask Test grid
    label_mask_locaiton.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    radiobutton_mask_location_desktop.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'w')
    radiobutton_mask_location_server.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'w')

    label_mask_path.grid(row= 1, column= 0, padx= 5, sticky= 'w')
    enrty_mask_path.grid(row= 1, column= 1, padx= 5, sticky= 'w', columnspan= 3)
    button_mask_path_browse.grid(row= 1, column= 4, padx= 5, sticky= 'w')

    label_mask_name.grid(row= 2, column= 0, padx= 5, sticky= 'w')
    enrty_mask_name.grid(row= 2, column= 1, padx= 5, sticky= 'w', columnspan= 3)

    label_ui_counts.grid(row= 3, column= 0, padx= 5, sticky= 'w')
    enrty_ui_counts.grid(row= 3, column= 1, padx= 5, sticky= 'w', columnspan= 2)

    radiobutton_stop_on_ui.grid(row= 4, column= 1, padx= 5, sticky= 'w', columnspan= 2)
    radiobutton_stop_on_failure.grid(row= 5, column= 1, padx= 5, sticky= 'w', columnspan= 2)
    radiobutton_forever.grid(row= 6, column= 1, padx= 5, sticky= 'w', columnspan= 2)
    
    button_mask_test_setup.grid(row= 3, column= 3, padx= 5, sticky= 'w', rowspan= 2)
    button_mask_window_close.grid(row= 3, column= 4, padx= 5, sticky= 'w', rowspan= 2)
    button_mask_test_run.grid(row= 5, column= 3, padx= 5, sticky= 'w', rowspan= 2)
    button_mask_test_stop.grid(row= 5, column= 4, padx= 5, sticky= 'w', rowspan= 2)

    # Histogram grid
    label_dimension.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    radiobutton_horizontal.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'w')
    radiobutton_vertical.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'w')

    label_top_limit.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'w')
    enrty_top_limit.grid(row= 1, column= 1, padx= 5, pady= 2, sticky= 'ew')
    label_left_limit.grid(row= 1, column= 2, padx= 5, pady= 2, sticky= 'w')
    enrty_left_limit.grid(row= 1, column= 3, padx= 5, pady= 2, sticky= 'ew')

    label_bottom_limit.grid(row= 2, column= 0, padx= 5, pady= 2, sticky= 'w')
    enrty_bottom_limit.grid(row= 2, column= 1, padx= 5, pady= 2, sticky= 'ew')
    label_right_limit.grid(row= 2, column= 2, padx= 5, pady= 2, sticky= 'w')
    enrty_right_limit.grid(row= 2, column= 3, padx= 5, pady= 2, sticky= 'ew')

    button_histogram_setup.grid(row= 0, column= 4, padx= 5, pady= 2, sticky= 'w')
    button_histogram_window_close.grid(row= 1, column= 4, padx= 5, pady= 2, sticky= 'w', rowspan= 2)

    # Measurement grid
    button_Vpp.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    button_eye_width.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'w')
    button_eye_height.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'w')
    button_cdrrate.grid(row= 0, column= 3, padx= 5, pady= 2, sticky= 'w')
    button_VIH.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'w')
    button_VIL.grid(row= 1, column= 1, padx= 5, pady= 2, sticky= 'w')

    # Control grid
    button_run.grid(row= 0, column= 0, padx= 5, pady= 1, sticky= 'w', rowspan= 2)
    button_stop.grid(row= 0, column= 1, padx= 5, pady= 1, sticky= 'w', rowspan= 2)
    button_single.grid(row= 0, column= 2, padx= 5, pady= 1, sticky= 'w', rowspan= 2)
    button_trigger_type.grid(row= 0, column= 3, padx= 5, pady= 1, sticky= 'w', rowspan= 2)

    button_autoscale.grid(row= 2, column= 0, padx= 5, pady= 1, sticky= 'w', rowspan= 2)
    button_default.grid(row= 2, column= 1, padx= 5, pady= 1, sticky= 'w', rowspan= 2)
    button_clear_display.grid(row= 2, column= 2, padx= 5, pady= 1, sticky= 'w', rowspan= 2)
    button_disable.grid(row= 2, column= 3, padx= 5, pady= 1, sticky= 'w', rowspan= 2)

    button_del_meas.grid(row= 4, column= 0, padx= 5, pady= 1, sticky= 'w', rowspan= 2)
    button_add_marker.grid(row= 4, column= 1, padx= 5, pady= 1, sticky= 'w', rowspan= 2)
    button_del_marker.grid(row= 4, column= 2, padx= 5, pady= 1, sticky= 'w', rowspan= 2)

    checkbutton_marker_color.grid(row= 4, column= 3, padx= 5, pady= 1, sticky= 'w', rowspan= 2)

    checkbutton_marker_1.grid(row= 0, column= 4, padx= 5, sticky= 'w')
    checkbutton_marker_2.grid(row= 1, column= 4, padx= 5, sticky= 'w')
    checkbutton_marker_3.grid(row= 2, column= 4, padx= 5, sticky= 'w')
    checkbutton_marker_4.grid(row= 3, column= 4, padx= 5, sticky= 'w')
    checkbutton_marker_5.grid(row= 4, column= 4, padx= 5, sticky= 'w')
    checkbutton_marker_6.grid(row= 5, column= 4, padx= 5, sticky= 'w')

    # Config grid
    label_voltage_scale.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    combobox_voltage_scale.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'w')
    button_voltage_scale_check.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'w')

    label_timebase_scale.grid(row= 0, column= 3, padx= 5, pady= 2, sticky= 'w')
    enrty_timebase_scale.grid(row= 0, column= 4, padx= 5, pady= 2, sticky= 'w')
    button_timebase_scale_check.grid(row= 0, column= 5, padx= 5, pady= 2, sticky= 'w')

    label_voltage_offset.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'w')
    combobox_voltage_offset.grid(row= 1, column= 1, padx= 5, pady= 2, sticky= 'w')
    button_voltage_offset_check.grid(row= 1, column= 2, padx= 5, pady= 2, sticky= 'w')

    label_timebase_offset.grid(row= 1, column= 3, padx= 5, pady= 2, sticky= 'w')
    enrty_timebase_offset.grid(row= 1, column= 4, padx= 5, pady= 2, sticky= 'w')
    button_timebase_offset_check.grid(row= 1, column= 5, padx= 5, pady= 2, sticky= 'w')

    label_trigger_channel.grid(row= 2, column= 0, padx= 5, pady= 2, sticky= 'w')
    combobox_trigger_channel.grid(row= 2, column= 1, padx= 5, pady= 2, sticky= 'w')
    label_trigger_level.grid(row= 3, column= 0, padx= 5, pady= 2, sticky= 'w')
    combobox_trigger_level.grid(row= 3, column= 1, padx= 5, pady= 2, sticky= 'w')
    button_trigger_check.grid(row= 3, column= 2, padx= 5, pady= 2, sticky= 'w')

    label_wfm_intensity.grid(row= 2, column= 3, padx= 5, pady= 2, sticky= 'w')
    entry_wfm_intensity.grid(row= 2, column= 4, padx= 5, pady= 2, sticky= 'w')
    button_wfm_intensity.grid(row= 2, column= 5, padx= 5, pady= 2, sticky= 'w')
    button_set_intensity_50.grid(row= 3, column= 4, padx= 5, pady= 2, sticky= 'e', columnspan= 2)

    label_label_type.grid(row= 4, column= 0, padx= 5, pady= 2, sticky= 'w')
    radiobutton_label.grid(row= 4, column= 1, padx= 5, pady= 2, sticky= 'w')
    radiobutton_bookmark.grid(row= 4, column= 2, padx= 5, pady= 2, sticky= 'w')

    label_label_name.grid(row= 5, column= 0, padx= 5, pady= 2, sticky= 'w', columnspan= 3)
    enrty_label_name.grid(row= 5, column= 1, padx= 5, pady= 2, sticky= 'ew', columnspan= 3)
    button_add_label.grid(row= 5, column= 4, padx= 5, pady= 2, sticky= 'w')
    button_del_label.grid(row= 5, column= 5, padx= 5, pady= 2, sticky= 'w')

    # Save Image grid
    label_save_img_pc_folder.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    enrty_save_img_pc_folder.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'ew')
    button_img_pc_folder_browse.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'w')

    label_save_img_name.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'w')
    enrty_save_img_name.grid(row= 1, column= 1, padx= 5, pady= 2, sticky= 'ew')
    button_img_name_save.grid(row= 1, column= 2, padx= 5, pady= 2, sticky= 'w')

    # Setup File grid
    label_setup_locaiton.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    radiobutton_setup_location_desktop.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'w')
    radiobutton_setup_location_server.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'w')

    label_save_scope_folder.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'w')
    enrty_save_scope_folder.grid(row= 1, column= 1, padx= 5, pady= 2, sticky= 'ew', columnspan= 3)
    button_scope_folder_browse.grid(row= 1, column= 4, padx= 5, pady= 2, sticky= 'w')

    label_file_name.grid(row= 2, column= 0, padx= 5, pady= 2, sticky= 'w')
    enrty_file_name.grid(row= 2, column= 1, padx= 5, pady= 2, sticky= 'ew', columnspan= 3)
    button_file_name_save.grid(row= 2, column= 4, padx= 5, pady= 2, sticky= 'w')

    button_file_name_load.grid(row= 2, column= 5, padx= 5, pady= 2, sticky= 'w')
    cbheckbutton_setup_label.grid(row= 2, column= 6, padx= 5, pady= 2, sticky= 'w')

    # Extract Results grid
    button_get_results.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    rb_mean_result.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'w')
    rb_minmax_result.grid(row= 2, column= 0, padx= 5, pady= 2, sticky= 'w')
    
    label_result_type_0.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'w')
    label_result_type_1.grid(row= 1, column= 1, padx= 5, pady= 2, sticky= 'w')
    label_result_type_2.grid(row= 2, column= 1, padx= 5, pady= 2, sticky= 'w')

    label_meas_name_1.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'w')
    text_result1_1.grid(row= 1, column= 2, padx= 5, pady= 2, sticky= 'w')
    text_result2_1.grid(row= 2, column= 2, padx= 5, pady= 2, sticky= 'w')

    label_meas_name_2.grid(row= 0, column= 3, padx= 5, pady= 2, sticky= 'w')
    text_result1_2.grid(row= 1, column= 3, padx= 5, pady= 2, sticky= 'w')
    text_result2_2.grid(row= 2, column= 3, padx= 5, pady= 2, sticky= 'w')

    label_meas_name_3.grid(row= 0, column= 4, padx= 5, pady= 2, sticky= 'w')
    text_result1_3.grid(row= 1, column= 4, padx= 5, pady= 2, sticky= 'w')
    text_result2_3.grid(row= 2, column= 4, padx= 5, pady= 2, sticky= 'w')

    label_meas_name_4.grid(row= 0, column= 5, padx= 5, pady= 2, sticky= 'w')
    text_result1_4.grid(row= 1, column= 5, padx= 5, pady= 2, sticky= 'w')
    text_result2_4.grid(row= 2, column= 5, padx= 5, pady= 2, sticky= 'w')

    label_meas_name_5.grid(row= 0, column= 6, padx= 5, pady= 2, sticky= 'w')
    text_result1_5.grid(row= 1, column= 6, padx= 5, pady= 2, sticky= 'w')
    text_result2_5.grid(row= 2, column= 6, padx= 5, pady= 2, sticky= 'w')

    label_meas_name_6.grid(row= 0, column= 7, padx= 5, pady= 2, sticky= 'w')
    text_result1_6.grid(row= 1, column= 7, padx= 5, pady= 2, sticky= 'w')
    text_result2_6.grid(row= 2, column= 7, padx= 5, pady= 2, sticky= 'w')


    ##### Notebook - PCIe Clock ##### 
    # Config. Frame ===================================================================================================================================
    label_frame_pcieclock_config= tk.LabelFrame(notebook_frame_pcieclock, text= 'Config.', background= frame_bg_color_2, fg= labelframe_word_color, font= ('Candara', 11, 'bold'),)

    # label_pcieclock_channel = tk.Label(label_frame_pcieclock_config, text= 'Channel', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12,),)
    # str_pcieclock_channel = tk.StringVar()
    # combobox_pcieclock_channel = ttk.Combobox(label_frame_pcieclock_config, width= 12, textvariable= str_pcieclock_channel, values= ['1', '2', '3', '4'])

    label_pcieclock_samplingrate = tk.Label(label_frame_pcieclock_config, text= 'Sampling Rate (Sa/s)', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12,),)
    str_pcieclock_samplingrate = tk.StringVar()
    combobox_pcieclock_samplingrate = ttk.Combobox(label_frame_pcieclock_config, width= 12, textvariable= str_pcieclock_samplingrate)
    commbobox_function(combobox= combobox_pcieclock_samplingrate, combobox_var= str_pcieclock_samplingrate, ini_dict_key= 'PCIeClockSamplingRate', ini_option_section= 'PCIe_Clock_Config', ini_option_key= 'PCIeClockSamplingRate', ini_selected_section= 'PCIe_Clock_Config_Selected_Values')

    # label_pcieclock_memory_depth = tk.Label(label_frame_pcieclock_config, text= 'Memory Depth (pts)', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12,),)
    # str_pcieclock_memory_depth = tk.StringVar()
    # enrty_pcieclock_memory_depth = tk.Entry(label_frame_pcieclock_config, width= 12, textvariable= str_pcieclock_memory_depth)

    label_pcieclock_voltage_scale = tk.Label(label_frame_pcieclock_config, text= 'Voltage Scale (V)', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12,),)
    str_pcieclock_voltage_scale = tk.StringVar()
    combobox_pcieclock_voltage_scale = ttk.Combobox(label_frame_pcieclock_config, width= 12, textvariable= str_pcieclock_voltage_scale)
    commbobox_function(combobox= combobox_pcieclock_voltage_scale, combobox_var= str_pcieclock_voltage_scale, ini_dict_key= 'PCIeClockVoltageScale', ini_option_section= 'PCIe_Clock_Config', ini_option_key= 'PCIeClockVoltageScale', ini_selected_section= 'PCIe_Clock_Config_Selected_Values')

    label_pcieclock_voltage_offset = tk.Label(label_frame_pcieclock_config, text= 'Voltage Offset (V)', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12,),)
    str_pcieclock_voltage_offset = tk.StringVar()
    combobox_pcieclock_voltage_offset = ttk.Combobox(label_frame_pcieclock_config, width= 12, textvariable= str_pcieclock_voltage_offset)
    commbobox_function(combobox= combobox_pcieclock_voltage_offset, combobox_var= str_pcieclock_voltage_offset, ini_dict_key= 'PCIeClockVoltageOffset', ini_option_section= 'PCIe_Clock_Config', ini_option_key= 'PCIeClockVoltageOffset', ini_selected_section= 'PCIe_Clock_Config_Selected_Values')

    label_pcieclock_timebase_scale = tk.Label(label_frame_pcieclock_config, text= 'Timebase Scale (s)', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 12,),)
    str_pcieclock_timebase_scale = tk.StringVar()
    enrty_pcieclock_timebase_scale = tk.Entry(label_frame_pcieclock_config, width= 12, textvariable= str_pcieclock_timebase_scale)

    boolvar_5G_LPF = tk.BooleanVar()    
    cbheckbutton_5G_LPF= tk.Checkbutton(label_frame_pcieclock_config, text= 'Add Bandwidth Limit (5GHz LPF)', variable= boolvar_5G_LPF, background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 11, 'bold'),)
    # cbheckbutton_5G_LPF.select()

    # button_pcieclock_calculate = tk.Button(label_frame_pcieclock_config, text='Calculate', width= 12, height= 1, command= lambda: '')
    button_pcieclock_voltage_scale_check = tk.Button(label_frame_pcieclock_config, text='Voltage Scale Check', height= 1, command= lambda: uxr.voltage_scale_check(
        voltage_scale= str_pcieclock_voltage_scale.get()
    ))

    button_pcieclock_voltage_offset_check = tk.Button(label_frame_pcieclock_config, text='Voltage Offset Check', height= 1, command= lambda: uxr.voltage_offset_check(
        voltage_offset= str_pcieclock_voltage_offset.get()
    ))
    
    button_pcieclock_setup = tk.Button(label_frame_pcieclock_config, text='Setup', width= 20, height= 2, command= lambda: uxr.setup_pcieclock_test(
        sampling_rate= str_pcieclock_samplingrate.get(),
        time_required= str_pcieclock_timebase_scale.get(), 
        is_low_pass_filter= boolvar_5G_LPF.get(), 
        voltage_scale= str_pcieclock_voltage_scale.get()
    ))

    # Control Frame ===================================================================================================================================
    label_frame_pcieclock_control= tk.LabelFrame(notebook_frame_pcieclock, text= 'Control', background= frame_bg_color_1, fg= labelframe_word_color, font= ('Candara', 11, 'bold'),)

    button_pcieclock_run = tk.Button(label_frame_pcieclock_control, text='RUN', width= 20, height= 2, command= lambda: uxr.run())
    button_pcieclock_stop = tk.Button(label_frame_pcieclock_control, text='STOP', width= 20, height= 2, command= lambda: uxr.stop())
    button_pcieclock_single = tk.Button(label_frame_pcieclock_control, text='SINGLE', width= 20, height= 2, command= lambda: uxr.single())
    button_pcieclock_clear_display = tk.Button(label_frame_pcieclock_control, text='Clear', width= 20, height= 2, command= lambda: uxr.clear_diaplay())
    # button_pcieclock_clear_display.config(state= 'disabled')
    button_pcieclock_autoscale = tk.Button(label_frame_pcieclock_control, text='Auto Scale', width= 20, height= 2, command= lambda: uxr.autoscale())
    button_pcieclock_autoscale.config(state= 'disabled')
    button_pcieclock_default = tk.Button(label_frame_pcieclock_control, text='Default', width= 20, height= 2, command= lambda: uxr.default())
    button_pcieclock_default.config(state= 'disabled')
    button_pcieclock_trigger_type = tk.Button(label_frame_pcieclock_control, text='Trigger Type', width= 20, height= 2, command= lambda: uxr.trig_type())

    def disable_button():
        if button_pcieclock_autoscale["state"] == 'normal':
            button_pcieclock_autoscale.config(state="disabled")
        else:
            button_pcieclock_autoscale.config(state="normal")
        if button_pcieclock_default["state"] == 'normal':
            button_pcieclock_default.config(state="disabled")
        else:
            button_pcieclock_default.config(state="normal")
        # if button_pcieclock_clear_display["state"] == 'normal':
        #     button_pcieclock_clear_display.config(state="disabled")
        # else:
        #     button_pcieclock_clear_display.config(state="normal")

    button_pcieclock_disable = tk.Button(label_frame_pcieclock_control, text= 'Disable', width= 20, height= 2, command= disable_button)

    # Save & Load Frame ===================================================================================================================================
    label_frame_pcieclock_save_load= tk.LabelFrame(notebook_frame_pcieclock, text= 'Save & Load', background= frame_bg_color_1, fg= labelframe_word_color, font= ('Candara', 11, 'bold'),)

    label_pcieclock_scope_locaiton= tk.Label(label_frame_pcieclock_save_load, text= 'Scope Location', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 12,),)
    int_pcieclock_scope_location = tk.IntVar()    
    radiobutton_pcieclock_scope_location_desktop= tk.Radiobutton(label_frame_pcieclock_save_load, text= 'Desktop', variable= int_pcieclock_scope_location, value= 1, background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)
    radiobutton_pcieclock_scope_location_desktop.select()
    radiobutton_pcieclock_scope_location_server= tk.Radiobutton(label_frame_pcieclock_save_load, text= 'Server', variable= int_pcieclock_scope_location, value= 2, background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)

    label_pcieclock_file_type= tk.Label(label_frame_pcieclock_save_load, text= 'File Type', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 12,),)
    int_pcieclock_file_type = tk.IntVar()    
    radiobutton_pcieclock_file_type_bin= tk.Radiobutton(label_frame_pcieclock_save_load, text= 'BIN File', variable= int_pcieclock_file_type, value= 1, background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)
    radiobutton_pcieclock_file_type_bin.select()
    radiobutton_pcieclock_file_type_setup= tk.Radiobutton(label_frame_pcieclock_save_load, text= 'Setup File', variable= int_pcieclock_file_type, value= 2, background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)

    label_pcieclock_scope_folder = tk.Label(label_frame_pcieclock_save_load, text= 'Folder (Scope)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)
    str_pcieclock_scope_folder = tk.StringVar()
    enrty_pcieclock_scope_folder = tk.Entry(label_frame_pcieclock_save_load, width= 80, textvariable= str_pcieclock_scope_folder)

    button_pcieclock_scope_folder_browse = tk.Button(label_frame_pcieclock_save_load, text='Browse', width= 12, height= 1, command= lambda: select_folder(entry_var= str_pcieclock_scope_folder))

    # label_pcieclock_pc_folder = tk.Label(label_frame_pcieclock_save_load, text= 'Folder (PC)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)
    # str_pcieclock_pc_folder = tk.StringVar()
    # enrty_pcieclock_pc_folder = tk.Entry(label_frame_pcieclock_save_load, width= 80, textvariable= str_pcieclock_pc_folder)

    # button_pcieclock_pc_folder_browse = tk.Button(label_frame_pcieclock_save_load, text='Browse', width= 12, height= 1, command= lambda: select_folder(entry_var= str_pcieclock_pc_folder))

    label_pcieclock_file_name = tk.Label(label_frame_pcieclock_save_load, text= 'File Name', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)
    str_pcieclock_file_name = tk.StringVar()
    enrty_pcieclock_file_name = tk.Entry(label_frame_pcieclock_save_load, width= 80, textvariable= str_pcieclock_file_name)

    button_pcieclock_save = tk.Button(label_frame_pcieclock_save_load, text='Save', width= 12, height= 1, command= lambda: uxr.save_setup_file_scope(
        folder= str_pcieclock_scope_folder.get(), 
        current_file_name= str_pcieclock_file_name.get(), 
        path_choice= int_pcieclock_scope_location.get(), 
        file_type_choice= int_pcieclock_file_type.get()
    ))
    
    button_pcieclock_load = tk.Button(label_frame_pcieclock_save_load, text='Load Setup File', height= 1, command= lambda: uxr.load_setup(
        folder= str_pcieclock_scope_folder.get(), 
        setup_name= str_pcieclock_file_name.get(), 
        label_choose_type= 2, 
        file_path_choice= int_pcieclock_scope_location.get()
    ))

    # PCIe Clock Grid ===================================================================================================================================

    # LabelFrame grid
    label_frame_pcieclock_config.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'nsew')
    label_frame_pcieclock_control.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'nsew')
    label_frame_pcieclock_save_load.grid(row= 2, column= 0, padx= 5, pady= 2, sticky= 'nsew')

    # Config. Grid
    # label_pcieclock_channel.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    # combobox_pcieclock_channel.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'w')

    label_pcieclock_samplingrate.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    combobox_pcieclock_samplingrate.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'w')

    label_pcieclock_timebase_scale.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'w')
    enrty_pcieclock_timebase_scale.grid(row= 0, column= 3, padx= 5, pady= 2, sticky= 'w')

    label_pcieclock_voltage_scale.grid(row= 0, column= 4, padx= 5, pady= 2, sticky= 'w')
    combobox_pcieclock_voltage_scale.grid(row= 0, column= 5, padx= 5, pady= 2, sticky= 'w')

    # label_pcieclock_memory_depth.grid(row= 1, column= 2, padx= 5, pady= 2, sticky= 'w')
    # enrty_pcieclock_memory_depth.grid(row= 1, column= 3, padx= 5, pady= 2, sticky= 'w')

    label_pcieclock_voltage_offset.grid(row= 0, column= 6, padx= 5, pady= 2, sticky= 'w')
    combobox_pcieclock_voltage_offset.grid(row= 0, column= 7, padx= 5, pady= 2, sticky= 'w')

    cbheckbutton_5G_LPF.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'w', columnspan= 3)
    # button_pcieclock_calculate.grid(row= 3, column= 3, padx= 5, pady= 2, sticky= 'w')

    button_pcieclock_setup.grid(row= 0, column= 8, padx= 5, pady= 2, sticky= 'w', rowspan= 2)
    button_pcieclock_voltage_scale_check.grid(row= 1, column= 4, padx= 5, pady= 2, sticky= 'w', columnspan= 2)
    button_pcieclock_voltage_offset_check.grid(row= 1, column= 6, padx= 5, pady= 2, sticky= 'w', columnspan= 2)

    # Control Grid
    button_pcieclock_run.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'nsew')
    button_pcieclock_stop.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'nsew')
    button_pcieclock_single.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'nsew')
    button_pcieclock_clear_display.grid(row= 0, column= 3, padx= 5, pady= 2, sticky= 'nsew')
    button_pcieclock_trigger_type.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'nsew')
    button_pcieclock_autoscale.grid(row= 1, column= 1, padx= 5, pady= 2, sticky= 'nsew')
    button_pcieclock_default.grid(row= 1, column= 2, padx= 5, pady= 2, sticky= 'nsew')
    button_pcieclock_disable.grid(row= 1, column= 3, padx= 7, pady= 2, sticky= 'nsew')

    # Save & Load Grid
    label_pcieclock_scope_locaiton.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    radiobutton_pcieclock_scope_location_desktop.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'w')
    radiobutton_pcieclock_scope_location_server.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'w')

    label_pcieclock_file_type.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'w')
    radiobutton_pcieclock_file_type_bin.grid(row= 1, column= 1, padx= 5, pady= 2, sticky= 'w')
    radiobutton_pcieclock_file_type_setup.grid(row= 1, column= 2, padx= 5, pady= 2, sticky= 'w')

    label_pcieclock_scope_folder.grid(row= 2, column= 0, padx= 5, pady= 2, sticky= 'w')
    enrty_pcieclock_scope_folder.grid(row= 2, column= 1, padx= 5, pady= 2, sticky= 'ew', columnspan= 5)
    button_pcieclock_scope_folder_browse.grid(row= 2, column= 6, padx= 5, pady= 2, sticky= 'w')

    # label_pcieclock_pc_folder.grid(row= 3, column= 0, padx= 5, pady= 2, sticky= 'w')
    # enrty_pcieclock_pc_folder.grid(row= 3, column= 1, padx= 5, pady= 2, sticky= 'ew', columnspan= 5)
    # button_pcieclock_pc_folder_browse.grid(row= 3, column= 6, padx= 5, pady= 2, sticky= 'w')

    label_pcieclock_file_name.grid(row= 3, column= 0, padx= 5, pady= 2, sticky= 'w')
    enrty_pcieclock_file_name.grid(row= 3, column= 1, padx= 5, pady= 2, sticky= 'ew', columnspan= 5)

    button_pcieclock_save.grid(row= 3, column= 6, padx= 5, pady= 2, sticky= 'w')
    button_pcieclock_load.grid(row= 3, column= 7, padx= 5, pady= 2, sticky= 'w')


    initialize()

    notebook.add(notebook_frame_realtime, text= 'Real-time Eye')
    notebook.add(notebook_frame_pcieclock, text= 'PCIe 100MHz Clock')
    notebook.pack(padx= 10, pady= 10, fill= 'both', expand= True)

    window.protocol('WM_DELETE_WINDOW', close_window)

    uxr= UXR(scope_ip= scope_ip)

    window.mainloop()


# 選擇 Scope IP ============================================================================================================================================

config_initial = configparser.ConfigParser()
config_initial.optionxform = str
config_initial.read(os.path.join(os.path.dirname(__file__), 'InitConfig_setup.ini'), encoding='UTF-8',)

scope_ips= []
for i in range(len(config_initial['Scope_IPs'])):
    scope_ips.append(config_initial['Scope_IPs'][f'IP_{i}'])
scope_ips.append('')

id_window = tk.Tk()
id_window.title(window_name)
id_window.resizable(width= False, height= False)
id_window.geometry('390x160+500+150')
id_window.configure(background= "#D5D4D4")

l_scope_ip = tk.Label(id_window, text= 'Enter Scope IP', background= '#D5D4D4', fg= "#3A3A3A", font= ('Candara', 12, 'bold'),)
str_scope_ip = tk.StringVar()
cb_scope_ip = ttk.Combobox(id_window, textvariable= str_scope_ip, values= scope_ips)
b_scope_ip = tk.Button(id_window, text= 'OK', width= 10, height= 2, command= lambda: show_main_window(old_scope_ips= scope_ips), )

l_ip = tk.Label(id_window, text= '★★★ 確認電腦IP與Scope在同一網域 ★★★', background= '#D5D4D4', fg= '#F6044D', font= ('Candara', 14, 'bold'),)

l_scope_ip.pack(padx= 5, pady= 5)
cb_scope_ip.pack(padx= 5, pady= 5)
b_scope_ip.pack(padx= 5, pady= 5)
l_ip.pack(padx= 5, pady= 5)

id_window.mainloop()
