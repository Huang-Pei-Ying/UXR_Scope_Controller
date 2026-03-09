import pyvisa
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk
import configparser
import os
from decimal import Decimal
import re
import time
import sys
import numpy as np

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

        select_VoltScale = config_initial['Scale_Offset_Selected_Values']['VoltScale']
        select_VoltOffset = config_initial['Scale_Offset_Selected_Values']['VoltOffset']
        TimebaseScale = config_initial['Scale_Offset_Config']['TimebaseScale']
        TimebaseOffset = config_initial['Scale_Offset_Config']['TimebaseOffset']
        select_TriggerLevel = config_initial['Scale_Offset_Selected_Values']['TriggerLevel']
        TriggerChan = config_initial['Scale_Offset_Config']['TriggerChan']
        WfmIntensity = config_initial['Scale_Offset_Config']['WfmIntensity']

        select_GeneralTopPercent = config_initial['Threshold_Selected_Values']['GeneralTopPercent']
        select_GeneralMiddlePercent = config_initial['Threshold_Selected_Values']['GeneralMiddlePercent']
        select_GeneralBasePercent = config_initial['Threshold_Selected_Values']['GeneralBasePercent']
        select_GeneralTop = config_initial['Threshold_Selected_Values']['GeneralTop']
        select_GeneralMiddle = config_initial['Threshold_Selected_Values']['GeneralMiddle']
        select_GeneralBase = config_initial['Threshold_Selected_Values']['GeneralBase']
        
        RealTimeSourceChannel = config_initial['Real_Time_Selected_Values']['RealTimeSourceChannel']
        select_RealTimeFrequency = config_initial['Real_Time_Selected_Values']['RealTimeFrequency']
        RealTimeSamplingRate = config_initial['Real_Time_Selected_Values']['RealTimeSamplingRate']
        RealTimeMemoryDepth = config_initial['Real_Time_Selected_Values']['RealTimeMemoryDepth']
        RealTimeHistogram = config_initial['Real_Time_Selected_Values']['RealTimeHistogram']
        RealTimeVoltageMeas = config_initial['Real_Time_Selected_Values']['RealTimeVoltageMeas']
        RealTimeMask = config_initial['Real_Time_Selected_Values']['RealTimeMask']
        RealTimeMaskPath = config_initial['Real_Time_Selected_Values']['RealTimeMaskPath']

        SamplingRate = config_initial['Acquisition']['SamplingRate']
        MemoryDepth = config_initial['Acquisition']['MemoryDepth']

        ChanLabel1 = config_initial['Lable_Setup_Config']['ChanLabel1']
        ChanLabel2 = config_initial['Lable_Setup_Config']['ChanLabel2']
        ChanLabel3 = config_initial['Lable_Setup_Config']['ChanLabel3']
        ChanLabel4 = config_initial['Lable_Setup_Config']['ChanLabel4']
        WMeLabel1 = config_initial['Lable_Setup_Config']['WMeLabel1']
        WMeLabel2 = config_initial['Lable_Setup_Config']['WMeLabel2']
        WMeLabel3 = config_initial['Lable_Setup_Config']['WMeLabel3']
        WMeLabel4 = config_initial['Lable_Setup_Config']['WMeLabel4']

        ChanSingle = config_initial['Chan_Delta']['ChanSingle']

        SaveImgFolder = config_initial['Save_Setup_Config']['SaveImgFolder']
        SaveImgLocation = config_initial['Save_Setup_Config']['SaveImgLocation']
        SaveImgPCFolder = config_initial['Save_Setup_Config']['SaveImgPCFolder']
        SaveImgName = config_initial['Save_Setup_Config']['SaveImgName']
        SaveWMeFolder = config_initial['Save_Setup_Config']['SaveWMeFolder']
        SaveWMeLocation = config_initial['Save_Setup_Config']['SaveWMeLocation']
        SaveWMePCFolder = config_initial['Save_Setup_Config']['SaveWMePCFolder']
        SaveWMeName = config_initial['Save_Setup_Config']['SaveWMeName']

        LoadWMe1 = config_initial['Load_WMemory_Setup_Config']['LoadWMe1']
        LoadWMe2 = config_initial['Load_WMemory_Setup_Config']['LoadWMe2']
        LoadWMe3 = config_initial['Load_WMemory_Setup_Config']['LoadWMe3']
        LoadWMe4 = config_initial['Load_WMemory_Setup_Config']['LoadWMe4']
        LoadSetup = config_initial['Load_WMemory_Setup_Config']['LoadSetup']

        str_volt_scale.set(value= select_VoltScale)
        str_volt_offset.set(value= select_VoltOffset)
        str_time_scale.set(value= TimebaseScale)
        str_time_offset.set(value= TimebaseOffset)
        str_trigger_level.set(value= select_TriggerLevel)
        str_trigger_chan.set(value= TriggerChan)
        str_wfm_intensity.set(value= WfmIntensity)

        str_gen_top_percent.set(value= select_GeneralTopPercent)
        str_gen_mid_percent.set(value= select_GeneralMiddlePercent)
        str_gen_base_percent.set(value= select_GeneralBasePercent)
        str_gen_top.set(value= select_GeneralTop)
        str_gen_mid.set(value= select_GeneralMiddle)
        str_gen_base.set(value= select_GeneralBase)

        int_source_chan.set(value= int(RealTimeSourceChannel))
        str_realtime_freq.set(value= select_RealTimeFrequency)
        str_realtime_sampling_rate.set(value= RealTimeSamplingRate)
        str_realtime_memory_depth.set(value= RealTimeMemoryDepth)
        boolvar_histogram.set(value= RealTimeHistogram)
        boolvar_voltage_meas.set(value= RealTimeVoltageMeas)
        boolvar_mask_test.set(value= RealTimeMask)
        str_mask.set(value= RealTimeMaskPath)

        str_sampling_rate.set(value= SamplingRate)
        str_memory_depth.set(value= MemoryDepth)

        str_label_1.set(value= ChanLabel1)
        str_label_2.set(value= ChanLabel2)
        str_label_3.set(value= ChanLabel3)
        str_label_4.set(value= ChanLabel4)
        str_label_5.set(value= WMeLabel1)
        str_label_6.set(value= WMeLabel2)
        str_label_7.set(value= WMeLabel3)
        str_label_8.set(value= WMeLabel4)

        str_ch.set(value= str(ChanSingle))
        # int_ch_delta_start.set(value= int(ChanStart))
        # int_ch_delta_stop.set(value= int(ChanStop))

        str_image_folder.set(value= SaveImgFolder)
        int_img_path_choice.set(value= SaveImgLocation)
        str_image_pc_folder.set(value= SaveImgPCFolder)
        str_image.set(value= SaveImgName)
        str_WMe_folder.set(value= SaveWMeFolder)
        int_wme_path_choice.set(value= SaveWMeLocation)
        str_WMe_pc_folder.set(value= SaveWMePCFolder)
        str_other_file.set(value= SaveWMeName)

        str_WMe1.set(value= LoadWMe1)
        str_WMe2.set(value= LoadWMe2)
        str_WMe3.set(value= LoadWMe3)
        str_WMe4.set(value= LoadWMe4)
        str_setup.set(value= LoadSetup)


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
                
        ### Acquisition Related ###
        def sampling_rate_acquire(self, rate): # 科學記號
            self.inst.write(f':ACQuire:SRATe:ANALog {rate}')
            time.sleep(0.05)

        def memory_depth_acquire(self, points_value: int):
            self.inst.write(f':ACQuire:POINts:ANALog {points_value}')
            time.sleep(0.05)

        # def meas_all_edge(self):
        #     ans= self.inst.query(':ANALyze:AEDGes?')
        #     time.sleep(0.05)
        #     if ans == '0\n':
        #         b_meas_all_edge['text'] = "Meas All Edge: ON"
        #         self.inst.write(f':ANALyze:AEDGes 1')
        #         time.sleep(0.05)
        #     else:
        #         b_meas_all_edge['text'] = "Meas All Edge: OFF"
        #         self.inst.write(f':ANALyze:AEDGes 0')
        #         time.sleep(0.05)
        
        ## Threshold Reslated ###
        def RF_threshold(self, rf_top, rf_base, rf_top_percent, rf_base_percent):
            if int_rf_thres.get() == 1:
                self.inst.write(f':MEASure:THResholds:RFALl:METHod ALL,PERCent')
                time.sleep(0.05)
                self.inst.write(f':MEASure:THResholds:RFALl:PERCent ALL,{rf_top_percent},{(float(rf_top_percent)+float(rf_base_percent))/2},{rf_base_percent}')
                time.sleep(0.05)
            elif int_rf_thres.get() == 2:
                self.inst.write(f':MEASure:THResholds:RFALl:METHod ALL,ABSolute')
                time.sleep(0.05)
                self.inst.write(f':MEASure:THResholds:RFALl:ABSolute ALL,{rf_top},{(float(rf_top)+float(rf_base))/2},{rf_base}')
                time.sleep(0.05)

        def gen_threshold(self, g_top, g_middle, g_base, g_top_percent, g_middle_percent, g_base_percent):
            if int_gen_thres.get() == 1:
                do_the_judge= False
                if float(g_top_percent) <= float(g_middle_percent):
                    g_top_percent= Decimal(g_middle_percent) + Decimal('0.1')
                    combobox_gen_top_percent.config(foreground= 'red')
                    combobox_gen_mid_percent.config(foreground= 'red')
                    do_the_judge= True
                if float(g_middle_percent) <= float(g_base_percent):
                    g_base_percent= Decimal(g_middle_percent) - Decimal('0.1')
                    combobox_gen_base_percent.config(foreground= 'red')
                    combobox_gen_mid_percent.config(foreground= 'red')
                    do_the_judge= True
                if not do_the_judge:
                    combobox_gen_top_percent.config(foreground= 'black')
                    combobox_gen_mid_percent.config(foreground= 'black')
                    combobox_gen_base_percent.config(foreground= 'black')

                self.inst.write(f':MEASure:THResholds:GENeral:METHod ALL,PERCent')
                time.sleep(0.05)
                self.inst.write(f':MEASure:THResholds:GENeral:PERCent ALL,{g_top_percent},{g_middle_percent},{g_base_percent}')
                time.sleep(0.05)
            elif int_gen_thres.get() == 2:
                do_the_judge= False
                if float(g_top) <= float(g_middle):
                    g_top= Decimal(g_middle) + Decimal('0.01')
                    combobox_gen_top.config(foreground= 'red')
                    combobox_gen_mid.config(foreground= 'red')
                    do_the_judge= True
                if float(g_middle) <= float(g_base):
                    g_base= Decimal(g_middle) - Decimal('0.01')
                    combobox_gen_base.config(foreground= 'red')
                    combobox_gen_mid.config(foreground= 'red')
                    do_the_judge= True
                if not do_the_judge:
                    combobox_gen_top.config(foreground= 'black')
                    combobox_gen_mid.config(foreground= 'black')
                    combobox_gen_base.config(foreground= 'black')

                self.inst.write(f':MEASure:THResholds:GENeral:METHod ALL,ABSolute')
                time.sleep(0.05)
                self.inst.write(f':MEASure:THResholds:GENeral:ABSolute ALL,{g_top},{g_middle},{g_base}')
                time.sleep(0.05)

        ### Scale Related ###
        def volt_check(self, scale, offset): # 科學記號
            display_dict= self.judge_chan_wme()
            for chan in display_dict['CHANnel']:
                self.inst.write(f':CHANnel{chan}:SCALe {scale}')
                time.sleep(0.05)
                self.inst.write(f':CHANnel{chan}:OFFSet {offset}')
                time.sleep(0.05)
            for wme in display_dict['WMEMory']:
                self.inst.write(f':WMEMory{wme}:YRANge {float(scale)*8}')
                time.sleep(0.05)
                self.inst.write(f':WMEMory{wme}:YOFFset {offset}')
                time.sleep(0.05)

        def timebase_position_check(self, position): # 科學記號
            self.inst.write(f':TIMebase:POSition {position}')
            time.sleep(0.05)

        def timebase_scale_check(self, scale): # 科學記號
            self.inst.write(f':TIMebase:SCALe {scale}')
            time.sleep(0.05)

        def trig_check(self, chan, level):
            res= self.inst.query(f':CHANnel{chan}:DISPlay?')
            time.sleep(0.05)
            if not res == '1\n':
                self.inst.write(f':CHANnel{chan}:DISPlay ON')
                time.sleep(0.05)
            self.inst.write(f':TRIGger:EDGE:SOURce CHANnel{chan}')
            time.sleep(0.05)
            self.inst.write(f':TRIGger:LEVel CHANnel{chan},{level}')
            time.sleep(0.05)
            if not res == '1\n':
                self.inst.write(f':CHANnel{chan}:DISPlay OFF')
                time.sleep(0.05)

        def intensity_check(self, intensity_value):
            self.inst.write(f'SYSTem:CONTrol "WaveformBrt -1 {intensity_value}"')
            time.sleep(0.05)

        ### Display Related ###
        def display_Chan(self, chan, bookmark, choose_type):
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
                self.add_bookmark(choose_type= choose_type,bookmark= bookmark, chan= chan)

        def display_WMemory(self, chan, bookmark, choose_type):
            res= self.inst.query(f':WMEMory{chan}:DISPlay?')
            time.sleep(0.05)
            if res == '1\n':
                self.inst.write(f':WMEMory{chan}:DISPlay OFF')
                time.sleep(0.05)
                try:
                    self.inst.write(f':DISPlay:BOOKmark{chan+4}:DELete')
                    time.sleep(0.05)
                except:
                    pass
            else:
                self.inst.write(f':WMEMory{chan}:DISPlay ON')
                time.sleep(0.05)
                self.add_bookmark(choose_type= choose_type, bookmark= bookmark, chan= chan+4)
        
        ### Measurement Related ###
        def called_meas_function(self, chan, command_templates: dict):
            display_dict= self.judge_chan_wme()
            for key in command_templates:
                if chan in display_dict[key]:
                    self.inst.write(command_templates[key].format(chan))
                    time.sleep(0.05)            
        
        def freq(self, chan):
            command_templates = {
                'CHANnel': ':MEASure:FREQuency CHANnel{}',
                'WMEMory': ':MEASure:FREQuency WMEMory{}'
            }            
            self.called_meas_function(chan= chan, command_templates= command_templates)

        def period(self, chan):
            command_templates = {
                'CHANnel': ':MEASure:PERiod CHANnel{}',
                'WMEMory': ':MEASure:PERiod WMEMory{}'
            }            
            self.called_meas_function(chan= chan, command_templates= command_templates)
    
        # def dutycycle(self, chan):
        #     command_templates = {
        #         'CHANnel': ':MEASure:DUTYcycle CHANnel{}',
        #         'WMEMory': ':MEASure:DUTYcycle WMEMory{}'
        #     }            
        #     self.called_meas_function(chan= chan, command_templates= command_templates)

        # def slewrate(self, chan, direction):
        #     display_dict= self.judge_chan_wme()
        #     for cha in display_dict['CHANnel']:
        #         if cha == chan:
        #             self.inst.write(f':MEASure:SLEWrate CHANnel{cha},{direction}')
        #             time.sleep(0.05)
        #             self.inst.write(f':MEASure:NAME MEAS1,"{direction} Slew Rate({cha})"')
        #             time.sleep(0.05)
        #     for wme in display_dict['WMEMory']:
        #         if wme == chan:
        #             self.inst.write(f':MEASure:SLEWrate WMEMory{wme},{direction}')
        #             time.sleep(0.05)
        #             self.inst.write(f':MEASure:NAME MEAS1,"{direction} Slew Rate(m{wme})"')
        #             time.sleep(0.05)

        # def tH(self, chan):
        #     command_templates = {
        #         'CHANnel': ':MEASure:PWIDth CHANnel{}',
        #         'WMEMory': ':MEASure:PWIDth WMEMory{}'
        #     }            
        #     self.called_meas_function(chan= chan, command_templates= command_templates)  

        # def tL(self, chan):
        #     command_templates = {
        #         'CHANnel': ':MEASure:NWIDth CHANnel{}',
        #         'WMEMory': ':MEASure:NWIDth WMEMory{}'
        #     }            
        #     self.called_meas_function(chan= chan, command_templates= command_templates)  

        # def tR(self, chan):
        #     command_templates = {
        #         'CHANnel': ':MEASure:RISetime CHANnel{}',
        #         'WMEMory': ':MEASure:RISetime WMEMory{}'
        #     }            
        #     self.called_meas_function(chan= chan, command_templates= command_templates)              

        # def tF(self, chan):
        #     command_templates = {
        #         'CHANnel': ':MEASure:FALLtime CHANnel{}',
        #         'WMEMory': ':MEASure:FALLtime WMEMory{}'
        #     }            
        #     self.called_meas_function(chan= chan, command_templates= command_templates)              

        def VIH(self, chan):
            command_templates = {
                'CHANnel': ':MEASure:VTOP CHANnel{}',
                'WMEMory': ':MEASure:VTOP WMEMory{}'
            }            
            self.called_meas_function(chan= chan, command_templates= command_templates)              

        def VIL(self, chan):
            command_templates = {
                'CHANnel': ':MEASure:VBASe CHANnel{}',
                'WMEMory': ':MEASure:VBASe WMEMory{}'
            }            
            self.called_meas_function(chan= chan, command_templates= command_templates)              

        # def tSU_tHO(self, edge_1, num_1, pos_1, edge_2, num_2, pos_2, chan, chan_start, chan_stop):
        #     displayed_dict= self.judge_chan_wme()
        #     for format in displayed_dict:
        #         for channel in displayed_dict[format]:
        #             if chan_start == channel:
        #                 res_start= f'{format}'
        #             if chan_stop == channel:
        #                 res_stop= f'{format}'

        #     if chan == 2:
        #         self.inst.write(f':MEASure:DELTatime:DEFine {edge_1},{num_1},{pos_1},{edge_2},{num_2},{pos_2}')
        #         time.sleep(0.05)
        #         self.inst.write(f':MEASure:DELTatime {res_start}{chan_start}, {res_stop}{chan_stop}')
        #         time.sleep(0.05)
        #     else:
        #         pass

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

        def trig_slope(self):
            res= self.inst.query(f':TRIGger:EDGE:SLOPe?')
            time.sleep(0.05)
            if res == 'POS\n':
                self.inst.write(':TRIGger:EDGE:SLOPe NEGative')
                time.sleep(0.05)
            else:
                self.inst.write(':TRIGger:EDGE:SLOPe POSitive')
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

        def add_bookmark(self, choose_type, bookmark, chan):
            if choose_type == 1:
                self.inst.write(f':DISPlay:BOOKmark:DELete:ALL')
                time.sleep(0.05)
                self.add_label(chan= chan, label= bookmark)
                return
            else:
                self.inst.write(f':DISPlay:LABel OFF')
                time.sleep(0.05)
                if bookmark == '':
                    self.inst.write(f':DISPlay:BOOKmark{chan}:DELete')

                else:
                    display_dict= self.judge_chan_wme()    
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
                    for cha in display_dict['CHANnel']:
                        if cha == chan:
                            self.inst.write(f':DISPlay:BOOKmark{chan}:DELete')
                            time.sleep(0.05)
                            self.inst.write(f':DISPlay:BOOKmark{chan}:SET NONE,"{bookmark}",CHANnel{chan},"",1')
                            time.sleep(0.05)
                            self.inst.write(f':DISPlay:BOOKmark{chan}:XPOSition {0.01}')
                            time.sleep(0.05)
                            bookmark_display_list.append(count)
                            self.inst.write(f':DISPlay:BOOKmark{chan}:YPOSition {2+interval*count}E-02')
                            time.sleep(0.05)
                        count+=1
                    for wme in display_dict['WMEMory']:
                        if wme == chan-4:
                            self.inst.write(f':DISPlay:BOOKmark{chan}:DELete')
                            time.sleep(0.05)
                            self.inst.write(f':DISPlay:BOOKmark{chan}:SET NONE,"{bookmark}",WMEMory{chan-4},"",1')
                            time.sleep(0.05)
                            self.inst.write(f':DISPlay:BOOKmark{chan}:XPOSition {0.01}')
                            time.sleep(0.05)
                            bookmark_display_list.append(count)
                            self.inst.write(f':DISPlay:BOOKmark{chan}:YPOSition {2+interval*count}E-02')
                            time.sleep(0.05)
                        count+=1

        def delete_bookmark(self, chan, choose_type):
            if choose_type == 1:
                self.inst.write(f':DISPlay:LABel OFF')
                time.sleep(0.05)
            else:
                self.inst.write(f':DISPlay:BOOKmark{chan}:DELete')
                time.sleep(0.05)

        def add_marker(self):
            tuple_marker = (boolvar_marker_1, boolvar_marker_2, boolvar_marker_3, boolvar_marker_4, boolvar_marker_5, boolvar_marker_6, 
                            # boolvar_marker_7, boolvar_marker_8, boolvar_marker_9, boolvar_marker_10, boolvar_marker_11, boolvar_marker_12, 
                            )
        
            for i, boolvar in enumerate(tuple_marker):
                self.inst.write(f':MARKer:MEASurement:MEASurement MEASurement{i+1},OFF')
                time.sleep(0.05)

            for i, boolvar in enumerate(tuple_marker):
                if boolvar.get():
                    self.inst.write(f':MARKer:MEASurement:MEASurement MEASurement{i+1},ON')
                    time.sleep(0.05)
        
        def delete_marker(self):
            tuple_marker = (boolvar_marker_1, boolvar_marker_2, boolvar_marker_3, boolvar_marker_4, boolvar_marker_5, boolvar_marker_6, 
                            # boolvar_marker_7, boolvar_marker_8, boolvar_marker_9, boolvar_marker_10, boolvar_marker_11, boolvar_marker_12, 
                            )
        
            for i, boolvar in enumerate(tuple_marker):
                if boolvar.get():
                    self.inst.write(f':MARKer:MEASurement:MEASurement MEASurement{i+1},OFF')
                    time.sleep(0.05)

        def add_label(self, chan, label):
            display_dict= self.judge_chan_wme()
            if label == '':
                self.inst.write(f':DISPlay:LABel OFF')
                time.sleep(0.05)
            else:
                self.inst.write(f':DISPlay:LABel ON')
                time.sleep(0.05)
                for cha in display_dict['CHANnel']:
                    if cha == chan:
                        self.inst.write(f':CHANnel{chan}:LABel "{label}"')
                        time.sleep(0.05)
                for wme in display_dict['WMEMory']:
                    if wme == chan-4:
                        self.inst.write(f':WMEMory{chan-4}:LABel "{label}"')
                        time.sleep(0.05)

        ### Save Related ###
        def load_wmemory(self, chan, folder, wme_name, file_path_choice):
            self.inst.write(f':WMEMory:TIETimebase 1')
            time.sleep(0.05)
            self.inst.write(f':DISPlay:SCOLor WMEMory1,17,100,100')
            time.sleep(0.05)
            self.inst.write(f':DISPlay:SCOLor WMEMory2,38,100,84')
            time.sleep(0.05)
            self.inst.write(f':DISPlay:SCOLor WMEMory3,60,80,100')
            time.sleep(0.05)
            self.inst.write(f':DISPlay:SCOLor WMEMory4,94,100,100')
            time.sleep(0.05)
            
            if file_path_choice == 2:
                total_folder_path = folder
            else:
                total_folder_path = f"C:/Users/Administrator/Desktop/{folder}"

            self.inst.write(f':DISK:LOAD "{total_folder_path}/{wme_name}.h5",WMEMory{chan},OFF')
            time.sleep(0.05)

        def load_setup(self, folder, setup_name, scale, position, choose_type, file_path_choice):
            if file_path_choice == 2:
                total_folder_path = folder
            else:
                total_folder_path = f"C:/Users/Administrator/Desktop/{folder}"
            self.inst.write(f':DISK:LOAD "{total_folder_path}/{setup_name}.set"')
            time.sleep(0.05)
            if boolvar_setup_timebase.get() == True:
                self.timebase_scale_check(scale= scale)
                self.timebase_position_check(position= position)
            if boolvar_setup_label.get() == True:
                label_content = [
                    str_label_1, str_label_2, str_label_3, str_label_4, 
                    str_label_5, str_label_6, str_label_7, str_label_8, 
                    ]
                for i in range(8):
                    self.add_bookmark(choose_type= choose_type, bookmark= label_content[i].get().rstrip('\n'), chan= i+1)
        
        def clear_wmemory(self, chan, string):
            self.inst.write(f':WMEMory{chan}:CLEar')
            time.sleep(0.05)
            string.set('')

        def save_image_scope(self, folder, image_name, path_choice):
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

            # CDIRectory會害存圖卡死 orz

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
            # 使用正則表達式來匹配所有 .png 檔案名稱
            png_files = re.findall(r'\b[\w-]+\.(?:png)\b', folder_content)

            for file_name in png_files:
                if f'{image_name}.png' == file_name:
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

            self.inst.write(f':DISK:SAVE:IMAGe "{folder_total_path}/{image_name}",PNG,SCReen,OFF,NORMal,OFF')
            time.sleep(0.05)

        def save_waveform_pc(self, folder, pc_folder, file_name):            

            full_path = rf"C:/Users/Administrator/Desktop/{folder}/{file_name}.png"
            full_path = full_path.replace('\\', '/')
            # print(full_path)
            data = b''
            message = f':DISK:GETFILE? "{full_path}"'
            data = self.inst.query_binary_values(message=message, datatype='B', header_fmt='ieee', container=bytes)
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
           
            with open(f"{pc_folder}/{file_name}.png", 'wb') as f:
                f.write(data)

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
            
            f_img = open(f"{pc_folder}/{file_name}.png", "wb")
            f_img.write(bytearray(screen_data))
            f_img.close()

        def save_other_file_scope(self, chan, folder, current_file_name, ext_type, path_choice):
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

            # 判斷存.h5或.set
            if ext_type == 1:
                # 使用正則表達式來匹配所有 .h5 檔案名稱
                files = re.findall(r'\b[\w-]+\.(?:h5)\b', folder_content)
                ext= 'h5'
                command= f':DISK:SAVE:WAVeform CHANnel{chan},"{folder_total_path}/{current_file_name}",H5,OFF'
            else:
                # 使用正則表達式來匹配所有 .set 檔案名稱
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

        def save_wmemory_pc(self, folder, pc_folder, file_name, ext_type):
            if ext_type == 1:
                ext = 'h5'
            else:
                ext = 'set'

            full_path = f"C:/Users/Administrator/Desktop/{folder}/{file_name}.{ext}"
            data = b''
            message = ':DISK:GETFILE? "' + full_path + '"'
            data = self.inst.query_binary_values(message= message, datatype= 'B', header_fmt= 'ieee', container= bytes)
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

            if os.path.exists(f"{pc_folder}/{file_name}.{ext}"):
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
           
            with open(f"{pc_folder}/{file_name}.{ext}", 'wb') as f:
                f.write(data)

        ### Display Related ###
        def judge_chan_wme(self):
            display_dict= {'CHANnel': [],'WMEMory': []}
            for i in range(1, 5):
                chan_res= self.inst.query(f':CHANnel{i}:DISPlay?')
                time.sleep(0.05)
                wme_res= self.inst.query(f':WMEMory{i}:DISPlay?')
                time.sleep(0.05)

                if chan_res == '1\n' and not wme_res == '1\n':
                    display_dict['CHANnel'].append(i)
                    # return 'CHANnel'
                if not chan_res == '1\n' and wme_res == '1\n':
                    display_dict['WMEMory'].append(i)
                    # return 'WMEMory'
                if chan_res == '1\n' and wme_res == '1\n':
                    display_dict['CHANnel'].append(i)
                    display_dict['WMEMory'].append(i)

            return display_dict

        ### Result Related ###
        def get_results(self):
            meas_name= ['', '', '']
            mean= ['', '', '']
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
                if divmod(index, 7)[1] == 2:
                    if measurement_type == 0:
                        final_result= self.judge_volt_unit(value= value)
                    elif measurement_type == 1:
                        slew= False
                        final_result= self.judge_time_unit(value= value, slew= slew)
                    elif measurement_type == 2:
                        slew= True
                        final_result= self.judge_time_unit(value= value, slew= slew)
                    elif measurement_type == 3:
                        final_result= self.judge_freq_unit(value= value)
                    elif measurement_type == 4:
                        final_result = f"{float(value):.2f}"+' %'

                    try:
                        mean[divmod(index, 7)[0]]= final_result
                    except:
                        continue

            # l_meas_name_1.config(text=f'{meas_name[0]}')
            # text_mean_1.config(state=tk.NORMAL)  # 先啟用Text小部件的編輯狀態
            # text_mean_1.delete(1.0, tk.END)  # 清空當前內容
            # text_mean_1.insert(tk.END, f"{mean[0]}")
            # text_mean_1.config(state=tk.DISABLED)  # 設置為只讀狀態

            # l_meas_name_2.config(text=f'{meas_name[1]}')
            # text_mean_2.config(state=tk.NORMAL)  # 先啟用Text小部件的編輯狀態
            # text_mean_2.delete(1.0, tk.END)  # 清空當前內容
            # text_mean_2.insert(tk.END, f"{mean[1]}")
            # text_mean_2.config(state=tk.DISABLED)  # 設置為只讀狀態

            # l_meas_name_3.config(text=f'{meas_name[2]}')
            # text_mean_3.config(state=tk.NORMAL)  # 先啟用Text小部件的編輯狀態
            # text_mean_3.delete(1.0, tk.END)  # 清空當前內容
            # text_mean_3.insert(tk.END, f"{mean[2]}")
            # text_mean_3.config(state=tk.DISABLED)  # 設置為只讀狀態

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

    ### Others ###
    def switch_string(var_1, var_2):
        string_1= var_1.get()
        string_2= var_2.get()
        var_1.set(string_2)
        var_2.set(string_1)

    def clear(string):
        string.set('')

    def close_window():
        if messagebox.askyesno('Message', 'Exit?'):
            config = configparser.ConfigParser()
            config.optionxform = str
            config.read( os.path.join(os.path.dirname(__file__), 'InitConfig_setup.ini'), encoding='utf-8',)
            
            config.set('Scale_Offset_Selected_Values', 'VoltScale', str_volt_scale.get())
            config.set('Scale_Offset_Selected_Values', 'VoltOffset', str_volt_offset.get())
            config.set('Scale_Offset_Config', 'TimebaseScale', str_time_scale.get())
            config.set('Scale_Offset_Config', 'TimebaseOffset', str_time_offset.get())
            config.set('Scale_Offset_Selected_Values', 'TriggerLevel', str_trigger_level.get())
            config.set('Scale_Offset_Config', 'TriggerChan', str_trigger_chan.get())
            config.set('Scale_Offset_Config', 'WfmIntensity', str_wfm_intensity.get())
            
            config.set('Threshold_Selected_Values', 'GeneralTopPercent', str_gen_top_percent.get())
            config.set('Threshold_Selected_Values', 'GeneralMiddlePercent', str_gen_mid_percent.get())
            config.set('Threshold_Selected_Values', 'GeneralBasePercent', str_gen_base_percent.get())
            config.set('Threshold_Selected_Values', 'GeneralTop', str_gen_top.get())
            config.set('Threshold_Selected_Values', 'GeneralMiddle', str_gen_mid.get())
            config.set('Threshold_Selected_Values', 'GeneralBase', str_gen_base.get())
            
            config.set('Real_Time_Selected_Values', 'RealTimeSourceChannel', str(int_source_chan.get()))
            config.set('Real_Time_Selected_Values', 'RealTimeFrequency', str_realtime_freq.get())
            config.set('Real_Time_Selected_Values', 'RealTimeSamplingRate', str_realtime_sampling_rate.get())
            config.set('Real_Time_Selected_Values', 'RealTimeMemoryDepth', str_realtime_memory_depth.get())
            config.set('Real_Time_Selected_Values', 'RealTimeHistogram', str(boolvar_histogram.get()))
            config.set('Real_Time_Selected_Values', 'RealTimeVoltageMeas', str(boolvar_voltage_meas.get()))
            config.set('Real_Time_Selected_Values', 'RealTimeMask', str(boolvar_mask_test.get()))
            config.set('Real_Time_Selected_Values', 'RealTimeMaskPath', str_mask.get())
            
            config.set('Acquisition', 'SamplingRate', str_sampling_rate.get())
            config.set('Acquisition', 'MemoryDepth', str_memory_depth.get())

            config.set('Lable_Setup_Config', 'ChanLabel1', str_label_1.get())
            config.set('Lable_Setup_Config', 'ChanLabel2', str_label_2.get())
            config.set('Lable_Setup_Config', 'ChanLabel3', str_label_3.get())
            config.set('Lable_Setup_Config', 'ChanLabel4', str_label_4.get())
            config.set('Lable_Setup_Config', 'WMeLabel1', str_label_5.get())
            config.set('Lable_Setup_Config', 'WMeLabel2', str_label_6.get())
            config.set('Lable_Setup_Config', 'WMeLabel3', str_label_7.get())
            config.set('Lable_Setup_Config', 'WMeLabel4', str_label_8.get())

            config.set('Chan_Delta', 'ChanSingle', str_ch.get())

            config.set('Save_Setup_Config', 'SaveImgFolder', str_image_folder.get())
            config.set('Save_Setup_Config', 'SaveImgLocation', str(int_img_path_choice.get()))
            config.set('Save_Setup_Config', 'SaveImgPCFolder', str_image_pc_folder.get())
            config.set('Save_Setup_Config', 'SaveImgName', str_image.get())
            config.set('Save_Setup_Config', 'SaveWMeFolder', str_WMe_folder.get())
            config.set('Save_Setup_Config', 'SaveWMeLocation', str(int_wme_path_choice.get()))
            config.set('Save_Setup_Config', 'SaveWMePCFolder', str_WMe_pc_folder.get())
            config.set('Save_Setup_Config', 'SaveWMeName', str_other_file.get())

            config.set('Load_WMemory_Setup_Config', 'LoadWMe1', str_WMe1.get())
            config.set('Load_WMemory_Setup_Config', 'LoadWMe2', str_WMe2.get())
            config.set('Load_WMemory_Setup_Config', 'LoadWMe3', str_WMe3.get())
            config.set('Load_WMemory_Setup_Config', 'LoadWMe4', str_WMe4.get())
            config.set('Load_WMemory_Setup_Config', 'LoadSetup', str_setup.get())

            config.write(open(os.path.join(os.path.dirname(__file__), 'InitConfig_setup.ini'), 'w'))

            # formatted_time= self.current_time()
            # print(f'\n{formatted_time} [GUI Message] Window Closed.')
            window.destroy()
            sys.exit()

    
    def combo_ini():
        config_initial = configparser.ConfigParser()
        config_initial.optionxform = str
        config_file = os.path.join(os.path.dirname(__file__), 'InitConfig_setup.ini')
        config_initial.read(config_file, encoding='UTF-8')
        
        # Scale
        VoltScale_options = config_initial['Scale_Offset_Config'].get('VoltScale', '').split(',')
        VoltOffset_options = config_initial['Scale_Offset_Config'].get('VoltOffset', '').split(',')
        TriggerLevel_options = config_initial['Scale_Offset_Config'].get('TriggerLevel', '').split(',')

        # Threshold
        GeneralTopPercent_options = config_initial['Threshold_Setup_Config'].get('GeneralTopPercent', '').split(',')
        GeneralMiddlePercent_options = config_initial['Threshold_Setup_Config'].get('GeneralMiddlePercent', '').split(',')
        GeneralBasePercent_options = config_initial['Threshold_Setup_Config'].get('GeneralBasePercent', '').split(',')
        GeneralTop_options = config_initial['Threshold_Setup_Config'].get('GeneralTop', '').split(',')
        GeneralMiddle_options = config_initial['Threshold_Setup_Config'].get('GeneralMiddle', '').split(',')
        GeneralBase_options = config_initial['Threshold_Setup_Config'].get('GeneralBase', '').split(',')
        
        RealTimeFrequency_options = config_initial['Real_Time_Config'].get('RealTimeFrequency', '').split(',')
        
        # 從這裡返回值供其他部分調用
        return {
            'VoltScale': VoltScale_options, 
            'VoltOffset': VoltOffset_options, 
            'TriggerLevel': TriggerLevel_options, 
            'GeneralTopPercent': GeneralTopPercent_options,
            'GeneralMiddlePercent': GeneralMiddlePercent_options, 
            'GeneralBasePercent': GeneralBasePercent_options, 
            'GeneralTop': GeneralTop_options, 
            'GeneralMiddle': GeneralMiddle_options, 
            'GeneralBase': GeneralBase_options, 
            'RealTimeFrequency': RealTimeFrequency_options, 
            
            'config_file': config_file,  # 儲存config文件路徑以便後續使用

            'selected_values': {
                'VoltScale': config_initial['Scale_Offset_Selected_Values'].get('VoltScale', ''),
                'VoltOffset': config_initial['Scale_Offset_Selected_Values'].get('VoltOffset', ''),
                'TriggerLevel': config_initial['Scale_Offset_Selected_Values'].get('TriggerLevel', ''),
                'GeneralTopPercent': config_initial['Threshold_Selected_Values'].get('GeneralTopPercent', ''),
                'GeneralMiddlePercent': config_initial['Threshold_Selected_Values'].get('GeneralMiddlePercent', ''),
                'GeneralBasePercent': config_initial['Threshold_Selected_Values'].get('GeneralBasePercent', ''),
                'GeneralTop': config_initial['Threshold_Selected_Values'].get('GeneralTop', ''),
                'GeneralMiddle': config_initial['Threshold_Selected_Values'].get('GeneralMiddle', ''),
                'GeneralBase': config_initial['Threshold_Selected_Values'].get('GeneralBase', ''),
                'RealTimeFrequency': config_initial['Real_Time_Selected_Values'].get('RealTimeFrequency', ''),
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
    # general_top_percent_options = config_data['GeneralTopPercent']
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
    window.configure(bg= "#FFF4E9")

    frame_bg_color_1= "#d8cfc4"
    frame_bg_color_2= "#dbc8b0"
    labelframe_word_color= "#765F50"
    label_word_color= "#5C260D"
    text_name_color= "#645C51"
    text_result_color= "#504737"

    # 設定wfm intensity參數
    wfm_intensity_STEP = 1
    wfm_intensity_MIN_VALUE = 0
    wfm_intensity_MAX_VALUE = 100

    # Channel Frame ===================================================================================================================================
    label_frame_chan= tk.LabelFrame(window, text= 'Channel', background= frame_bg_color_2, fg= labelframe_word_color, font= ('Candara', 10, 'bold'),)

    button_chan1 = tk.Button(label_frame_chan, text='Chan1', width= 20, height= 2, command= lambda: uxr.display_Chan(chan= 1, bookmark= str_label_1.get(), choose_type= int_label_type.get()))
    button_chan2 = tk.Button(label_frame_chan, text='Chan2', width= 20, height= 2, command= lambda: uxr.display_Chan(chan= 2, bookmark= str_label_2.get(), choose_type= int_label_type.get()))
    button_chan3 = tk.Button(label_frame_chan, text='Chan3', width= 20, height= 2, command= lambda: uxr.display_Chan(chan= 3, bookmark= str_label_3.get(), choose_type= int_label_type.get()))
    button_chan4 = tk.Button(label_frame_chan, text='Chan4', width= 20, height= 2, command= lambda: uxr.display_Chan(chan= 4, bookmark= str_label_4.get(), choose_type= int_label_type.get()))
    button_wme1 = tk.Button(label_frame_chan, text='WMemory1', width= 20, height= 2, command= lambda: uxr.display_WMemory(chan= 1, bookmark= str_label_5.get(), choose_type= int_label_type.get()))
    button_wme2 = tk.Button(label_frame_chan, text='WMemory2', width= 20, height= 2, command= lambda: uxr.display_WMemory(chan= 2, bookmark= str_label_6.get(), choose_type= int_label_type.get()))
    button_wme3 = tk.Button(label_frame_chan, text='WMemory3', width= 20, height= 2, command= lambda: uxr.display_WMemory(chan= 3, bookmark= str_label_7.get(), choose_type= int_label_type.get()))
    button_wme4 = tk.Button(label_frame_chan, text='WMemory4', width= 20, height= 2, command= lambda: uxr.display_WMemory(chan= 4, bookmark= str_label_8.get(), choose_type= int_label_type.get()))

    # Scale / Offset Frame ===================================================================================================================================
    label_frame_scale= tk.LabelFrame(window, text= 'Scale / Offset', background= frame_bg_color_1, fg= labelframe_word_color, font= ('Candara', 10, 'bold'),)
    
    label_ch= tk.Label(label_frame_scale, text= 'Chan', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)
    str_ch = tk.StringVar()
    combobox_ch = ttk.Combobox(label_frame_scale, width= 5, textvariable= str_ch, values= ['All', '1', '2', '3', '4'])

    label_volt_scale = tk.Label(label_frame_scale, text= 'Voltage Scale (V)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)

    str_volt_scale = tk.StringVar()
    combobox_volt_scale = ttk.Combobox(label_frame_scale, width= 7, textvariable= str_volt_scale)
    commbobox_function(combobox= combobox_volt_scale, combobox_var= str_volt_scale, ini_dict_key= 'VoltScale', ini_option_section= 'Scale_Offset_Config', ini_option_key= 'VoltScale', ini_selected_section= 'Scale_Offset_Selected_Values')

    label_volt_offset = tk.Label(label_frame_scale, text= 'Voltage Offset (V)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)

    str_volt_offset = tk.StringVar()
    combobox_volt_offset = ttk.Combobox(label_frame_scale, width= 7, textvariable= str_volt_offset)
    commbobox_function(combobox= combobox_volt_offset, combobox_var= str_volt_offset, ini_dict_key= 'VoltOffset', ini_option_section= 'Scale_Offset_Config', ini_option_key= 'VoltOffset', ini_selected_section= 'Scale_Offset_Selected_Values')

    button_volt_scale = tk.Button(label_frame_scale, text= 'Volt Check', width= 10, height= 1, command= lambda: uxr.volt_check(scale= str_volt_scale.get(), offset= str_volt_offset.get()))

    label_trigger_chan = tk.Label(label_frame_scale, text= 'Trigger Channel', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)

    str_trigger_chan = tk.StringVar()
    combobox_trigger_chan = ttk.Combobox(label_frame_scale, width= 7, textvariable= str_trigger_chan, values= [1, 2, 3, 4])

    label_trigger_level = tk.Label(label_frame_scale, text= 'Trigger level (V)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)

    str_trigger_level = tk.StringVar()
    combobox_trigger_level = ttk.Combobox(label_frame_scale, width= 7, textvariable= str_trigger_level)
    commbobox_function(combobox= combobox_trigger_level, combobox_var= str_trigger_level, ini_dict_key= 'TriggerLevel', ini_option_section= 'Scale_Offset_Config', ini_option_key= 'TriggerLevel', ini_selected_section= 'Scale_Offset_Selected_Values')

    button_trigger_check = tk.Button(label_frame_scale, text= 'Trig Check', width= 10, height= 1, command= lambda: uxr.trig_check(chan= str_trigger_chan.get(), level= str_trigger_level.get()))

    label_time_scale = tk.Label(label_frame_scale, text= 'Timebase Scale (sec)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)

    str_time_scale = tk.StringVar()
    enrty_time_scale = tk.Entry(label_frame_scale, width= 7, textvariable= str_time_scale)

    label_time_offset = tk.Label(label_frame_scale, text= 'Timebase Offset (sec)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)

    str_time_offset = tk.StringVar()
    enrty_time_offset = tk.Entry(label_frame_scale, width= 7, textvariable= str_time_offset)

    button_time_scale_check = tk.Button(label_frame_scale, text= 'Time scale Check', height= 1, command= lambda: uxr.timebase_scale_check(scale= str_time_scale.get()))
    button_time_position_check = tk.Button(label_frame_scale, text= 'Time posi Check', height= 1, command= lambda: uxr.timebase_position_check(position= str_time_offset.get()))

    label_wfm_intensity = tk.Label(label_frame_scale, text= 'Waveform Intensity (%)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)

    vcmd = (window.register(validate_number), "%P") # %P = 輸入後字串
    str_wfm_intensity = tk.StringVar()
    entry_wfm_intensity = tk.Entry(label_frame_scale, width= 7, justify="center", textvariable= str_wfm_intensity, validate="key", validatecommand=vcmd)
    update_color(value= str_wfm_intensity.get())
    button_wfm_intensity = tk.Button(label_frame_scale, text= 'Intensity Check', height= 1, command= lambda: uxr.intensity_check(intensity_value= str_wfm_intensity.get()))
    
    button_set_intensity_50 = tk.Button(label_frame_scale, text="Set Intensity 50", command=set_to_50, font=("Candara", 10))

    entry_wfm_intensity.bind("<MouseWheel>", on_mouse_wheel)
    entry_wfm_intensity.bind("<Button-4>", lambda e: on_mouse_wheel(type("Event", (), {"delta": 120})))
    entry_wfm_intensity.bind("<Button-5>", lambda e: on_mouse_wheel(type("Event", (), {"delta": -120})))

    # Acquisition Frame ===================================================================================================================================
    label_frame_acquisition= tk.LabelFrame(window, text= 'Acquisition', background= frame_bg_color_2, fg= labelframe_word_color, font= ('Candara', 10, 'bold'),)
    
    label_sampling_rate = tk.Label(label_frame_acquisition, text= 'Sampling Rate', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 11,),)
    str_sampling_rate = tk.StringVar()
    entry_sampling_rate = tk.Entry(label_frame_acquisition, width= 10, textvariable= str_sampling_rate)
    button_sampling_rate_check = tk.Button(label_frame_acquisition, text= 'Sampling Rate Check', height= 1, command= lambda: uxr.sampling_rate_acquire(rate= str_sampling_rate.get()))
    button_sampling_rate_auto = tk.Button(label_frame_acquisition, text= 'Return Automatic', height= 1, command= lambda: uxr.sampling_rate_acquire(rate= 'AUTO'))

    label_memory_depth = tk.Label(label_frame_acquisition, text= 'Memory Depth', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 11,),)
    str_memory_depth = tk.StringVar()
    entry_memory_depth = tk.Entry(label_frame_acquisition, width= 10, textvariable= str_memory_depth)
    button_memory_depth_check = tk.Button(label_frame_acquisition, text= 'Memory Depth Check', height= 1, command= lambda: uxr.memory_depth_acquire(points_value= str_memory_depth.get()))
    button_memory_depth_auto = tk.Button(label_frame_acquisition, text= 'Return Automatic', height= 1, command= lambda: uxr.memory_depth_acquire(points_value= 'AUTO'))

    # Label Frame ===================================================================================================================================
    label_frame_label= tk.LabelFrame(window, text= 'Label', background= frame_bg_color_1, fg= labelframe_word_color, font= ('Candara', 10, 'bold'),)

    int_label_type = tk.IntVar()    
    # radiobutton_label= tk.Radiobutton(label_frame_label, text= 'Label', variable= int_label_type, value= 1, background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 10, 'bold'),)

    radiobutton_bookmark= tk.Radiobutton(label_frame_label, text= 'Bookmark', variable= int_label_type, value= 2, background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 10, 'bold'),)
    radiobutton_bookmark.select()

    str_label_1 = tk.StringVar()
    entry_label_1 = tk.Entry(label_frame_label, width= 25, textvariable= str_label_1)

    button_label_1 = tk.Button(label_frame_label, text= 'Chan1_label', command= lambda: uxr.add_bookmark(choose_type= int_label_type.get(), chan= 1, bookmark= str_label_1.get().rstrip('\n')))
    button_del_label_1 = tk.Button(label_frame_label, text= 'Delete', command= lambda: uxr.delete_bookmark(chan= 1, choose_type= int_label_type.get()))

    str_label_2 = tk.StringVar()
    entry_label_2 = tk.Entry(label_frame_label, width= 25, textvariable= str_label_2)

    button_label_2 = tk.Button(label_frame_label, text= 'Chan2_label', command= lambda: uxr.add_bookmark(choose_type= int_label_type.get(), chan= 2, bookmark= (str_label_2.get().rstrip('\n'))))
    button_del_label_2 = tk.Button(label_frame_label, text= 'Delete', command= lambda: uxr.delete_bookmark(chan= 2, choose_type= int_label_type.get()))

    str_label_3 = tk.StringVar()
    entry_label_3 = tk.Entry(label_frame_label, width= 25, textvariable= str_label_3)

    button_label_3 = tk.Button(label_frame_label, text= 'Chan3_label', command= lambda: uxr.add_bookmark(choose_type= int_label_type.get(), chan= 3, bookmark= (str_label_3.get().rstrip('\n'))))
    button_del_label_3 = tk.Button(label_frame_label, text= 'Delete', command= lambda: uxr.delete_bookmark(chan= 3, choose_type= int_label_type.get()))

    str_label_4 = tk.StringVar()
    entry_label_4 = tk.Entry(label_frame_label, width= 25, textvariable= str_label_4)

    button_label_4 = tk.Button(label_frame_label, text= 'Chan4_label', command= lambda: uxr.add_bookmark(choose_type= int_label_type.get(), chan= 4, bookmark= (str_label_4.get().rstrip('\n'))))
    button_del_label_4 = tk.Button(label_frame_label, text= 'Delete', command= lambda: uxr.delete_bookmark(chan= 4, choose_type= int_label_type.get()))

    str_label_5 = tk.StringVar()
    entry_label_5 = tk.Entry(label_frame_label, width= 25, textvariable= str_label_5)

    button_label_5 = tk.Button(label_frame_label, text= 'WMe1_label', command= lambda: uxr.add_bookmark(choose_type= int_label_type.get(), chan= 5, bookmark= str_label_5.get().rstrip('\n')))
    button_del_label_5 = tk.Button(label_frame_label, text= 'Delete', command= lambda: uxr.delete_bookmark(chan= 5, choose_type= int_label_type.get()))

    str_label_6 = tk.StringVar()
    entry_label_6 = tk.Entry(label_frame_label, width= 25, textvariable= str_label_6)

    button_label_6 = tk.Button(label_frame_label, text= 'WMe2_label', command= lambda: uxr.add_bookmark(choose_type= int_label_type.get(), chan= 6, bookmark= (str_label_6.get().rstrip('\n'))))
    button_del_label_6 = tk.Button(label_frame_label, text= 'Delete', command= lambda: uxr.delete_bookmark(chan= 6, choose_type= int_label_type.get()))

    str_label_7 = tk.StringVar()
    entry_label_7 = tk.Entry(label_frame_label, width= 25, textvariable= str_label_7)

    button_label_7 = tk.Button(label_frame_label, text= 'WMe3_label', command= lambda: uxr.add_bookmark(choose_type= int_label_type.get(), chan= 7, bookmark= (str_label_7.get().rstrip('\n'))))
    button_del_label_7 = tk.Button(label_frame_label, text= 'Delete', command= lambda: uxr.delete_bookmark(chan= 7, choose_type= int_label_type.get()))

    str_label_8 = tk.StringVar()
    entry_label_8 = tk.Entry(label_frame_label, width= 25, textvariable= str_label_8)

    button_label_8 = tk.Button(label_frame_label, text= 'WMe4_label', command= lambda: uxr.add_bookmark(choose_type= int_label_type.get(), chan= 8, bookmark= (str_label_8.get().rstrip('\n'))))
    button_del_label_8 = tk.Button(label_frame_label, text= 'Delete', command= lambda: uxr.delete_bookmark(chan= 8, choose_type= int_label_type.get()))

    # Measurement Frame ===================================================================================================================================
    label_frame_meas_item= tk.LabelFrame(window, text= 'Measurement', background= frame_bg_color_2, fg= labelframe_word_color, font= ('Candara', 10, 'bold'),)

    button_freq = tk.Button(label_frame_meas_item, text='Frequency', width= 20, height= 2, command= lambda: uxr.freq(chan= str_ch.get()))
    button_period = tk.Button(label_frame_meas_item, text='Period', width= 20, height= 2, command= lambda: uxr.period(chan= str_ch.get()))
    button_VIH = tk.Button(label_frame_meas_item, text='VIH', width= 20, height= 2, command= lambda: uxr.VIH(chan= str_ch.get()))
    button_VIL= tk.Button(label_frame_meas_item, text='VIL', width= 20, height= 2, command= lambda: uxr.VIL(chan= str_ch.get()))
    
    # Threshold Frame ===================================================================================================================================
    label_frame_thres= tk.LabelFrame(window, text= 'Threshold', background= frame_bg_color_1, fg= labelframe_word_color, font= ('Candara', 10, 'bold'),)

    int_gen_thres = tk.IntVar()    
    radiobutton_gen_threshold_1= tk.Radiobutton(label_frame_thres, text= 'Gen Thres Top (%)', variable= int_gen_thres, value= 1, background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)

    str_gen_top_percent = tk.StringVar()
    combobox_gen_top_percent = ttk.Combobox(label_frame_thres, width= 8, textvariable= str_gen_top_percent)
    commbobox_function(combobox= combobox_gen_top_percent, combobox_var= str_gen_top_percent, ini_dict_key= 'GeneralTopPercent', ini_option_section= 'Threshold_Setup_Config', ini_option_key= 'GeneralTopPercent', ini_selected_section= 'Threshold_Selected_Values')
    
    label_gen_threshold_1= tk.Label(label_frame_thres, text= '        Gen Thres Middle (%)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)

    str_gen_mid_percent = tk.StringVar()
    combobox_gen_mid_percent = ttk.Combobox(label_frame_thres, width= 8, textvariable= str_gen_mid_percent)
    commbobox_function(combobox= combobox_gen_mid_percent, combobox_var= str_gen_mid_percent, ini_dict_key= 'GeneralMiddlePercent', ini_option_section= 'Threshold_Setup_Config', ini_option_key= 'GeneralMiddlePercent', ini_selected_section= 'Threshold_Selected_Values')

    label_gen_threshold_2= tk.Label(label_frame_thres, text= '        Gen Thres Base (%)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)

    str_gen_base_percent = tk.StringVar()
    combobox_gen_base_percent = ttk.Combobox(label_frame_thres, width= 8, textvariable= str_gen_base_percent)
    commbobox_function(combobox= combobox_gen_base_percent, combobox_var= str_gen_base_percent, ini_dict_key= 'GeneralBasePercent', ini_option_section= 'Threshold_Setup_Config', ini_option_key= 'GeneralBasePercent', ini_selected_section= 'Threshold_Selected_Values')

    radiobutton_gen_threshold_2= tk.Radiobutton(label_frame_thres, text= 'Gen Thres Top (V)', variable= int_gen_thres, value= 2, background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11, 'bold'),)
    radiobutton_gen_threshold_2.select()

    str_gen_top = tk.StringVar()
    combobox_gen_top = ttk.Combobox(label_frame_thres, width= 8, textvariable= str_gen_top)
    commbobox_function(combobox= combobox_gen_top, combobox_var= str_gen_top, ini_dict_key= 'GeneralTop', ini_option_section= 'Threshold_Setup_Config', ini_option_key= 'GeneralTop', ini_selected_section= 'Threshold_Selected_Values')

    label_gen_threshold_4= tk.Label(label_frame_thres, text= '        Gen Thres Middle (V)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)

    str_gen_mid = tk.StringVar()
    combobox_gen_mid = ttk.Combobox(label_frame_thres, width= 8, textvariable= str_gen_mid)
    commbobox_function(combobox= combobox_gen_mid, combobox_var= str_gen_mid, ini_dict_key= 'GeneralMiddle', ini_option_section= 'Threshold_Setup_Config', ini_option_key= 'GeneralMiddle', ini_selected_section= 'Threshold_Selected_Values')

    label_gen_threshold_5= tk.Label(label_frame_thres, text= '        Gen Thres Base (V)', background= frame_bg_color_1, fg= label_word_color, font= ('Candara', 11,),)

    str_gen_base = tk.StringVar()
    combobox_gen_base = ttk.Combobox(label_frame_thres, width= 8, textvariable= str_gen_base)
    commbobox_function(combobox= combobox_gen_base, combobox_var= str_gen_base, ini_dict_key= 'GeneralBase', ini_option_section= 'Threshold_Setup_Config', ini_option_key= 'GeneralBase', ini_selected_section= 'Threshold_Selected_Values')
    button_gen_check = tk.Button(
        label_frame_thres, text= 'Gen Thres Check', command= lambda: uxr.gen_threshold(
            g_top= combobox_gen_top.get(), g_middle= combobox_gen_mid.get(), g_base= combobox_gen_base.get(), g_top_percent= combobox_gen_top_percent.get(), g_middle_percent= combobox_gen_mid_percent.get(), g_base_percent= combobox_gen_base_percent.get(), 
            )
        )

    # Control Frame ===================================================================================================================================
    label_frame_control= tk.LabelFrame(window, text= 'Control', background= frame_bg_color_1, fg= labelframe_word_color, font= ('Candara', 10, 'bold'),)

    button_run = tk.Button(label_frame_control, text='RUN', width= 20, height= 2, command= lambda: uxr.run())

    button_stop = tk.Button(label_frame_control, text='STOP', width= 20, height= 2, command= lambda: uxr.stop())

    button_single = tk.Button(label_frame_control, text='SINGLE', width= 20, height= 2, command= lambda: uxr.single())

    button_clear_display = tk.Button(label_frame_control, text='Clear', width= 8, height= 2, command= lambda: uxr.clear_diaplay())
    button_clear_display.config(state= 'disabled')

    button_autoscale = tk.Button(label_frame_control, text='Auto Scale', width= 20, height= 2, command= lambda: uxr.autoscale())
    button_autoscale.config(state= 'disabled')

    button_default = tk.Button(label_frame_control, text='Default', width= 20, height= 2, command= lambda: uxr.default())
    button_default.config(state= 'disabled')

    button_trigger = tk.Button(label_frame_control, text='Trigger Type', width= 20, height= 2, command= lambda: uxr.trig_type())

    button_del = tk.Button(label_frame_control, text='Delete item', width= 20, height= 2, command= lambda: uxr.delete_item())

    button_add_marker = tk.Button(label_frame_control, text='Add Marker', width= 20, height= 2, command= lambda: uxr.add_marker())

    button_del_marker = tk.Button(label_frame_control, text='Del Marker', width= 20, height= 2, command= lambda: uxr.delete_marker())

    button_trig_slope = tk.Button(label_frame_control, text= 'Trig Slope', width= 8, height= 2, command= lambda: uxr.trig_slope())

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

    button_button_disable = tk.Button(label_frame_control, text= 'Disable\nButton', width= 8, height=2, command= disable_button)

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

    # Real-time eye Frame ===================================================================================================================================
    label_frame_realtime_eye= tk.LabelFrame(window, text= 'Real Time Eye', background= frame_bg_color_2, fg= labelframe_word_color, font= ('Candara', 10, 'bold'),)

    label_source_chan= tk.Label(label_frame_realtime_eye, text= 'Source Channel', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 11,),)
    int_source_chan = tk.IntVar()
    combobox_source_chan = ttk.Combobox(label_frame_realtime_eye, width= 5, textvariable= int_source_chan, values= ['1', '2', '3', '4'])
    
    label_realtime_freq= tk.Label(label_frame_realtime_eye, text= 'Frequency (GHz)', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 11,),)
    str_realtime_freq= tk.StringVar()
    combobox_realtime_freq = ttk.Combobox(label_frame_realtime_eye, width= 8, textvariable= str_realtime_freq)
    commbobox_function(combobox= combobox_realtime_freq, combobox_var= str_realtime_freq, ini_dict_key= 'RealTimeFrequency', ini_option_section= 'Real_Time_Config', ini_option_key= 'RealTimeFrequency', ini_selected_section= 'Real_Time_Selected_Values')
    
    label_realtime_sampling_rate= tk.Label(label_frame_realtime_eye, text= 'Sampling Rate (Sa/s)', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 11,),)
    str_realtime_sampling_rate = tk.StringVar()
    entry_realtime_sampling_rate = tk.Entry(label_frame_realtime_eye, width= 10, textvariable= str_realtime_sampling_rate)

    label_realtime_memory_depth= tk.Label(label_frame_realtime_eye, text= 'Memory Depth (pts)', background= frame_bg_color_2, fg= label_word_color, font= ('Candara', 11,),)
    str_realtime_memory_depth = tk.StringVar()
    entry_realtime_memory_depth = tk.Entry(label_frame_realtime_eye, width= 10, textvariable= str_realtime_memory_depth)

    boolvar_histogram = tk.BooleanVar()    
    checkbutton_histogram= tk.Checkbutton(label_frame_realtime_eye, text= 'Histogram', variable= boolvar_histogram, background= frame_bg_color_2, fg= label_word_color)
    boolvar_voltage_meas = tk.BooleanVar()    
    checkbutton_voltage_meas= tk.Checkbutton(label_frame_realtime_eye, text= 'Voltage Meas', variable= boolvar_voltage_meas, background= frame_bg_color_2, fg= label_word_color)
    boolvar_mask_test = tk.BooleanVar()    
    checkbutton_mask_test= tk.Checkbutton(label_frame_realtime_eye, text= 'Mask', variable= boolvar_mask_test, background= frame_bg_color_2, fg= label_word_color)
    str_mask= tk.StringVar()
    entry_mask= tk.Entry(label_frame_realtime_eye, width= 25, textvariable= str_mask)


    # 100MHz PCIe CLK Frame ===================================================================================================================================
    # Save Frame ===================================================================================================================================
    # Load WMemory Frame ===================================================================================================================================



    # Grid ===================================================================================================================================

    # LabelFrame grid
    label_frame_chan.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'nsew')
    label_frame_scale.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'nsew')
    label_frame_acquisition.grid(row= 2, column= 0, padx= 5, pady= 2, sticky= 'nsew')
    label_frame_label.grid(row= 3, column= 0, padx= 5, pady= 2, sticky= 'nsew')
    label_frame_meas_item.grid(row= 4, column= 0, padx= 5, pady= 2, sticky= 'nsew')
    label_frame_thres.grid(row= 5, column= 0, padx= 5, pady= 2, sticky= 'nsew')

    label_frame_control.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'nsew')
    label_frame_realtime_eye.grid(row= 1, column= 1, padx= 5, pady= 2, sticky= 'nsew')

    # Channel grid
    button_chan1.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    button_chan2.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'w')
    button_chan3.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'w')
    button_chan4.grid(row= 0, column= 3, padx= 5, pady= 2, sticky= 'w')
    button_wme1.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'w')
    button_wme2.grid(row= 1, column= 1, padx= 5, pady= 2, sticky= 'w')
    button_wme3.grid(row= 1, column= 2, padx= 5, pady= 2, sticky= 'w')
    button_wme4.grid(row= 1, column= 3, padx= 5, pady= 2, sticky= 'w')

    # Scale / Offset grid
    label_ch.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    combobox_ch.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'w')
    
    label_volt_scale.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'w', columnspan= 2)
    combobox_volt_scale.grid(row= 1, column= 2, padx= 5, pady= 2, sticky= 'w')
    label_volt_offset.grid(row= 2, column= 0, padx= 5, pady= 2, sticky= 'w', columnspan= 2)
    combobox_volt_offset.grid(row= 2, column= 2, padx= 5, pady= 2, sticky= 'w')
    button_volt_scale.grid(row= 1, column= 3, padx= 5, pady= 2, sticky= 'w')

    label_trigger_chan.grid(row= 4, column= 0, padx= 5, pady= 2, sticky= 'w', columnspan= 2)
    combobox_trigger_chan.grid(row= 4, column= 2, padx= 5, pady= 2, sticky= 'w')
    label_trigger_level.grid(row= 5, column= 0, padx= 5, pady= 2, sticky= 'w', columnspan= 2)
    combobox_trigger_level.grid(row= 5, column= 2, padx= 5, pady= 2, sticky= 'w')
    button_trigger_check.grid(row= 4, column= 3, padx= 5, pady= 2, sticky= 'w')

    label_time_scale.grid(row= 1, column= 4, padx= 5, pady= 2, sticky= 'w')
    enrty_time_scale.grid(row= 1, column= 5, padx= 5, pady= 2, sticky= 'w')
    button_time_scale_check.grid(row= 1, column= 6, padx= 5, pady= 2, sticky= 'w')
    label_time_offset.grid(row= 2, column= 4, padx= 5, pady= 2, sticky= 'w')
    enrty_time_offset.grid(row= 2, column= 5, padx= 5, pady= 2, sticky= 'w')
    button_time_position_check.grid(row= 2, column= 6, padx= 5, pady= 2, sticky= 'w')

    label_wfm_intensity.grid(row= 4, column= 4, padx= 5, pady= 2, sticky= 'w')
    entry_wfm_intensity.grid(row= 4, column= 5, padx= 5, pady= 2, sticky= 'w')
    button_wfm_intensity.grid(row= 4, column= 6, padx= 5, pady= 2, sticky= 'w')
    button_set_intensity_50.grid(row= 5, column= 6, padx= 5, pady= 2, sticky= 'w')

    # Label grid
    # radiobutton_label.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    entry_label_1.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w', columnspan= 2)
    button_label_1.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'w')
    button_del_label_1.grid(row= 0, column= 3, padx= 5, pady= 2, sticky= 'w')
    entry_label_2.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'w', columnspan= 2)
    button_label_2.grid(row= 1, column= 2, padx= 5, pady= 2, sticky= 'w')
    button_del_label_2.grid(row= 1, column= 3, padx= 5, pady= 2, sticky= 'w')
    entry_label_3.grid(row= 2, column= 0, padx= 5, pady= 2, sticky= 'w', columnspan= 2)
    button_label_3.grid(row= 2, column= 2, padx= 5, pady= 2, sticky= 'w')
    button_del_label_3.grid(row= 2, column= 3, padx= 5, pady= 2, sticky= 'w')
    entry_label_4.grid(row= 3, column= 0, padx= 5, pady= 2, sticky= 'w', columnspan= 2)
    button_label_4.grid(row= 3, column= 2, padx= 5, pady= 2, sticky= 'w')
    button_del_label_4.grid(row= 3, column= 3, padx= 5, pady= 2, sticky= 'w')

    entry_label_5.grid(row= 0, column= 4, padx= 5, pady= 2, sticky= 'w')
    button_label_5.grid(row= 0, column= 5, padx= 5, pady= 2, sticky= 'w')
    button_del_label_5.grid(row= 0, column= 6, padx= 5, pady= 2, sticky= 'w')
    entry_label_6.grid(row= 1, column= 4, padx= 5, pady= 2, sticky= 'w')
    button_label_6.grid(row= 1, column= 5, padx= 5, pady= 2, sticky= 'w')
    button_del_label_6.grid(row= 1, column= 6, padx= 5, pady= 2, sticky= 'w')
    entry_label_7.grid(row= 2, column= 4, padx= 5, pady= 2, sticky= 'w')
    button_label_7.grid(row= 2, column= 5, padx= 5, pady= 2, sticky= 'w')
    button_del_label_7.grid(row= 2, column= 6, padx= 5, pady= 2, sticky= 'w')
    entry_label_8.grid(row= 3, column= 4, padx= 5, pady= 2, sticky= 'w')
    button_label_8.grid(row= 3, column= 5, padx= 5, pady= 2, sticky= 'w')
    button_del_label_8.grid(row= 3, column= 6, padx= 5, pady= 2, sticky= 'w')

    # Acquisition grid
    label_sampling_rate.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    entry_sampling_rate.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'w')
    button_sampling_rate_check.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'w')
    button_sampling_rate_auto.grid(row= 1, column= 2, padx= 5, pady= 2, sticky= 'w')

    label_memory_depth.grid(row= 0, column= 3, padx= 5, pady= 2, sticky= 'w')
    entry_memory_depth.grid(row= 0, column= 4, padx= 5, pady= 2, sticky= 'w')
    button_memory_depth_check.grid(row= 0, column= 5, padx= 5, pady= 2, sticky= 'w')
    button_memory_depth_auto.grid(row= 1, column= 5, padx= 5, pady= 2, sticky= 'w')

    # Measurement grid
    button_freq.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    button_period.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'w')
    button_VIH.grid(row= 0, column= 3, padx= 5, pady= 2, sticky= 'w')
    button_VIL.grid(row= 0, column= 4, padx= 5, pady= 2, sticky= 'w')

    # Threshold grid
    radiobutton_gen_threshold_1.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    combobox_gen_top_percent.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'w')

    label_gen_threshold_1.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'w')
    combobox_gen_mid_percent.grid(row= 1, column= 1, padx= 5, pady= 2, sticky= 'w')

    label_gen_threshold_2.grid(row= 2, column= 0, padx= 5, pady= 2, sticky= 'w')
    combobox_gen_base_percent.grid(row= 2, column= 1, padx= 5, pady= 2, sticky= 'w')

    radiobutton_gen_threshold_2.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'w')
    combobox_gen_top.grid(row= 0, column= 3, padx= 5, pady= 2, sticky= 'w')

    label_gen_threshold_4.grid(row= 1, column= 2, padx= 5, pady= 2, sticky= 'w')
    combobox_gen_mid.grid(row= 1, column= 3, padx= 5, pady= 2, sticky= 'w')

    label_gen_threshold_5.grid(row= 2, column= 2, padx= 5, pady= 2, sticky= 'w')
    combobox_gen_base.grid(row= 2, column= 3, padx= 5, pady= 2, sticky= 'w')

    button_gen_check.grid(row= 0, column= 4, padx= 5, pady= 2, sticky= 'w')

    # Control grid
    button_run.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w', rowspan= 2)
    button_stop.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'w', rowspan= 2)
    button_single.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'w', rowspan= 2)
    button_clear_display.grid(row= 0, column= 3, padx= 5, pady= 2, sticky= 'w', rowspan= 2)

    button_autoscale.grid(row= 2, column= 0, padx= 5, pady= 2, sticky= 'w', rowspan= 2)
    button_default.grid(row= 2, column= 1, padx= 5, pady= 2, sticky= 'w', rowspan= 2)
    button_trigger.grid(row= 2, column= 2, padx= 5, pady= 2, sticky= 'w', rowspan= 2)
    button_trig_slope.grid(row= 2, column= 3, padx= 5, pady= 2, sticky= 'w', rowspan= 2)

    button_del.grid(row= 4, column= 0, padx= 5, pady= 2, sticky= 'w', rowspan= 2)
    button_add_marker.grid(row= 4, column= 1, padx= 5, pady= 2, sticky= 'w', rowspan= 2)
    button_del_marker.grid(row= 4, column= 2, padx= 5, pady= 2, sticky= 'w', rowspan= 2)
    button_button_disable.grid(row= 4, column= 3, padx= 5, pady= 2, sticky= 'w', rowspan= 2)

    checkbutton_marker_1.grid(row= 0, column= 4, padx= 5) 
    checkbutton_marker_2.grid(row= 1, column= 4, padx= 5) 
    checkbutton_marker_3.grid(row= 2, column= 4, padx= 5) 
    checkbutton_marker_4.grid(row= 3, column= 4, padx= 5) 
    checkbutton_marker_5.grid(row= 4, column= 4, padx= 5) 
    checkbutton_marker_6.grid(row= 5, column= 4, padx= 5) 

    # Real-time eye grid
    label_source_chan.grid(row= 0, column= 0, padx= 5, pady= 2, sticky= 'w')
    combobox_source_chan.grid(row= 0, column= 1, padx= 5, pady= 2, sticky= 'w')

    label_realtime_sampling_rate.grid(row= 0, column= 2, padx= 5, pady= 2, sticky= 'w')
    entry_realtime_sampling_rate.grid(row= 0, column= 3, padx= 5, pady= 2, sticky= 'w')

    label_realtime_freq.grid(row= 1, column= 0, padx= 5, pady= 2, sticky= 'w')
    combobox_realtime_freq.grid(row= 1, column= 1, padx= 5, pady= 2, sticky= 'w')

    label_realtime_memory_depth.grid(row= 1, column= 2, padx= 5, pady= 2, sticky= 'w')
    entry_realtime_memory_depth.grid(row= 1, column= 3, padx= 5, pady= 2, sticky= 'w')

    checkbutton_histogram.grid(row= 2, column= 0, padx= 5, pady= 2, sticky= 'w')
    checkbutton_voltage_meas.grid(row= 3, column= 0, padx= 5, pady= 2, sticky= 'w')
    checkbutton_mask_test.grid(row= 4, column= 0, padx= 5, pady= 2, sticky= 'w')
    entry_mask.grid(row= 4, column= 1, padx= 5, pady= 2, sticky= 'w')






    initialize()

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
id_window.configure(background= '#91B6E1')

l_scope_ip = tk.Label(id_window, text= 'Enter Scope IP', background= '#91B6E1', fg= '#091E87', font= ('Candara', 12, 'bold'),)
str_scope_ip = tk.StringVar()
cb_scope_ip = ttk.Combobox(id_window, textvariable= str_scope_ip, values= scope_ips)
b_scope_ip = tk.Button(id_window, text= 'OK', width= 10, height= 2, command= lambda: show_main_window(old_scope_ips= scope_ips), )

l_ip = tk.Label(id_window, text= '★★★ 確認電腦IP與Scope在同一網域 ★★★', background= '#91B6E1', fg= '#F6044D', font= ('Candara', 14, 'bold'),)

l_scope_ip.pack(padx= 5, pady= 5)
cb_scope_ip.pack(padx= 5, pady= 5)
b_scope_ip.pack(padx= 5, pady= 5)
l_ip.pack(padx= 5, pady= 5)

id_window.mainloop()
