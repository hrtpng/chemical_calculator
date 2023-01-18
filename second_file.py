import tkinter as tk
from tkinter import ttk

from chemlib import Element
from chemlib import Compound

# boron = Element('B')
# print(boron.properties)
# print(boron.AtomicMass)
# ftor = Element('F')
# print(ftor.properties)
# acetic_acid = Compound('CH3COOH')
# print(acetic_acid)
# alkohol = Compound('C2H5OH')
# print(alkohol)
# print(alkohol.molar_mass())


class GUI:
    def __init__(self, pressing):
        self.pressing = pressing

        self.background_color = 'white'
        self.OPERATIONS = [
            'g/L to mol/L', 'mol/L to g/L',
            'g/L to % in 100 ml', '% in 100 ml to g/L',
            'mol/L to % in 100 ml', '% in 100 ml to mol/L',
            'g/mol to M in solution']

        self.create_frames()
        self.create_buttons()


    def create_frames(self):
        self.window = tk.Tk()
        self.window.geometry('628x350')
        self.window.title('Chemistry calculator')
        self.window.configure(background=self.background_color)
        self.welcome_frame = tk.Label(self.window, text='Welcome to chemistry calculator',
                                      height=2, width=78)
        self.welcome_frame.grid(column=0, row=0)
        self.common_frame = tk.Frame(self.window)
        self.common_frame.grid(column=0, row=1, sticky=tk.NSEW)
        self.text_frame_convert = tk.Label(self.common_frame, text='Convert: ',
                                           height=2, width=25)
        self.text_frame_convert.grid(column=0, row=1, sticky=tk.W)
        self.text_frame_for_formula = tk.Entry(self.common_frame, width=52)
        self.text_frame_for_formula.grid(column=1, row=0, columnspan=7, sticky=tk.E)
        # добивить текст(или не здесь)

        self.first_frame_for_convert = tk.Text(self.common_frame, height=1, width=8)
        self.first_frame_for_convert.grid(column=2, row=1, sticky=tk.W)
        
        self.second_frame_for_convert = tk.Text(self.common_frame, height=1, width=8)
        self.second_frame_for_convert.grid(column=4, row=1)
        
        self.third_frame_for_convert = tk.Text(self.common_frame, height=1, width=8)
        self.third_frame_for_convert.grid(column=6, row=1, sticky=tk.E)


        self.frame_for_history = tk.Text(
            self.common_frame, height=12, width=52)
        self.frame_for_history.grid(column=1, row=3, rowspan=7, columnspan=7, sticky=tk.E)

    def texts_for_convert(self, text1, text2, text3=None):
        if text3 is None:
            self.third_frame_for_convert.grid_remove()
        if text3 is not None:
            self.third_frame_for_convert.grid()
        self.first_text_for_convert = tk.Label(self.common_frame, text=text1,
                                           height=1, width=8)
        self.first_text_for_convert.grid(column=3, row=1, sticky=tk.W)

        self.second_text_for_convert = tk.Label(self.common_frame, text=text2,
                                           height=1, width=8)
        self.second_text_for_convert.grid(column=5, row=1, sticky=tk.W)

        self.third_text_for_convert = tk.Label(self.common_frame, text=text3,
                                           height=1, width=8)
        self.third_text_for_convert.grid(column=7, row=1, sticky=tk.W)

    def create_buttons(self):
        self.molar_mass_button = tk.Button(self.common_frame, command=self.pressing('molar mass'),
                                           text='Calculate molar mass', height=1, width=15)
        self.molar_mass_button.grid(column=0, row=0, sticky=tk.W)
        row_index = 1
        for operation in self.OPERATIONS:
            row_index = row_index + 1
            self.buttons = tk.Button(self.common_frame, text=operation,
                                     command=self.pressing(operation), height=1, width=15)
            self.buttons.grid(column=0, row=row_index, sticky=tk.W)
        self.convert_button = tk.Button(self.common_frame, text='Convert',
                                        command=self.pressing('Convert'), height=1, width=10)
        self.convert_button.grid(column=6, row=2, columnspan=2, sticky=tk.E)

    def update_history(self, result):
        history = '\n'.join(result)
        self.frame_for_history.delete('1.0', tk.END)
        self.frame_for_history.insert(tk.END, history)

    def show(self):
        self.window.mainloop()


class Calculator:
    def __init__(self):
        self.last_operation = ''
        self.history = []
        self.gui = GUI(self.pressing)
        self.gui.show()

    def add_history_item(self, action, formula, output, input=None):
        item = {'action': action, 'formula': formula,
                'input': input, 'output': output}
        self.history.append(item)
        formated_history = []
        for elem in self.history:
            if elem['input'] is None:
                formated_history.append( elem['formula'] + ': ' + '\n' + elem['action'] + str(elem['output']))
            else:
                formated_history.append( elem['formula'] + ': ' + '\n' + elem['action'] + str(elem['output']), str(elem['input']))   
        self.gui.update_history(formated_history)

    def molar_mass(self):
        self.compound = Compound(self.gui.text_frame_for_formula.get())
        self.molar_massa = self.compound.molar_mass()
        return self.molar_massa

    def pressing(self, button_type: str):
        def press_button():
            if button_type == 'molar mass':
                self.molar_mass()
                print(self.compound, '\n', self.compound.molar_mass())
                self.add_history_item(
                    button_type, self.compound.formula, self.compound.molar_mass())
            if button_type in self.gui.OPERATIONS:
                if button_type == 'g/L to mol/L':
                    self.gui.texts_for_convert('g /', 'L', 'mol/l')
                if button_type == 'mol/L to g/L':
                    self.gui.texts_for_convert('mol/L', 'g / ', 'L')
                if button_type == 'g/L to % in 100 ml':
                    self.gui.texts_for_convert('g /', 'L', '% / 100 ml')
                if button_type == '% in 100 ml to g/L':
                    self.gui.texts_for_convert('% / 100 ml', 'g /', 'L',)
                if button_type == 'mol/L to % in 100 ml':
                    self.gui.texts_for_convert('mol/L', '% / 100 ml')
                if button_type == '% in 100 ml to mol/L':
                    self.gui.texts_for_convert('% / 100 ml', 'mol/L')
                if button_type == 'g/mol to M in solution':
                    self.gui.texts_for_convert('M', 'L')   
                


                # self.gui.frame_for_convert.insert(tk.END, button_type)
                # self.gui.text_frame_for_formula.insert(
                #     tk.END, 'Enter the chemical formula')
                self.last_operation = button_type
            if button_type == 'Convert':
                if self.last_operation == 'g/L to mol/L':
                    massa = float(self.molar_mass())
                    gramm = float(self.gui.frame_for_convert.get('1.0', 'end'))
                    result = gramm / massa
                    print(result)
            print(self.history)
        return press_button


calc = Calculator()
