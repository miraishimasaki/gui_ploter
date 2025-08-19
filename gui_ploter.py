from tkinter import StringVar
# from tkinter.filedialog import askdirectory,askopenfile
from tkinter import messagebox
from PIL.Image import open
from PIL.ImageTk import PhotoImage
from matplotlib import use
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

# from time import time,sleep
from re import sub,findall
import ttkbootstrap as ttk

# from threading import Thread
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, lambdify,sympify



class ploter:
    def __init__(self):
        self.root = None
        self.photo_frame = None
        
        self.creat_windows()
        self.xdatas = StringVar(value='')                   #輸入數據變量
        self.ydatas = StringVar(value='')                   #輸入縱軸數據變量
        self.var_name = StringVar(value='')                 #輸入數據對於的變量名的變量
        self.output = StringVar(value='')                   #輸出變量
        self.expresion =  StringVar(value='')               #輸入表達式的變量
        self.output_unit = StringVar(value='')              #輸出變量的單位
        self.input_unit =  StringVar(value='')              #輸入變量的單位
        self.title = StringVar(value='')                    #輸入圖像標題的變量
        self.create_photo_frame()
        self.expr_entry = self.create_entry()
        self.create_button()
        self.combbox = self.create_combobox()

        self.interp_params = {'method': 'Cubic Spline','points':300}  # 插值的参数
        self.fitting_params = {'method': '2nd-order poly','points':300}  # 拟合的参数

        self.create_menu()
        self.root.mainloop()    

    def creat_windows(self):
        self.root = ttk.Window(themename='vapor',title='ploter_V1.0',size=(1950,1200),resizable=(False, False))
    
    
    def create_photo_frame(self):
        
        self.photo_frame = ttk.Frame(self.root,height=800,width=750) 
        #原来下面按钮之间有填充就是因为frame的样式设计成了light
        self.photo_frame.place(x=30,y=200)
        self.load_photo('./internal/test.jpg')
        
    def create_entry(self):
        dir_entry_label = ttk.Label(self.root,text='輸入表達式',bootstyle='inverse-danger',state='disabled')
        dir_entry_label.place(x=1000,y=783)
        dir_entry = ttk.Entry(self.root,width=58,bootstyle='danger',state='disabled',font=('Times New Roman',10,'bold'),textvariable=self.expresion)
        dir_entry.place(x=1000,y=820)

        dir_entry_label1 = ttk.Label(self.root,text='輸入數據對應的變量名',bootstyle='inverse-info')
        dir_entry_label1.place(x=1000,y=413)
        dir_entry1 = ttk.Entry(self.root,width=18,bootstyle='info',font=('Times New Roman',10,'bold'),textvariable=self.var_name)
        dir_entry1.place(x=1000,y=450)

        dir_entry_label2 = ttk.Label(self.root,text='輸入數據的單位',bootstyle='inverse-info')
        dir_entry_label2.place(x=1400,y=413)
        dir_entry2 = ttk.Entry(self.root,width=20,bootstyle='info',font=('Times New Roman',10,'bold'),textvariable=self.input_unit)
        dir_entry2.place(x=1400,y=450)

        dir_entry_label3 = ttk.Label(self.root,text='輸出數據對應的變量名',bootstyle='inverse-info')
        dir_entry_label3.place(x=1000,y=563)
        dir_entry3 = ttk.Entry(self.root,width=18,bootstyle='info',font=('Times New Roman',10,'bold'),textvariable=self.output)
        dir_entry3.place(x=1000,y=600)

        dir_entry_label4 = ttk.Label(self.root,text='輸出數據的單位',bootstyle='inverse-info')
        dir_entry_label4.place(x=1400,y=563)
        dir_entry4 = ttk.Entry(self.root,width=20,bootstyle='info',font=('Times New Roman',10,'bold'),textvariable=self.output_unit)
        dir_entry4.place(x=1400,y=600)

        path_entry_label = ttk.Label(self.root,text='輸入一組數據（橫軸）',bootstyle='inverse-primary')
        path_entry_label.place(x=1000,y=163)
        path_entry = ttk.Entry(self.root,width=58,bootstyle='primary',font=('Times New Roman',10,'bold'),textvariable=self.xdatas)
        path_entry.place(x=1000,y=200)

        path_entry_label1 = ttk.Label(self.root,text='輸入一組數據（縱軸）',bootstyle='inverse-primary')
        path_entry_label1.place(x=1000,y=283)
        path_entry1 = ttk.Entry(self.root,width=58,bootstyle='primary',font=('Times New Roman',10,'bold'),textvariable=self.ydatas)
        path_entry1.place(x=1000,y=320)
        
        path_entry_label2 = ttk.Label(self.root,text='輸入圖像標題',bootstyle='inverse-light')
        path_entry_label2.place(x=1400,y=670)
        path_entry2 = ttk.Entry(self.root,width=20,bootstyle='light',font=('Times New Roman',10,'bold'),textvariable=self.title)
        path_entry2.place(x=1400,y=700)

        return dir_entry
    

    def create_menu(self):
        Menubar = ttk.Menu(self.root)
        tipsmenu = ttk.Menu(Menubar)
        helpmenu = ttk.Menu(Menubar)
        Menubar.add_cascade(label='設定',menu=tipsmenu)
        tipsmenu.add_command(label='插值設置', command=self.interpolation_tl)
        tipsmenu.add_command(label='數據擬合設置', command=self.fitting_tl)
        self.root.config(menu = Menubar)

    def create_combobox(self,obj = None):
        if not obj:
            cb_label = ttk.Label(self.root,text='模式',bootstyle='inverse-light')
            cb_label.place(x=1000,y= 670)
            cb = ttk.Combobox(self.root,bootstyle = 'light',width=16,values=['輸入表達式計算','給定縱軸數據','數據擬合','插值'],state='readonly')
            cb.bind('<<ComboboxSelected>>', self.update)
            cb.set('給定縱軸數據')   
            cb.place(x=1000,y=700)
        else:
            cb_label = ttk.Label(obj,text='模式',bootstyle='inverse-light')
            cb_label.place(x=500,y= 335)
            cb = ttk.Combobox(obj,bootstyle = 'light',width=16,state='readonly')

            cb.place(x=500,y=365)
        return cb
    
    def update(self,event):
        if self.combbox.get() == '輸入表達式計算':
            self.expr_entry.config(state='normal')
        elif self.combbox.get() == '給定縱軸數據':
            self.expr_entry.config(state='disabled')    

    def create_button(self):
        gen_btn = ttk.Button(self.root,text='Generate',bootstyle='success-outline',width=57,command=self.plot)
        gen_btn.place(x=1000,y=950)

    def load_x_data(self):
        data = self.xdatas.get()
        numbers = findall(r"[-+]?\d*\.\d+|[-+]?\d+", data)

        if numbers:
            numbers = [float(num) for num in numbers]

            return np.array(numbers)
        else:
            print("字符串中没有数字")
            messagebox.showerror("Error", "請輸入正確的數據")
            return np.array([])
        
    def load_y_data(self):
        data = self.ydatas.get()
        numbers = findall(r"[-+]?\d*\.\d+|[-+]?\d+", data)

        if numbers:
            numbers = [float(num) for num in numbers]

            return np.array(numbers)
        else:
            print("字符串中没有数字")
            messagebox.showerror("Error", "請輸入正確的數據")
            return np.array([])


    def tranform(self):
        # 用正则表达式替换对应的自变量
        result = sub(self.var_name.get(), 'x', self.expresion.get())
        return result

    def calculate(self):
        # 处理表达式
        input_data = self.load_x_data()
        if input_data.size != 0:
            print("输入的表达式:", self.expresion.get())
            print("输入的数据:", input_data)

            x = symbols('x')
            #用正則表達式替換對應的自變量
            expresion = self.tranform()
            expr = sympify(expresion)      
            f = lambdify(x, expr, modules=['numpy'])
            output_data = f(input_data)

            if not isinstance(output_data, np.ndarray):
                print("Error: 输出数据不是有效的数组")
                messagebox.showerror("Error", "請輸入正確的表達式")
                return None, None
            print(f'輸出的數據：{output_data}')
            return input_data, output_data
        else:
            return None, None


    def update_fitting(self,event,method, points):
        self.fitting_params['method'] = method
        self.fitting_params['points'] = points


    def fitting_tl(self):
        ftl =  ttk.Toplevel(self.root)
        ftl.title('數據擬合設置')
        ftl.geometry('400x300')
        cb_label = ttk.Label(ftl,text='模式',bootstyle='inverse-light')
        cb_label.place(x=50,y= 135)
        cb = ttk.Combobox(ftl,bootstyle = 'light',width=16,state='readonly',values=['2nd-order poly','3rd-order poly','Higher-order poly（5）','Exponential fitting','Logarithmic fitting','Linear fitting'])
        #cb.bind('<<ComboboxSelected>>', lambda event: self.update_fitting(event, cb.get(), 300))
        cb.place(x=50,y=165)
        scale = ttk.Scale(
            ftl, from_=10, to=150, length=250,orient='horizontal', bootstyle='light',command=lambda event : print(scale.get()))
        #绑定用lambda event：来获取scale的值，event是tkinter自动传入的事件对象
        scale.set(50)
        sc_label = ttk.Label(ftl,text='插值点(每单位10-150)',bootstyle='inverse-light')
        sc_label.place(x=50,y= 35)
        scale.place(x=50, y=75)
        cb.set('2nd-order poly')  # 设置默认值为二阶多项式拟合

        ftl.protocol("WM_DELETE_WINDOW", lambda: [self.update_fitting(None, cb.get(), int(scale.get())), 
                                                  print(f'method : {self.fitting_params["method"]}, points : {self.fitting_params["points"]}'),
                                                  ftl.destroy()
                                                  ])   #关闭窗口时更新参数

    def fitting(self, event=None):
        if self.combbox.get() == '數據擬合':
            x_data = self.load_x_data()
            y_data =  self.load_y_data()

            x_yield = np.linspace(x_data.min(), x_data.max(), self.fitting_params['points'])

            if self.fitting_params['method'] == '2nd-order poly':
                coeff = np.polyfit(x_data, y_data, 2)
                print(f'2nd-order poly fitting params: {coeff}')
                y_yield = np.polyval(coeff, x_yield)

            elif self.fitting_params['method'] == '3rd-order poly':
                coeff = np.polyfit(x_data, y_data, 3)
                print(f'3rd-order poly fitting params: {coeff}')
                y_yield = np.polyval(coeff, x_yield)

            elif self.fitting_params['method'] == 'Higher-order poly（5）':
                coeff = np.polyfit(x_data, y_data, 5)
                print(f'Higher-order poly fitting params: {coeff}')
                y_yield = np.polyval(coeff, x_yield)     

            elif self.fitting_params['method'] == 'Linear fitting':
                coeff = np.polyfit(x_data, y_data, 1)
                print(f'Linear fitting params: {coeff}')
                y_yield = np.polyval(coeff, x_yield)

            #指数和对数拟合，稍微复杂
            elif self.fitting_params['method'] == 'Exponential fitting':
                #4,6.4,8,8.8,9.22,9.5,9.7,9.86,10,10.2,10.32,10.42,10.50,10.55,10.58,10.60
                # mask1 = y_data > 0  # 确保y值为正
                # mask2 = x_data!=0
                # mask = mask1 & mask2
                
                # def get_params_exp(x, y):
                #     if mask.sum()<2:
                #         a,b = 1, 0
                #         return a, b
                #     else:
                #         a,b = np.polyfit(1/x[mask], np.log(y[mask]), 1)
                #         return a,b

                # a, b = get_params_exp(x_data, y_data)
                # print(f'Exponential fitting params: a={a}, b={b}')
                # y_yield = np.exp(a/x_yield+b)  # 注意这里的x_yield是横轴数据
                
                mask1 = y_data > 0  # 确保y值为正
                mask = mask1 
                def get_params_exp(x, y):
                    if mask.sum()<2:
                        a,b = 1, 0
                        return a, b
                    else:
                        b,log_a = np.polyfit(x[mask], np.log(y[mask]), 1)
                        return np.exp(log_a), b
                    
                a, b = get_params_exp(x_data, y_data)
                print(f'Exponential fitting params: a={a}, b={b}')
                y_yield = a*np.exp(b*x_yield)  # 注意这里的x_yield是横轴数据

            elif self.fitting_params['method'] == 'Logarithmic fitting':
                mask = x_data > 0  # 确保x值为正
                def get_params_log(x, y):
                    if mask.sum()<2:
                        a,b = 1, np.mean(y_data)
                        return a, b
                    else:
                        a,b = np.polyfit(np.log(x[mask]), y[mask], 1)
                        return a, b
                    
                a, b = get_params_log(x_data, y_data)
                print(f'Logarithmic fitting params: a={a}, b={b}')
                y_yield = a * np.log(x_yield) + b

            return x_yield,y_yield


    def update_interpolation(self,event,method, points):
        self.interp_params['method'] = method
        self.interp_params['points'] = points

    def interpolation_tl(self):
        itl =  ttk.Toplevel(self.root)
        itl.title('數據插值設置')
        itl.geometry('400x300')
        cb_label = ttk.Label(itl,text='模式',bootstyle='inverse-light')
        scale = ttk.Scale(
            itl, from_=10, to=150, length=250,orient='horizontal', bootstyle='light',command=lambda event : print(scale.get()))
        #绑定用lambda event：来获取scale的值，event是tkinter自动传入的事件对象
        scale.set(50)
        sc_label = ttk.Label(itl,text='插值点(每单位10-150)',bootstyle='inverse-light')
        sc_label.place(x=50,y= 35)
        scale.place(x=50, y=75)
        cb_label.place(x=50,y= 135)
        cb = ttk.Combobox(itl,bootstyle = 'light',width=16,state='readonly',values=['Cubic Spline','Lagrange','Linear','Nearest Neighbor'])
        #cb.bind('<<ComboboxSelected>>', lambda event: self.update_interpolation(event, cb.get(), 300))
        cb.place(x=50,y=165)

        cb.set('Cubic Spline')  # 设置默认值为三次样条曲线插值

        itl.protocol("WM_DELETE_WINDOW", lambda: [self.update_interpolation(None, cb.get(), int(scale.get())), 
                                                  print(f'method : {self.interp_params["method"]}, points : {self.interp_params["points"]}'),
                                                  itl.destroy()])   
        #关闭窗口时更新参数，需要绑定destroy事件，否则无法正确关闭窗口


    def interpolation(self):
        if self.combbox.get() == '插值':
            x_data = self.load_x_data()
            y_data =  self.load_y_data()

            x_yield = np.linspace(x_data.min(),x_data.max(),self.interp_params['points'])
            
            if self.interp_params['method'] == 'Cubic Spline':
                f = interp1d(x_data, y_data, kind='cubic')
                
            elif self.interp_params['method'] == 'Lagrange':
                f = interp1d(x_data, y_data, kind='quadratic')
                
            elif self.interp_params['method'] == 'Linear':
                f = interp1d(x_data, y_data, kind='linear')
                
            elif self.interp_params['method'] == 'Nearest Neighbor':
                f = interp1d(x_data, y_data, kind='nearest')
                

            y_yield = f(x_yield)
            return x_yield,y_yield
        
    def load_photo(self,img): 
        pil_img = open(img)
        pil_img = pil_img.resize((750,750))
        # 创建一个与tkinter兼容的图像对象
        photo = PhotoImage(pil_img)
        children = self.photo_frame.winfo_children()
        if not children:
            photo_label = ttk.Label(self.photo_frame, image=photo)
            photo_label.image = photo
            photo_label.pack()
        else:
            #不清除原来的子控件，节省响应时间
            photo_label = children[0]
            photo_label.config(image=photo)  # 重新设置photo_label的image属性
            photo_label.image = photo  # 保持对photo的引用

    def plot(self):
        if self.combbox.get() == '輸入表達式計算':
            x,y = self.calculate()
            if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
                plt.plot(x,y)
                if self.input_unit.get() != '' and self.output_unit.get() != '':
                    plt.xlabel(f'{self.var_name.get()}/{self.input_unit.get()}')
                    plt.ylabel(f'{self.output.get()}/{self.output_unit.get()}')
                else:
                    plt.xlabel(f'{self.var_name.get()}')
                    plt.ylabel(f'{self.output.get()}')
                if self.title.get() != '':
                    plt.title(self.title.get())
                plt.grid(True)
                plt.show()

        elif self.combbox.get() == '給定縱軸數據':
            x = self.load_x_data()
            y = self.load_y_data()
            if len(x) != 0 and len(y) != 0:
                if len(x) != len(y):
                    messagebox.showerror("Error", "請確保橫軸和縱軸數據的長度相同")
                    return
                if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
                    plt.plot(x,y)
                    if self.input_unit.get() != '' and self.output_unit.get() != '':
                        plt.xlabel(f'{self.var_name.get()}/{self.input_unit.get()}')
                        plt.ylabel(f'{self.output.get()}/{self.output_unit.get()}')
                    else:
                        plt.xlabel(f'{self.var_name.get()}')
                        plt.ylabel(f'{self.output.get()}')
                    if self.title.get() != '':
                        plt.title(self.title.get())
                    plt.grid(True)
                    plt.show()

        elif self.combbox.get() == '插值':
            x,y = self.interpolation()
            plt.plot(self.load_x_data(), self.load_y_data(), 'o', label='原始數據')
            if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
                plt.plot(x,y, label='插值結果')
                if self.input_unit.get() != '' and self.output_unit.get() != '':
                    plt.xlabel(f'{self.var_name.get()}/{self.input_unit.get()}')
                    plt.ylabel(f'{self.output.get()}/{self.output_unit.get()}')
                else:
                    plt.xlabel(f'{self.var_name.get()}')
                    plt.ylabel(f'{self.output.get()}')
                if self.title.get() != '':
                    plt.title(self.title.get())
                plt.grid(True)
                plt.legend()
                plt.show()

        elif self.combbox.get() == '數據擬合':
            x,y = self.fitting()
            plt.plot(self.load_x_data(), self.load_y_data(), 'o', label='原始數據')
            if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
                plt.plot(x,y, label='擬合結果')
                if self.input_unit.get() != '' and self.output_unit.get() != '':
                    plt.xlabel(f'{self.var_name.get()}/{self.input_unit.get()}')
                    plt.ylabel(f'{self.output.get()}/{self.output_unit.get()}')
                else:
                    plt.xlabel(f'{self.var_name.get()}')
                    plt.ylabel(f'{self.output.get()}')
                if self.title.get() != '':
                    plt.title(self.title.get())
                plt.grid(True)
                plt.legend()
                plt.show()

    def save_result(self):
        pass

use('TkAgg')  # 使用TkAgg后端
# 设置全局字体为支持中文的字体
plt.rcParams['font.sans-serif'] = ['KaiTi']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
ploter = ploter()

