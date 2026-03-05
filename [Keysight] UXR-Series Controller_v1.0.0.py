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

        # str_volt_scale.set(value= select_VoltScale)


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

    def close_window():
        if messagebox.askyesno('Message', 'Exit?'):
            config = configparser.ConfigParser()
            config.optionxform = str
            config.read( os.path.join(os.path.dirname(__file__), 'InitConfig_setup.ini'), encoding='utf-8',)
            
            # config.set('Scale_Offset_Selected_Values', 'VoltScale', str_volt_scale.get())

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


        # 從這裡返回值供其他部分調用
        return {
            'VoltScale': VoltScale_options, 
            'selected_values': {
                'VoltScale': config_initial['Scale_Offset_Selected_Values'].get('VoltScale', ''),
                }        
        }

    def add_option(combobox, combobox_value, options, config_file, section, key, selected_section):
        new_option = combobox_value.get().strip()
        if new_option and new_option not in options:
            options.append(new_option)
            combobox['values'] = options
            # save_to_ini(config_file, section, key, options, selected_section, combobox.get())

    def delete_option(combobox, combobox_value, options, config_file, section, key, selected_section):
        selected_option = combobox_value.get().strip()
        if selected_option in options:
            options.remove(selected_option)
            combobox['values'] = options
            combobox_value.set('')  # 清空當前選擇
            # save_to_ini(config_file, section, key, options, selected_section, combobox.get())

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
    window.configure(bg= '#E9F4FF')

    bg_color_1= '#c4cdd8'
    bg_color_2= '#b0c8db'

    # 設定wfm intensity參數
    wfm_intensity_STEP = 1
    wfm_intensity_MIN_VALUE = 0
    wfm_intensity_MAX_VALUE = 100

    # Measurement Frame ===================================================================================================================================

    label_frame_meas_item= tk.LabelFrame(window, text= 'Measurement', background= bg_color_1, fg= '#506376', font= ('Candara', 10, 'bold'),)

    # b_freq = tk.Button(label_frame_meas_item, text='Frequency', width= 20, height= 2, command= lambda: mxr.freq(chan= int_ch_single.get()))

    # Grid ===================================================================================================================================
    # LabelFrame grid
    label_frame_meas_item.grid(row= 0, column= 0, padx= 5, pady= 2, columnspan= 2, sticky= 'nsew')
    # b_freq.grid(row= 0, column= 0, padx= 5, pady= 4)


    # ToolTip(b_tSU, 'Channel記得勾對欸')
    # ToolTip(cbb_volt_scale, '可用滑鼠滾輪選擇\n新增選項: 輸入後按Enter\n刪除選項: 選擇後按Delete')


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
