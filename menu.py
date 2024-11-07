import math
import tkinter as tk
from math import inf
from tkinter import ttk
from main import genetic_algorithm, genetic_algorithm_binary

chromosomes_list = None
population_generated = False
current_best_genes = None
current_best_eval = math.inf
coding_type: tk.StringVar
crossingover_type: tk.StringVar


# SCHITAEM CHROMOSOMUSHKI
def chromosome_calculation():
    global chromosomes_list, population_generated
    global current_best_eval, current_best_genes
    MUTATION_CHANCE = mutation_prob_entry.get()
    CHROMOSOME_COUNT = chromosomes_count_entry.get()
    GENES_BOUNDS = (min_gen_entry.get(), max_gen_entry.get())
    NUM_ITERS = generation_number_spinbox.get()

    new_generation_counter_num = str(int(generations_counter_text.get(1.0, tk.END)) + int(NUM_ITERS))
    generations_counter_text.config(state=tk.NORMAL)
    generations_counter_text.delete(1.0, tk.END)
    generations_counter_text.insert(1.0, new_generation_counter_num)
    generations_counter_text.config(state=tk.DISABLED)

    coding = coding_type.get()
    crossingover = crossingover_type.get()

    if coding == "вещественное":
        genetic_algorithm_func = genetic_algorithm
    else:
        genetic_algorithm_func = genetic_algorithm_binary

    params = {
        'chromosomes_number': CHROMOSOME_COUNT,
        'bounds': GENES_BOUNDS,
        'mutation_chance': MUTATION_CHANCE,
        'crossover_chance': 50,
        'generations_number': int(NUM_ITERS),
        'previous_population': chromosomes_list if population_generated else None,
        'crossingover_type': crossingover
    }

    if crossingover == "обычный кроссинговер":
        chromosomes_list, best_genes, best_eval = genetic_algorithm_func(**params)
    else:
        params['crossingover_type'] = "modded"
        chromosomes_list, best_genes, best_eval = genetic_algorithm_func(**params)

    population_generated = True
    if best_eval < current_best_eval:
        current_best_eval = best_eval
        current_best_genes = best_genes

    best_genes_formatted = (f'x[1]: {current_best_genes[0]}\n'
                            f'x[2]: {current_best_genes[1]}')
    best_solution_text.config(state=tk.NORMAL)
    best_solution_text.delete(1.0, tk.END)
    best_solution_text.insert("1.0", best_genes_formatted)
    best_solution_text.config(state=tk.DISABLED)

    best_min_value_text.config(state=tk.NORMAL)
    best_min_value_text.delete(1.0, tk.END)
    best_min_value_text.insert("1.0", current_best_eval + 12)
    best_min_value_text.config(state=tk.DISABLED)

    for item in tree.get_children():
        tree.delete(item)
    for index, chromosome in enumerate(chromosomes_list):
        tree.insert("", tk.END, values=(index + 1, chromosome.result, chromosome.gene_1, chromosome.gene_2))


class EditableTreeview(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind("<Double-1>", self.on_double_click)
        self.entry = None

    def on_double_click(self, event):
        item = self.selection()[0]
        column = self.identify_column(event.x)

        current_value = self.item(item, "values")[int(column[1:]) - 1]

        if self.entry is not None:
            self.entry.destroy()

        x, y, width, height = self.bbox(item, column)
        self.entry = tk.Entry(self)
        self.entry.insert(0, current_value)
        self.entry.place(x=x + self.winfo_x(), y=y + self.winfo_y(), width=width)

        self.entry.focus()
        self.entry.bind("<Return>", lambda e: self.save_edit(item, column))
        self.entry.bind("<FocusOut>", lambda e: self.cancel_edit())

    def save_edit(self, item, column):
        new_value = int(self.entry.get())
        column_index = int(column[1:]) - 1
        values = list(self.item(item, "values"))
        values[column_index] = new_value
        self.item(item, values=values)

        self.entry.destroy()
        self.entry = None

    def cancel_edit(self):
        if self.entry is not None:
            self.entry.destroy()
            self.entry = None


root = tk.Tk()
root.geometry("1600x900")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=5)
root.rowconfigure(0, weight=1)

# create frames
left_frame = tk.Frame(root, borderwidth=2, relief="groove")
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

parameters_frame = tk.Frame(left_frame, borderwidth=2, relief="groove")
parameters_frame.pack(pady=5, padx=5, fill='both', expand=True)

control_frame = tk.Frame(left_frame, borderwidth=2, relief="groove")
control_frame.pack(pady=5, padx=5, fill='both', expand=True)

results_frame = tk.Frame(left_frame, borderwidth=2, relief="groove")
results_frame.pack(pady=5, padx=5, fill='both', expand=True)

chromosomes_frame = tk.Frame(root, borderwidth=2, relief="groove")
chromosomes_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
chromosomes_frame.columnconfigure(0, weight=1)
chromosomes_frame.rowconfigure(0, weight=1)


def create_label_entry(frame, label_text, default_value):
    row = frame.grid_size()[1]
    label = tk.Label(frame, text=label_text, font=("Helvetica", 12))
    label.grid(row=row, column=0, sticky="e")
    entry_var = tk.IntVar(frame)
    entry_var.set(default_value)
    entry = tk.Entry(frame, textvariable=entry_var)
    entry.grid(row=row, column=1)
    return entry_var


