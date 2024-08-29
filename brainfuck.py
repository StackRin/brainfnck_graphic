import tkinter as tk
import os
from tkinter import messagebox, filedialog


def clean_up(code):
    code = code.replace(" ", "\0")
    code = code.replace("\t", "\0")
    return code


def sign_output():
    global input_var
    input_var.set(input_var.get() + '.')
    result.set('')


def sign_clear():
    global input_var
    str = input_var.get()
    str = str[:-1]
    input_var.set(str)
    result.set("")


def sign_left_scope():
    global input_var
    input_var.set(input_var.get() + '[')


def sign_right_scope():
    global input_var
    input_var.set(input_var.get() + ']')


def sign_plus():
    global input_var
    input_var.set(input_var.get() + '+')


def sign_minus():
    global input_var
    input_var.set(input_var.get() + '-')


def sign_left_arrow():
    global input_var
    input_var.set(input_var.get() + '<')


def sign_right_arrow():
    global input_var
    input_var.set(input_var.get() + '>')


def sign_input():
    global input_var
    input_var.set(input_var.get() + ",")


class BrainfuckInterpreter:
    def __init__(self):
        self.memory = [0] * 30000
        self.ptr = 0
        self.output = ""
        self.loop_stack = []
        self.code = ""
        self.ip = 0

    def output_char(self):
        """输出当前内存指针指向位置的字符"""
        global result
        result.set(result.get() + chr(self.memory[self.ptr]))

    def input_char(self):
        """从用户输入读取一个字符并存储在当前内存指针位置"""
        char = input("Input character: ")[0]
        self.memory[self.ptr] = ord(char)

    def sign_plus(self):
        self.memory[self.ptr] = (self.memory[self.ptr] + 1) % 256

    def sign_minus(self):
        self.memory[self.ptr] = (self.memory[self.ptr] - 1) % 256

    def sign_left_arrow(self):
        self.ptr -= 1
        if self.ptr < 0:
            self.ptr = 0

    def sign_right_arrow(self):
        self.ptr += 1
        if self.ptr >= len(self.memory):
            self.memory.extend([0] * (self.ptr - len(self.memory) + 1))

    def sign_left_scope(self):
        if self.memory[self.ptr] != 0:
            self.loop_stack.append(self.ip)

    def sign_right_scope(self):
        if len(self.loop_stack) > 0:
            if self.memory[self.ptr] > 0:
                self.ip = self.loop_stack[-1]
            else:
                self.loop_stack.pop()

    def sign_run(self):
        global input_var

        var = input_var.get()
        try:
            while self.ip < len(var):
                if var[self.ip] == "+":
                    self.sign_plus()
                elif var[self.ip] == "-":
                    self.sign_minus()
                elif var[self.ip] == "<":
                    self.sign_left_arrow()
                elif var[self.ip] == ">":
                    self.sign_right_arrow()
                elif var[self.ip] == ".":
                    self.output_char()
                elif var[self.ip] == ",":
                    self.input_char()
                elif var[self.ip] == "[":
                    self.sign_left_scope()
                elif var[self.ip] == "]":
                    self.sign_right_scope()
                self.ip += 1

        except Exception as e:
            result.set(str(e))


def on_maximize():
    global format_font, input_var_label, result_label
    format_font = ("Arial", 22)
    input_var_label.config(font=format_font)
    result_label.config(font=format_font)


def insert_from_file():
    global input_var
    file_path = tk.filedialog.askopenfilename(title="选择脚本", filetypes=[("Brainfuck", "*.txt")])
    bfr_file = open(file_path, 'r')
    input_var.set(bfr_file.read())


def on_restore():
    global format_font, input_var_label, result_label
    format_font = ("Arial", 12)
    input_var_label.config(font=format_font)
    result_label.config(font=format_font)


def check_maximized():
    window_state = root.wm_state()
    if window_state == "zoomed":
        on_maximize()
    else:
        on_restore()
    root.after(100, check_maximized)


root = tk.Tk()
root.title("Brainfuck Interpreter")
format_font = ("Arial", 12)
root.geometry("600x400")
root.wm_maxsize()
bf = BrainfuckInterpreter()
# 设置窗口大小自适应
for i in range(6):  # 假设有5列
    root.columnconfigure(i, weight=1)
for i in range(6):  # 假设有6行
    root.rowconfigure(i, weight=1)

menu = tk.Menu(root)
file_menu = tk.Menu(menu, tearoff=False)
file_menu.add_command(label="重置",command=lambda: input_var.set(""))
file_menu.add_command(label="打开", command=insert_from_file)
file_menu.add_command(label="退出", command=root.quit)
menu.add_cascade(label="文件", menu=file_menu)
root.config(menu=menu)
# 输入
input_var = tk.StringVar()
input_var.set("")
input_var_label = tk.Entry(root, textvariable=input_var, name='input_var', font=format_font, width=20,
                           justify=tk.LEFT,
                           )
input_var_label.grid(row=1, column=1, columnspan=4, sticky="ew")
# 输出
result = tk.StringVar()
result.set(" ")
result_split = tk.StringVar()
result_split.set(" ")
result_label = tk.Label(root, textvariable=result, name='result_var', height=2, width=20, justify=tk.LEFT, anchor=tk.E)
result_label.grid(row=2, column=1, columnspan=4, sticky="ew")

# 按钮
button_plus = tk.Button(root, text='+', relief=tk.FLAT, bg='#eacda1', command=sign_plus)
button_minus = tk.Button(root, text='-', relief=tk.FLAT, bg='#eacda1', command=sign_minus)
button_left_bracket = tk.Button(root, text='[', relief=tk.FLAT, bg='#eacda1', command=sign_left_scope)
button_right_bracket = tk.Button(root, text=']', relief=tk.FLAT, bg='#eacda1', command=sign_right_scope)
button_left_arrow = tk.Button(root, text='<', relief=tk.FLAT, bg='#eacda1', command=sign_left_arrow)
button_right_arrow = tk.Button(root, text='>', relief=tk.FLAT, bg='#eacda1', command=sign_right_arrow)
button_output = tk.Button(root, text='.', relief=tk.FLAT, bg='#eacda1', command=sign_output)
button_input = tk.Button(root, text=',', relief=tk.FLAT, bg='#eacda1', command=sign_input)
button_left_clear = tk.Button(root, text='c', relief=tk.FLAT, bg='#eacda1', command=sign_clear)
button_right_run = tk.Button(root, text='run', relief=tk.FLAT, bg='#eacda1', command=bf.sign_run)

# 按钮布局
button_plus.grid(row=4, column=1, sticky="nsew", padx=4, pady=2)
button_minus.grid(row=5, column=1, sticky="nsew", padx=4, pady=2)
button_left_bracket.grid(row=4, column=2, sticky="nsew", padx=4, pady=2)
button_right_bracket.grid(row=5, column=2, sticky="nsew", padx=4, pady=2)
button_left_arrow.grid(row=4, column=3, sticky="nsew", padx=4, pady=2)
button_right_arrow.grid(row=5, column=3, sticky="nsew", padx=4, pady=2)
button_output.grid(row=4, column=4, sticky="nsew", padx=4, pady=2)
button_input.grid(row=5, column=4, sticky="nsew", padx=4, pady=2)
button_left_clear.grid(row=4, column=5, sticky="nsew", padx=4, pady=2)
button_right_run.grid(row=5, column=5, sticky="nsew", padx=4, pady=2)

# ... (其他代码保持不变)
check_maximized()
root.mainloop()
