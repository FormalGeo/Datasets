import os
import shutil
from formalgeo.tools import load_json, safe_save_json


def check_dataset(path_dataset):
    legal_files = {'diagrams', 'files', 'gdl', 'problems', 'info.json', 'LICENSE', 'REAMDE.md'}
    dataset_files = set(os.listdir(path_dataset))

    legal = True
    if len(dataset_files - legal_files) > 0:
        print("Redundant files: {}".format(dataset_files - legal_files))
        legal = False
    if len(legal_files - dataset_files) > 0:
        print("Missing files: {}".format(legal_files - dataset_files - {'diagrams', 'expanded', 'files'}))
        legal = False

    if not legal:
        msg = "Dataset checking not passed."
        raise Exception(msg)


def release():
    path_projects = "../../../projects"
    path_released = "../../../released"

    if not os.path.exists(path_projects):
        msg = "Path '{}' not exists.".format(path_projects)
        raise Exception(msg)
    check_dataset(path_projects)

    if not os.path.exists(path_released):
        os.makedirs(path_released)

    info = load_json(os.path.join(path_projects, "info.json"))
    info["downloads"] = ""
    filename = "{}_{}".format(info["dataset_name"], info["dataset_version"])
    path_released_filename = f"../../../released/{filename}"

    print("Packing... (It may take a few minutes)")
    shutil.make_archive(path_released_filename, 'gztar', path_projects)

    safe_save_json({filename: info}, os.path.join(path_released, f"{filename}_released.json"))


if __name__ == '__main__':
    release()