# parameters frame
func_name_lbl = tk.Label(parameters_frame,
                         text="Функция: -12x[2] + 4x[1]^2 + 4x[2]^2 -4x[1]x[2]",
                         font=("Helvetica", 12))
func_name_lbl.grid(row=0, columnspan=2)

mutation_prob_entry = create_label_entry(parameters_frame, "Вероятность мутации,%: ", 50)
chromosomes_count_entry = create_label_entry(parameters_frame, "Количество хромосом: ", 50)
max_gen_entry = create_label_entry(parameters_frame, "Максимальное значение гена: ", 50)
min_gen_entry = create_label_entry(parameters_frame, "Минимальное значение гена: ", -50)

# control frame
calculate_chromosomes_btn = tk.Button(control_frame, text="Рассчитать хромосомы",
                                      command=lambda: chromosome_calculation())
calculate_chromosomes_btn.grid(row=0, columnspan=2, pady=5)

generation_number_lbl = tk.Label(control_frame, text="Количество поколений: ")
generation_number_lbl.grid(row=1, column=0)
default_value_spinbox = tk.IntVar(control_frame)
default_value_spinbox.set(100)
generation_number_spinbox = tk.Spinbox(control_frame,
                                       from_=1,
                                       to=inf,
                                       increment=1,
                                       textvariable=default_value_spinbox)
generation_number_spinbox.grid(row=1, column=1)

generations_counter_lbl = tk.Label(control_frame,
                                   text="Количество прошлых поколений: ")
generations_counter_lbl.grid(row=2, column=0)

generations_counter_text = tk.Text(control_frame,
                                   height=1,
                                   width=30)
generations_counter_text.grid(row=2, column=1)
generations_counter_text.insert("1.0", "0")
generations_counter_text.config(state=tk.DISABLED)

# results frame
best_solution_lbl = tk.Label(results_frame,
                             text="Лучшее решение: ",
                             font=("Helvetica", 12))
best_solution_lbl.grid(row=0, columnspan=2)

best_solution_text = tk.Text(results_frame,
                             height=10,
                             width=50)
best_solution_text.grid(row=1, columnspan=2)
best_solution_text.config(state=tk.DISABLED)

best_min_value_lbl = tk.Label(results_frame,
                              text="Значение функции: ",
                              font=("Helvetica", 12))
best_min_value_lbl.grid(row=2, columnspan=2)

best_min_value_text = tk.Text(results_frame,
                              height=1,
                              width=30)
best_min_value_text.grid(row=3, columnspan=2)
best_min_value_text.config(state=tk.DISABLED)

# spreadsheet
columns = ("number", "result", "gene_1", "gene_2")
tree = EditableTreeview(master=chromosomes_frame, columns=columns, show="headings")
tree.grid(row=0, column=0, sticky="nsew")
tree.heading("number", text="Номер", anchor="w")
tree.heading("result", text="Результат", anchor="w")
tree.heading("gene_1", text="Ген 1", anchor="w")
tree.heading("gene_2", text="Ген 2", anchor="w")
scrollbar = tk.Scrollbar(chromosomes_frame, orient="vertical", command=tree.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
tree.configure(yscrollcommand=scrollbar.set)


def confirm_selection():
    coding = coding_type.get()
    crossover = crossingover_type.get()
    print(f"Выбранный тип кодирования: {coding}")
    print(f"Выбранный тип кодирования: {crossover}")
    selection_window.destroy()


def open_selection_window():
    global selection_window
    selection_window = tk.Toplevel(root)
    selection_window.title("Выбрать тип кодирования и кроссинговера")

    global coding_type
    global crossingover_type
    coding_type = tk.StringVar(value="вещественное")
    crossingover_type = tk.StringVar(value="обычный кроссинговер")

    coding_label = tk.Label(selection_window, text="Выберите тип кодирования:")
    coding_label.pack(pady=10)

    float_radio = ttk.Radiobutton(selection_window, text="вещественное", variable=coding_type, value="вещественное")
    binary_radio = ttk.Radiobutton(selection_window, text="двоичное", variable=coding_type, value="двоичное")
    float_radio.pack(anchor=tk.W)
    binary_radio.pack(anchor=tk.W)

    crossover_label = tk.Label(selection_window, text="Выберите тип кроссовера:")
    crossover_label.pack(pady=10)

    basic_crossover_radio = ttk.Radiobutton(selection_window, text="обычный кроссинговер", variable=crossingover_type,
                                            value="обычный кроссинговер")
    cx_crossover_radio = ttk.Radiobutton(selection_window, text="модифицированный кроссинговер",
                                         variable=crossingover_type,
                                         value="модифицированный кроссинговер")
    basic_crossover_radio.pack(anchor=tk.W)
    cx_crossover_radio.pack(anchor=tk.W)

    confirm_button = ttk.Button(selection_window, text="Подтвердить", command=confirm_selection)
    confirm_button.pack(pady=20)


open_selection_button = tk.Button(parameters_frame, text="Выбрать тип кодировки и кроссинговера",
                                  command=open_selection_window)
open_selection_button.grid(row=5, column=0, pady=10, columnspan=2)

root.mainloop()
