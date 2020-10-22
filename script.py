import os;
import re;
import shutil;
from threading import Timer;
default_directory = os.getcwd();
def initialize_config():
    
    default_config_string = "Src directory=\"C:\Projects\Bookmarker(WEB)\"\nDst directory=\"F:\Bookmarker copier\"\nDelete at src=False\nCheck interval in seconds=60";


    src_dir_path = "";
    dst_dir_path = "";
    config_exists = os.path.isfile("config.txt");
    if(config_exists == False):
        f = open("config.txt", "w");
        f.write(default_config_string);
    
    
    f = open("config.txt");
    lines = f.readlines();
    temp = lines[0];
    temp = temp.replace("\n", "");
    temp = re.search("\"(?P<path>[^\"]+)\"", temp);
    src_dir_path = temp.group("path");
    temp = lines[1];
    temp = temp.replace("\n", "");
    temp = re.search("\"(?P<path>[^\"]+)\"", temp);
    dst_dir_path = temp.group("path");
    temp = lines[2];
    temp = temp.replace("\n", "");
    temp = re.search("\=(?P<bool>.+)$", temp);
    delete_at_src = temp.group("bool");
    temp = lines[3];
    temp = temp.replace("\n", "");
    temp = re.search("\=(?P<num>.+)$", temp);
    check_interval = int(temp.group("num"));
    if(delete_at_src == "False"):
        delete_at_src = False;
    else:
        delete_at_src = True;



    return src_dir_path, dst_dir_path, delete_at_src, check_interval;
def delete_all_files(files):
    for file_path in files:
        if(re.match(".*\.\w+$", file_path)):
            try:
                os.unlink(file_path);
            except:
                print("exception");
        else:
            
            
            try:
                shutil.rmtree(file_path);
            except:
                print("exception");
    pass;
def get_all_files_in_directory(path):
    
    os.chdir(path);
    full_paths = [os.path.abspath(x) for x in os.listdir()];
    names = os.listdir();
    
    return full_paths, names;  

def copy_all_files_into_destination(files, dst_path):
    for file_path in files:
        if(re.match(".*\.\w+$", file_path)):
            try:
                shutil.copy2(file_path, dst_path);
            except:
                print("exception");
        else:
            temp = re.search(r"\\(?P<folder_name>[^\\]+)$", file_path);
            new_path = dst_path + "\\" + temp.group("folder_name");
            try:
                shutil.copytree(file_path, new_path);
            except:
                print("exception");
    pass;

def execute(src_dir_path, dst_dir_path, delete_at_src, check_interval):
    full_paths_src, names_src = get_all_files_in_directory(src_dir_path);
    full_paths_dst, names_dst = get_all_files_in_directory(dst_dir_path);
    full_paths_not_in_dst = [];
    for i in range(0, len(names_src)):
        if(names_src[i] not in names_dst):
            full_paths_not_in_dst.append(full_paths_src[i]);
    copy_all_files_into_destination(full_paths_not_in_dst, dst_dir_path);
    if(delete_at_src == True):
        delete_all_files(full_paths_not_in_dst);
    temp = Timer(check_interval, execute, [src_dir_path, dst_dir_path, delete_at_src, check_interval]);
    temp.start();
    pass;

def main():
    src_dir_path, dst_dir_path, delete_at_src, check_interval = initialize_config();
    execute(src_dir_path, dst_dir_path, delete_at_src, check_interval);
    
    
    
    
    



if __name__ == "__main__":
    main();
