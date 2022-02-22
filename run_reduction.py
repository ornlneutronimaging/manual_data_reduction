import sys
import os
import glob

REDUCTION_SCRIPT = 'mcp_detector_correction.py --skipimg'
DEBUGGING = True


def is_folder_contains_fits(folder_name):
    """check if the folder provided contain any fits file, data that need to be reduced"""

    list_fits = glob.glob(os.path.join(folder_name, '*.fits'))
    if len(list_fits) == 0:
        return False
    return True


def build_output_path(folder_name):
    path_parsed = folder_name.split("/")
    facility = path_parsed[0]
    instrument = path_parsed[1]
    ipts = path_parsed[2]
    shared = 'shared'
    autoreduce = 'autoreduce'
    # images = path_parsed[3]
    # mcp = path_parsed[4]
    folder_structure_to_keep = os.path.sep.join(path_parsed[5:])

    if DEBUGGING:
        facility = '/Volumes/G-DRIVE/IPTS/'

    base_output_folder = os.path.sep.join([facility, instrument, ipts, shared, autoreduce, folder_structure_to_keep])
    return base_output_folder


def get_list_inside_folders(folder_name):
    """return the list of inside folders"""
    list_inside_files = glob.glob(os.path.join(folder_name, '*'))
    list_inside_folders = []
    for _file in list_inside_files:
        if os.path.isdir(_file):
            list_inside_folders.append(_file)

    return list_inside_folders


def run_reduction(list_folders=None):
    if list_folders is None:
        return

    for _folder in list_folders:

        if is_folder_contains_fits(_folder):

            output_path = build_output_path(_folder)
            input_path = _folder

            cmd = f"{REDUCTION_SCRIPT} {input_path} {output_path}"
            print(cmd)
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
