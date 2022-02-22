import sys
import os
import glob
import subprocess

REDUCTION_SCRIPT = 'mcp_detector_correction.py --skipimg'
DEBUGGING = False


def is_folder_contains_fits(folder_name):
    """check if the folder provided contain any fits file, data that need to be reduced"""

    list_fits = glob.glob(os.path.join(folder_name, '*.fits'))
    if len(list_fits) == 0:
        return False
    return True


def build_output_path(folder_name):
    folder_name = os.path.abspath(folder_name)
    path_parsed = folder_name.split("/")
    facility = path_parsed[1]
    instrument = path_parsed[2]

    if instrument == 'snfs1':
        index_offset = 2
    else:
        index_offset = 0

    instrument = path_parsed[2+index_offset]
    ipts = path_parsed[3+index_offset]
    shared = 'shared'
    autoreduce = 'autoreduce'
    # images = path_parsed[4+index_offset]
    # mcp = path_parsed[5+index_offset]
    folder_structure_to_keep = os.path.sep.join(path_parsed[6+index_offset:])

    print(f"facility: {facility}")
    print(f"instrument: {instrument}")
    print(f"ipts: {ipts}")
    print(f"data folder: {folder_structure_to_keep}")

    if DEBUGGING:
        facility = '/Volumes/G-DRIVE/IPTS/'

    base_output_folder = os.path.sep.join([os.path.sep + facility, instrument, ipts, shared, autoreduce, folder_structure_to_keep])
    return base_output_folder


def get_list_inside_folders(folder_name):
    """return the list of inside folders"""
    list_inside_files = glob.glob(os.path.join(folder_name, '*'))
    list_inside_folders = []
    for _file in list_inside_files:
        if os.path.isdir(_file):
            list_inside_folders.append(_file)

    return list_inside_folders



def create_full_path(output_dir):
    if os.path.exists(output_dir):
        return
    os.makedirs(output_dir)



def run_reduction(list_folders=None):
    if list_folders is None:
        return

    for _folder in list_folders:

        _folder = os.path.abspath(_folder)

        if is_folder_contains_fits(_folder):

            output_path = build_output_path(_folder)
            print(f"creating output path: {output_path}") 
            create_full_path(output_path)

            input_path = _folder

            cmd = f"{REDUCTION_SCRIPT} {input_path} {output_path}"
            print(f"Running: {cmd}")
            
            proc = subprocess.Popen(cmd, shell=True,
                                    stdin=subprocess.PIPE,
                                    universal_newlines=True,
                                    cwd=output_path)
            proc.communicate()
            print(f"Done!")

            continue

        list_inside_folders = get_list_inside_folders(_folder)
        if len(list_inside_folders) == 0:
            continue

        run_reduction(list_folders=list_inside_folders)

        




if __name__ == '__main__':
    arguments = sys.argv

    if len(sys.argv) == 1:
        print("Please provide an input folder path!")
    else:
        list_folders = sys.argv[1:]
        run_reduction(list_folders=list_folders)
