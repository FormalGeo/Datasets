import os
import shutil
from formalgeo.tools import load_json, safe_save_json


def check_dataset():
    legal_files = {'diagrams', 'files', 'gdl', 'problems', 'info.json', 'LICENSE', 'REAMDE.md'}
    dataset_files = set(os.listdir())

    if len(legal_files - dataset_files) > 0:
        msg = "Missing files: {}".format(legal_files - dataset_files - {'diagrams', 'expanded', 'files'})
        raise Exception(msg)


def release():
    check_dataset()

    path_released = "../../released"
    if not os.path.exists(path_released):
        os.makedirs(path_released)

    info = load_json("info.json")
    info["downloads"] = ""
    filename = "{}_{}".format(info["dataset_name"], info["dataset_version"])

    path_released_filename = f"../../released/{filename}"
    path_released_info = f"../../released/{filename}_released.json"

    print("Packing... (It may take a few minutes)")
    shutil.make_archive(path_released_filename, 'gztar', "./")

    safe_save_json({filename: info}, path_released_info)


if __name__ == '__main__':
    working_directory = "../../../../projects/formalgeo7k-v2"
    os.chdir(working_directory)

    release()
