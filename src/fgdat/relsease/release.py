import json
import os
import shutil
from formalgeo.tools import load_json, safe_save_json
from tqdm import tqdm


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


def copy_tree(src, dst):
    print("Calculating file number...")
    tree = list(os.walk(src))

    total = 0
    for path, _, files in tree:
        total += len(files)

    pbar = tqdm(total=total, unit_scale=True, desc='Copying Dataset')
    for path, _, files in tree:
        dst_path = os.path.join(dst, os.path.relpath(path, src))
        os.makedirs(dst_path, exist_ok=True)

        for file in files:
            src_file = os.path.join(path, file)
            dst_file = os.path.join(dst_path, file)
            if file.endswith(".json"):  # compress json
                data = load_json(src_file)
                with open(dst_file, 'w') as f:
                    json.dump(data, f, separators=(',', ':'))
            else:
                shutil.copy(src_file, dst_file)

            pbar.update(1)
    pbar.update(total - pbar.n)


def release(path_dataset, path_released="../../../released"):
    if not os.path.exists(path_dataset):
        msg = "Path '{}' not exists.".format(path_dataset)
        raise Exception(msg)
    check_dataset(path_dataset)

    info = load_json(os.path.join(path_dataset, "info.json"))
    filename = "{}_{}".format(info["dataset_name"], info["dataset_version"])
    path_cache = os.path.join(path_released, filename)

    shutil.copy(os.path.join(path_dataset, "info.json"), os.path.join(path_released, "{}.json".format(filename)))
    copy_tree(path_dataset, path_cache)

    print("Packing... (It may take a few minutes)")
    shutil.make_archive(path_cache, 'gztar', path_cache)

    print("Removing cache... (It may take a few minutes)")
    shutil.rmtree(path_cache)

    released = load_json(os.path.join(path_released, "released.json"))
    released[filename] = info
    safe_save_json(released, os.path.join(path_released, "released.json"))


if __name__ == '__main__':
    release("../../../projects/formalgeo7k")
    release("../../../projects/formalgeo-imo")
