# tkinter
from tkinter import *
from tkinter import font
from tkinter import filedialog
from tkinter import messagebox

# idlelib
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator

# other imports
from os.path import exists
import json

# config files
theme = open('config/theme.json', 'r')
theme_data = json.load(theme)

save = open('config/save.json', 'r+')
save_data = json.load(save)

current_file = save_data['current_file']

# root
root = Tk()

root.iconbitmap('akins.ico')
root.title('Akins')
root.geometry('840x400')

root.resizable(False, False)
root.option_add('*tearOff', False)

# scrollbar
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

# text
txt = Text(root, yscrollcommand=scrollbar.set)
txt.pack(fill=BOTH)

scrollbar.config(command=txt.yview)

cdg = ColorDelegator()

cdg.tagdefs['COMMENT'] = {
    'foreground': theme_data['languages']['python']['comment']['color'],
    'background': theme_data['languages']['python']['comment']['background']
}

cdg.tagdefs['KEYWORD'] = {
    'foreground': theme_data['languages']['python']['keyword']['color'],
    'background': theme_data['languages']['python']['keyword']['background']
}

cdg.tagdefs['BUILTIN'] = {
    'foreground': theme_data['languages']['python']['builtin']['color'],
    'background': theme_data['languages']['python']['builtin']['background']
}

cdg.tagdefs['STRING'] = {
    'foreground': theme_data['languages']['python']['string']['color'],
    'background': theme_data['languages']['python']['string']['background']
}

cdg.tagdefs['DEFINITION'] = {
    'foreground': theme_data['languages']['python']['definition']['color'],
    'background': theme_data['languages']['python']['definition']['background']
}

cdg.tagdefs['SYNC'] = {
    'foreground': theme_data['languages']['python']['sync']['color'],
    'background': theme_data['languages']['python']['sync']['background']
}

cdg.tagdefs['TODO'] = {
    'foreground': theme_data['languages']['python']['todo']['color'],
    'background': theme_data['languages']['python']['todo']['background']
}

cdg.tagdefs['ERROR'] = {
    'foreground': theme_data['languages']['python']['error']['color'],
    'background': theme_data['languages']['python']['error']['background']
}

cdg.tagdefs['hit'] = {
    'foreground': theme_data['languages']['python']['hit']['color'],
    'background': theme_data['languages']['python']['hit']['background']
}

Percolator(txt).insertfilter(cdg)

# menus
menu = Menu(root)
root.config(menu=menu)

# file menu
file_m = Menu(menu)
menu.add_cascade(label='File', menu=file_m)

if not current_file == None and exists(current_file):
    file = open(current_file, 'r')
    content = file.read()

    txt.delete(1.0, END)
    txt.insert(END, content)
else:
    save.truncate(0)
    save.seek(0)

    current_file = None
    json.dump(save_data, save, indent=4, sort_keys=False)

# file menu functions
def save_file():
    file = filedialog.askopenfilename(initialdir='.', title='Create a file')

    if file == '':
        return

    file = open(file, 'w+')
    file.write(txt.get(1.0, END))

def open_file():
    file = filedialog.askopenfilename(initialdir='.', title='Open a file', filetypes=(
        ('All Files', '*.*'),
        ('Text Files', '*.txt'),
        ('Python Files', '*.py')
    ))
    
    save.truncate(0)
    save.seek(0)

    save_data['current_file'] = file
    json.dump(save_data, save, indent=4, sort_keys=False)

    if file == '':
        return

    file = open(file, 'r')
    content = file.read()

    txt.delete(1.0, END)
    txt.insert(END, content)

# file menu commands
file_m.add_command(label='Save File', command=save_file)
file_m.add_command(label='Open File', command=open_file)

# python menu
python_m = Menu(menu)
menu.add_cascade(label='Python', menu=python_m)

if not current_file == None and exists(current_file):
    file = open(current_file, 'r')
    content = file.read()

    txt.delete(1.0, END)
    txt.insert(END, content)
else:
    save.truncate(0)
    save.seek(0)

    current_file = None
    json.dump(save_data, save, indent=4, sort_keys=False)

# python menu functions
def run_file():
    with open(current_file) as current:
        exec(current.read())

# python menu commands
python_m.add_command(label='Run File', command=run_file)

# theming
txt.configure(
    bg=theme_data['editor']['background'],
    fg=theme_data['editor']['default_color'],
    insertbackground='#fff',
    highlightthickness=-1,
    font=font.Font(
        family=theme_data['editor']['font']['font_family'],
        size=theme_data['editor']['font']['font_size'],
        slant=theme_data['editor']['font']['slant'],
        weight=theme_data['editor']['font']['font_weight'],
        underline=theme_data['editor']['font']['underlined'],
        overstrike=theme_data['editor']['font']['strikethrough']
    )
)

if save_data['show_message'] == True:
    messagebox.showinfo(save_data['message_title'], save_data['message'])
    
    save.truncate(0)
    save.seek(0)

    save_data['show_message'] = False
    json.dump(save_data, save, indent=4, sort_keys=False)

# start main loop
root.mainloop()