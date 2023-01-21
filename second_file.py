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
            'g to mmol', 'mmol to g',
            'g/mol to M in solution']

        self.remove_formula_on = ['', 'Enter the chemical formula', 'You forgot to enter the fomula']

        self.create_frames()
        self.create_buttons()


    def create_frames(self):
        self.window = tk.Tk()
        self.window.geometry('628x355')
        self.window.title('Chemistry calculator')
        self.window.configure(background=self.background_color)
        self.welcome_frame = tk.Label(self.window, text='Welcome to chemistry calculator' )
        self.welcome_frame.pack(expand=True, fill='both')
        self.common_frame = tk.Frame(self.window)
        self.common_frame.pack(expand=True, fill='both')

        self.text_frame_convert = tk.Label(self.common_frame, text='Convert: ',
                                           height=2, width=25)
        self.text_frame_convert.grid(column=0, row=2, sticky=tk.W)

        self.text_frame_for_formula = tk.Entry(self.common_frame, width=52)
        self.text_frame_for_formula.grid(column=1, row=0, columnspan=7, sticky=tk.E)
        def clear_formula_frame(event):
            if self.text_frame_for_formula.get() in self.remove_formula_on:
                self.text_frame_for_formula.delete(0, tk.END)
        self.text_frame_for_formula.bind('<Button-1>', clear_formula_frame)
        self.frame_for_history = tk.Text(self.common_frame, height=12, width=52)
        self.frame_for_history.grid(column=1, row=3, rowspan=7, columnspan=7, sticky=tk.E)
    
    def frames_for_convert(self):
        self.first_frame_for_convert = tk.Text(self.common_frame, height=1, width=8)
        self.first_frame_for_convert.grid(column=2, row=1, sticky=tk.W)
        
        self.second_frame_for_convert = tk.Text(self.common_frame, height=1, width=8)
        self.second_frame_for_convert.grid(column=4, row=1)
        

    def texts_for_convert(self, text1, text2=None):
        if text2 is None:
            self.second_frame_for_convert.grid_remove()
        self.first_text_for_convert = tk.Label(self.common_frame, text=text1,
                                           height=1, width=8)
        self.first_text_for_convert.grid(column=3, row=1, sticky=tk.W)

        self.second_text_for_convert = tk.Label(self.common_frame, text=text2,
                                           height=1, width=8)
        self.second_text_for_convert.grid(column=5, row=1, sticky=tk.W)

        self.text_frame_enter = tk.Label(self.common_frame, text='Enter: ',
                                           height=2, width=25)
        self.text_frame_enter.grid(column=0, row=1, sticky=tk.W)

    def clear_input(self):
        if self.first_frame_for_convert != '':
                self.first_frame_for_convert.delete(1.0, tk.END)
                self.second_frame_for_convert.delete(1.0, tk.END)


    def create_buttons(self):
        self.molar_mass_button = tk.Button(self.common_frame, command=self.pressing('molar mass'),
                                           text='Calculate molar mass', height=1, width=15)
        self.molar_mass_button.grid(column=0, row=0, sticky=tk.W)
        row_index = 2
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
                formated_history.append( elem['formula'] + ': ' 
                + '\n' + 'Molar mass: ' + str(elem['output']) 
                + '\n' + elem['action'] + ': ' 
                + '\n' + self.gui.first_frame_for_convert.get('1.0', 'end')
                + self.gui.second_frame_for_convert.get('1.0', 'end')
                + str(elem['input']) + '\n' + '\n') 
        self.gui.update_history(formated_history[::-1])

    def molar_mass(self):
        self.compound = Compound(self.gui.text_frame_for_formula.get())
        self.molar_massa = self.compound.molar_mass()
        return self.molar_massa

    def pressing(self, button_type: str):
        def press_button():
            if button_type == 'molar mass':
                print(repr(self.gui.text_frame_for_formula.get()))
                if self.gui.text_frame_for_formula.get() in self.gui.remove_formula_on:
                    self.gui.text_frame_for_formula.delete(0, tk.END)
                    self.gui.text_frame_for_formula.insert(tk.END, 'You forgot to enter the fomula')
                    return
                self.molar_mass()
                print(self.compound, '\n', self.compound.molar_mass())
                self.add_history_item(
                    button_type, self.compound.formula, self.compound.molar_mass())
            if button_type in self.gui.OPERATIONS:
                if self.gui.text_frame_for_formula.get() in self.gui.remove_formula_on:
                    self.gui.text_frame_for_formula.delete(0, tk.END)
                    self.gui.text_frame_for_formula.insert(tk.END, 'Enter the chemical formula')
                self.gui.frames_for_convert()
                if button_type == 'g/L to mol/L':
                    self.gui.texts_for_convert('g /', 'L')
                if button_type == 'mol/L to g/L':
                    self.gui.texts_for_convert('mol/L')
                if button_type == 'g to mmol':
                    self.gui.texts_for_convert('g')
                if button_type == 'mmol to g':
                    self.gui.texts_for_convert('mmol')
                if button_type == 'g/mol to M in solution':
                    self.gui.texts_for_convert('M')

                self.last_operation = button_type
            if button_type == 'Convert':
                if self.gui.text_frame_for_formula.get() in self.gui.remove_formula_on:
                    self.gui.text_frame_for_formula.delete(0, tk.END)
                    self.gui.text_frame_for_formula.insert(tk.END, 'You forgot to enter the fomula')
                    return
                if self.gui.first_frame_for_convert.get('1.0', 'end') == '\n':
                     self.gui.first_frame_for_convert.insert(tk.END, 'Error')
                     return
                if self.last_operation == 'g/L to mol/L':
                    if self.gui.second_frame_for_convert.get('1.0', 'end') == '\n':
                     self.gui.second_frame_for_convert.insert(tk.END, 'eror')
                     return
                    massa = float(self.molar_mass())
                    gramm = float(self.gui.first_frame_for_convert.get('1.0', 'end'))
                    litr = float(self.gui.second_frame_for_convert.get('1.0', 'end'))
                    result = gramm / massa * litr

                if self.last_operation == 'mol/L to g/L':
                    massa = float(self.molar_mass())
                    mol = float(self.gui.first_frame_for_convert.get('1.0', 'end'))
                    result = mol * massa

                if self.last_operation == 'g to mmol':
                    massa = float(self.molar_mass())
                    gramm = float(self.gui.first_frame_for_convert.get('1.0', 'end'))
                    result = gramm / massa * 1000

                if self.last_operation == 'mmol to g':
                    massa = float(self.molar_mass())
                    mmol = float(self.gui.first_frame_for_convert.get('1.0', 'end'))
                    result = mmol / 1000 * massa

                if self.last_operation == 'g/mol to M in solution':
                    massa = float(self.molar_mass())
                    mol = float(self.gui.first_frame_for_convert.get('1.0', 'end'))
                    result = massa * mol

                self.add_history_item(
                    self.last_operation, self.compound.formula, self.compound.molar_mass(), result)

                self.gui.clear_input()
        
                    

            print(self.history)
        return press_button


calc = Calculator()
