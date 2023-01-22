import tkinter as tk

from chemlib import Compound

class GUI:
    def __init__(self, on_click_builder):
        self.on_click_builder = on_click_builder

        self.background_color = 'white'
        self.operations = {
            'g/L to mol/L': {'input_names': ['g/', 'L'], 'result': 'mol/L'},
            'mol/L to g/L': {'input_names': ['mol/L'], 'result': 'g/L'},
            'g to mmol': {'input_names': ['g'], 'result': 'mmol'},
            'mmol to g': {'input_names': ['mmol'], 'result': 'g'},
            'g/mol to M in solution': {'input_names': ['M'], 'result': 'g/L'}
        }

        self.first_frame_for_convert = None
        self.second_frame_for_convert = None

        self.create_frames()
        self.create_buttons()

    def create_frames(self):
        self.window = tk.Tk()
        self.window.geometry('640x355')
        self.window.resizable(False, False)
        self.window.title('Chemistry calculator')
        self.window.configure(background=self.background_color)
        self.welcome_label = tk.Label(self.window, text='Welcome to chemistry calculator')
        self.welcome_label.pack(expand=True, fill='both')
        self.common_frame = tk.Frame(self.window)
        self.common_frame.pack(expand=True, fill='both')

        self.convertion_options_label = tk.Label(self.common_frame, text='Convertion options:', height=2)
        self.convertion_options_label.grid(column=0, row=2, padx=(0, 65))

        self.formula_entry = tk.Entry(self.common_frame, width=52)
        self.formula_entry.grid(column=1, row=0, columnspan=7, sticky=tk.E)

        def clear_formula_frame(event):
            self.replace_formula_entry_text()

        self.formula_entry.bind('<Button-1>', clear_formula_frame)
        
        self.frame_for_history = tk.Text(
            self.common_frame, height=10, width=52)
        self.frame_for_history.grid(
            column=1, row=3, rowspan=5, columnspan=7, sticky=tk.E)
        scrollbar = tk.Scrollbar(self.common_frame, orient='vertical',
            command=self.frame_for_history.yview)
        scrollbar.grid(row=3, column=8, rowspan=5, sticky=tk.NS)
        self.frame_for_history['yscrollcommand'] = scrollbar.set
        self.set_scrollbar_end()

    def set_scrollbar_end(self):
        self.frame_for_history.see('end')

    def replace_formula_entry_text(self, text: str = None):
        remove_formula_on = [
            '', 'Enter the chemical formula', 'You forgot to enter the fomula']
        if self.formula_entry.get() in remove_formula_on:
            self.formula_entry.delete(0, tk.END)
            if text is not None:
                self.formula_entry.insert(tk.END, text)
            return True

    def texts_for_convert(self, text1, text2=None):
        if self.first_frame_for_convert:
            self.first_frame_for_convert.grid_remove()
        if self.second_frame_for_convert:
            self.second_frame_for_convert.grid_remove()

        self.first_frame_for_convert = tk.Text(
            self.common_frame, height=1, width=8)
        self.first_frame_for_convert.grid(column=3, row=1, sticky=tk.W)
        if text2:
            self.second_frame_for_convert = tk.Text(
                self.common_frame, height=1, width=8)
            self.second_frame_for_convert.grid(column=5, row=1)
        self.first_text_for_convert = tk.Label(
            self.common_frame, text=text1, height=1, width=8)
        self.first_text_for_convert.grid(column=4, row=1, sticky=tk.W)

        self.second_text_for_convert = tk.Label(
            self.common_frame, text=text2, height=1, width=8)
        self.second_text_for_convert.grid(column=6, row=1, sticky=tk.W)

        self.enter_label = tk.Label(self.common_frame, text='Enter: ', height=2)
        self.enter_label.grid(column=1, row=1, sticky=tk.W)

    def clear_inputs(self):
        self.clear_first_input()
        self.clear_second_input()

    def clear_first_input(self):
        if self.first_frame_for_convert:
            self.first_frame_for_convert.delete(1.0, tk.END)

    def clear_second_input(self):
        if self.second_frame_for_convert:
            self.second_frame_for_convert.delete(1.0, tk.END)

    def create_buttons(self):
        self.molar_mass_button = tk.Button(self.common_frame, command=self.on_click_builder('molar mass'),
                                           text='Calculate molar mass', height=1, width=15)
        self.molar_mass_button.grid(column=0, row=0, sticky=tk.W)
        row_index = 2
        for operation in self.operations:
            row_index = row_index + 1
            self.buttons = tk.Button(self.common_frame, text=operation,
                                     command=self.on_click_builder(operation), height=1, width=15)
            self.buttons.grid(column=0, row=row_index, sticky=tk.W)
        self.convert_button = tk.Button(self.common_frame, text='Convert',
                                        command=self.on_click_builder('Convert'), height=1, width=10)
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
        self.molar_massa = 0
        self.gui = GUI(self.on_click_builder)

    def add_history_item(self, action, formula, output, input=None):
        item = {'action': action, 'formula': formula, 'input': input, 'output': output}
        self.history.append(item)
        formated_history = []
        for elem in self.history:
            if elem['input'] is None:
                h = f"{elem['formula']}:\n"
                h += f"{elem['action']}: {elem['output']}"
                formated_history.append(h)
            else:
                formatting = self.gui.operations[self.last_operation]

                h = f"{elem['formula']}:\n"
                h += f"Molar mass: {elem['output']}\n"
                h += f"{elem['action']}:\n"
                first_val = self.gui.first_frame_for_convert.get(
                    '1.0', 'end').strip()
                h += f"{first_val} {formatting['input_names'][0]}"
                if len(formatting['input_names']) == 2:
                    second_val = self.gui.second_frame_for_convert.get(
                        '1.0', 'end').strip()
                    h += f" {second_val} {formatting['input_names'][1]}"
                h += f" = {elem['input']} {formatting['result']} \n"
                h += '=' * 15
                formated_history.append(h)

        self.gui.update_history(formated_history[::-1])

    def molar_mass(self):
        try:
            self.compound = Compound(self.gui.formula_entry.get())
            self.molar_massa = self.compound.molar_mass()
            return self.molar_massa
        except:
            return None

    def on_click_builder(self, button_type: str):
        def on_click():
            if button_type == 'molar mass':
                self.on_molar_mass_click()
            if button_type in self.gui.operations:
                self.on_operations_click(button_type)
            if button_type == 'Convert':
                self.on_convert_click()
        return on_click

    def on_molar_mass_click(self):
        if self.gui.replace_formula_entry_text('You forgot to enter the fomula'):
            return

        res = self.molar_mass()
        if res is None:
            return
        self.add_history_item('molar mass', self.compound.formula, round(
            self.compound.molar_mass(), 3))

    def on_operations_click(self, button_type):
        self.gui.replace_formula_entry_text('Enter the chemical formula')
        input_names = self.gui.operations[button_type]['input_names']
        self.gui.texts_for_convert(*input_names)
        self.last_operation = button_type

    def on_convert_click(self):
        if self.gui.replace_formula_entry_text('You forgot to enter the fomula'):
            return
        if self.gui.first_frame_for_convert.get('1.0', 'end') == '\n' or  not self.is_number(self.gui.first_frame_for_convert.get('1.0', 'end')):
            self.gui.clear_first_input()
            self.gui.first_frame_for_convert.insert(tk.END, 'Error')
            return

        res = self.molar_mass()
        if res is None:
            return
        massa = float(self.molar_massa)
        first_entry_value = float(
            self.gui.first_frame_for_convert.get('1.0', 'end'))
        if self.last_operation == 'g/L to mol/L':
            if self.gui.second_frame_for_convert.get('1.0', 'end') == '\n' or  not self.is_number(self.gui.second_frame_for_convert.get('1.0', 'end')):
                self.gui.clear_second_input()
                self.gui.second_frame_for_convert.insert(tk.END, 'Error')
                return
            litr = float(self.gui.second_frame_for_convert.get('1.0', 'end'))
            result = first_entry_value / massa * litr

        if self.last_operation == 'mol/L to g/L':
            result = first_entry_value * massa

        if self.last_operation == 'g to mmol':
            result = first_entry_value / massa * 1000

        if self.last_operation == 'mmol to g':
            result = first_entry_value / 1000 * massa

        if self.last_operation == 'g/mol to M in solution':
            result = massa * first_entry_value

        self.add_history_item(
            self.last_operation, self.compound.formula, round(self.compound.molar_mass(), 3), round(result, 3))

        self.gui.clear_inputs()

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

calc = Calculator()
calc.gui.show()
