import os
from formalgeo.tools import load_json, save_json
from fgdat.files import overwrite


def format_predicate_gdl_source(path_dataset):
    if not overwrite(os.path.join(path_dataset, "predicate_GDL-source.json")):
        return

    data = load_json(os.path.join(path_dataset, "files/predicate_GDL-source.json"))
    new_data = {
        "Notes": data["Notes"],
        "Predicates": {
            "Preset": data["Predicates"]["Preset"],
            "Entity": {},
            "Relation": {},
            "Attribution": {}
        }
    }

    for p_class in ["Entity", "Relation", "Attribution"]:
        for p_name in data["Predicates"][p_class]:
            new_data["Predicates"][p_class][p_name] = {
                "body": data["Predicates"][p_class][p_name]["body"],
                "doc_cn": data["Predicates"][p_class][p_name]["doc_cn"],
                "doc_en": data["Predicates"][p_class][p_name]["doc_en"],
                "pic_width": data["Predicates"][p_class][p_name]["pic_width"],
                "anti_parse_to_nl_cn": data["Predicates"][p_class][p_name]["anti_parse_to_nl_cn"],
                "anti_parse_to_nl_en": data["Predicates"][p_class][p_name]["anti_parse_to_nl_en"],
            }

    save_json(new_data, os.path.join(path_dataset, "files/predicate_GDL-source.json"))


def format_theorem_gdl_source(path_dataset):
    if not overwrite(os.path.join(path_dataset, "theorem_GDL-source.json")):
        return

    data = load_json(os.path.join(path_dataset, "files/theorem_GDL-source.json"))
    new_data = {
        "Notes": data["Notes"],
        "Theorems": {}
    }

    for p_name in data["Theorems"]:
        new_data["Theorems"][p_name] = {
            "body": data["Theorems"][p_name]["body"],
            "doc_cn": data["Theorems"][p_name]["doc_cn"],
            "doc_en": data["Theorems"][p_name]["doc_en"],
            "pic_width": data["Theorems"][p_name]["pic_width"],
            "category": data["Theorems"][p_name]["category"],
        }

    save_json(new_data, os.path.join(path_dataset, "files/theorem_GDL-source.json"))


if __name__ == '__main__':
    format_predicate_gdl_source("../../../projects/formalgeo7k")
    format_theorem_gdl_source("../../../projects/formalgeo7k")
