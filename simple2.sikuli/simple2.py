import json
import os
import sys
from collections import defaultdict

"""
context path : u'pom.xml', u'C:\\Users\\cguoq\\.jenkins\\workspace\\decrypt-job\\CriminalCode-admin-web', u'pom.png'
"""

default_dict = defaultdict(list)
base_path = os.path.join(os.getcwd(), sys.argv[1])
config_path = os.path.join(os.getcwd(), sys.argv[2])
workspace_path = sys.argv[3]

with open(config_path, 'r') as config:
    config_content = json.load(config)

def create_png_image(file_name):
    image_name = file_name.split(".")[0] + ".png"
    file = os.path.join(base_path, image_name)
    if not os.path.exists(file):
        command = "python create_png_file.py " + file_name
        os.chdir(base_path)
        os.system('cmd /c {}'.format(command))

    return image_name

for key, value in config_content.items():
    default_dict[key].append(value)
    image_name = create_png_image(value)
    #default_dict[key][0] = workspace_path + default_dict[key][1].encode('utf-8')
    default_dict[key].append(workspace_path + key)
    default_dict[key].append(image_name)
    print("project path value is: {}".format(default_dict[key]))

#def compile_package_project(path):
#    os.chdir(path)
#    build_package_process()

def build_package_process(sleep = 5):
    os.system('cmd /c {}'.format("mvn clean"))
    wait(sleep)
    os.system('cmd /c {}'.format("mvn install"))
    wait(sleep)
    os.system('cmd /c {}'.format("mvn package"))
    wait(sleep)

def wait_and_click(image,time=3,similarity=0.7,offsetx=0,offsety=0):
    wait(image,time)
    click(Pattern(image).similar(similarity).targetOffset(offsetx,offsety),time)

def click_and_wait(image,time=2,similarity=0.7,offsetx=0,offsety=0):
    click(Pattern(image).similar(similarity).targetOffset(offsetx,offsety),time)
    wait(time)

def rightclick_pattern(image,time=3,similarity=0.7,offsetx=-30,offsety=0):
    click(image)
    rightClick(Pattern(image).similar(similarity).targetOffset(offsetx,offsety),time)
    wait(time)

def choose_language(similarity=0.7):
    print("start to choose language.")
    if exists(Pattern("sougou.png").similar(similarity)):
        click_and_wait("sougou.png")
        click_and_wait("english_language.png")
    if exists("english_language_icon.png"):
        pass
    if exists("pinyin.png") or exists("chn_pinyin.png"):
        click_and_wait("pinyin.png")
        click_and_wait("english_language.png")

def command_and_enter(command):
    type(command + "\n")
    wait(1)

def copy_all_then_close():
    print("start to copy config file content")
    type("a",KeyModifier.CTRL)
    type("c",KeyModifier.CTRL)
    type("w",KeyModifier.CTRL)

def create_new_file_and_save(time=3):
    print("start to create one new au3 file and save it")
    wait(time)
    type("n",KeyModifier.CTRL)
    wait(time)
    type("v",KeyModifier.CTRL)
    wait(time)
    type("s",KeyModifier.CTRL)

def copy_one_config_file(context):
    print("start to copy config file content")
    doubleClick("my_computer.png")
    wait_and_click("my_computer_bar.png")
    command_and_enter(context[1])
    rightclick_pattern(context[2])
    click_and_wait("notepad_plus.png")
    wait_and_click("active_notepad_plus.png",offsetx=-21,offsety=-14)
    copy_all_then_close()

def save_config_content_to_scite():
    print("start to save config content to scite")
    click_and_wait("search_icon.png")
    wait_and_click("search_bar.png",2)
    type("SciTE")
    wait_and_click("scite_icon.png")
    create_new_file_and_save()

def save_new_au3_file(context):
    print("start to save config file to au3.")
    file_prefix = context[0].split(".")[0]
    wait_and_click("save_file_path_bar.png",offsetx=280,offsety=30)
    command_and_enter(context[1])
    click("file_name_bar.png")
    type(file_prefix)
    click("save_icon.png")
    print("save config file to au3")

def delete_and_rename_config_file(context):
    print("start to delete and rename config file")
    new_name = context[0].split(".")[0] + ".au3"
    delete_previous_config = "del " + context[0]
    rename_new_config_file = "rename "+ new_name + "  " + context[0]
    os.chdir(context[1])
    os.system('cmd /c {}'.format(delete_previous_config))
    os.system('cmd /c {}'.format(rename_new_config_file))

def close_all_windows():
    print("start to close all active windows.")
        
    def exist_close_icon():
        try:
            if exists("close_icon_normal.png") or exists("close_icon_expand.png"):
                return True
        except FindFailed:
            return False

    while True:
        if exist_close_icon():
            if exists("close_icon_normal.png"):
                click(Pattern("close_icon_normal.png").targetOffset(42,-4))
            if exists("close_icon_expand.png"):
                click(Pattern("close_icon_expand.png").targetOffset(41,-1))
            if exists("yes_icon.png"):
                click("yes_icon.png")
        else:
            break

    print("all the active windows are closed.")

def decrypt_one_config_file(context):
    copy_one_config_file(context)
    save_config_content_to_scite()
    save_new_au3_file(context)
    delete_and_rename_config_file(context)

for project_path,context in default_dict.items():
    print("context value is: {}".format(context))
    choose_language(similarity=0.85)
#    compile_package_project(context[0])
    decrypt_one_config_file(context)
    close_all_windows()

