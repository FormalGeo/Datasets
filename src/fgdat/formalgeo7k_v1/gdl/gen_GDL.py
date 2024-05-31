import os.path
from formalgeo.tools import load_json, save_json
from fgdat.files import overwrite


def gen_predicate_gdl(path_dataset):
    if not overwrite(os.path.join(path_dataset, "gdl/predicate_GDL.json")):
        return

    predicate_gdl_source = load_json(os.path.join(path_dataset, "files", "predicate_GDL-source.json"))
    entity = {}
    for name in predicate_gdl_source["Predicates"]["Entity"]:
        entity[name] = predicate_gdl_source["Predicates"]["Entity"][name]["body"]
    relation = {}
    for name in predicate_gdl_source["Predicates"]["Relation"]:
        relation[name] = predicate_gdl_source["Predicates"]["Relation"][name]["body"]
    attr = {}
    for name in predicate_gdl_source["Predicates"]["Attribution"]:
        attr[name] = predicate_gdl_source["Predicates"]["Attribution"][name]["body"]
    predicate_gdl = {
        "Preset": predicate_gdl_source["Predicates"]["Preset"],
        "Entity": entity,
        "Relation": relation,
        "Attribution": attr
    }

    save_json(predicate_gdl, os.path.join(path_dataset, "gdl", "predicate_GDL.json"))


def gen_theorem_gdl(path_dataset):
    if not overwrite(os.path.join(path_dataset, "gdl/theorem_GDL.json")):
        return

    theorem_gdl_source = load_json(os.path.join(path_dataset, "files", "theorem_GDL-source.json"))
    theorem_gdl = {}
    for name in theorem_gdl_source["Theorems"]:
        theorem_gdl[name] = theorem_gdl_source["Theorems"][name]["body"]

    save_json(theorem_gdl, os.path.join(path_dataset, "gdl", "theorem_GDL.json"))


def deal_item(title, items):
    doc = "    " + title + ": "
    space = " " * len(doc)
    if len(items) > 0:
        doc += items[0] + "\n"
        for i in range(1, len(items)):
            doc += space + items[i] + "\n"
    else:
        doc += "\n"

    return doc


def gen_doc(path_dataset, language):
    filename = "doc_{}.md".format(language)
    if not overwrite(os.path.join(path_dataset, "gdl", filename)):
        return

    predicate_gdl_source = load_json(os.path.join(path_dataset, "files", "predicate_GDL-source.json"))

    with open(os.path.join(path_dataset, "files", "preset_{}.md".format(language)), 'r', encoding='utf-8') as file:
        doc = file.read()

    if language == "cn":
        doc += "## 自定义谓词\n### 实体\n"
    else:
        doc += "## Custom Predicate\n### Entity\n"

    for entity in predicate_gdl_source["Predicates"]["Entity"]:
        entity_name = entity.split("(")[0]
        doc += "#### {}\n".format(entity)
        doc += "<div>\n    <img src=\"pic/{}.png\" alt=\"{}\" width=\"{}%\">\n</div>\n\n".format(
            entity_name,
            entity_name,
            predicate_gdl_source["Predicates"]["Entity"][entity]["pic_width"]
        )
        doc += deal_item("ee_check", predicate_gdl_source["Predicates"]["Entity"][entity]["body"]["ee_check"])
        doc += deal_item("multi", predicate_gdl_source["Predicates"]["Entity"][entity]["body"]["multi"])
        doc += deal_item("extend", predicate_gdl_source["Predicates"]["Entity"][entity]["body"]["extend"])
        doc += "\n**Description**:  \n{}\n\n".format(
            predicate_gdl_source["Predicates"]["Entity"][entity]["doc_{}".format(language)])

    if language == "cn":
        doc += "### 实体关系\n"
    else:
        doc += "### Relation\n"
    for relation in predicate_gdl_source["Predicates"]["Relation"]:
        relation_name = relation.split("(")[0]
        doc += "#### {}\n".format(relation)
        doc += "<div>\n    <img src=\"pic/{}.png\" alt=\"{}\" width=\"{}%\">\n</div>\n\n".format(
            relation_name,
            relation_name,
            predicate_gdl_source["Predicates"]["Relation"][relation]["pic_width"])
        doc += deal_item("ee_check", predicate_gdl_source["Predicates"]["Relation"][relation]["body"]["ee_check"])
        if "fv_check" in predicate_gdl_source["Predicates"]["Relation"][relation]["body"]:
            doc += deal_item("fv_check", predicate_gdl_source["Predicates"]["Relation"][relation]["body"]["fv_check"])
        doc += deal_item("multi", predicate_gdl_source["Predicates"]["Relation"][relation]["body"]["multi"])
        doc += deal_item("extend", predicate_gdl_source["Predicates"]["Relation"][relation]["body"]["extend"])
        doc += "\n**Description**:  \n{}\n\n".format(
            predicate_gdl_source["Predicates"]["Relation"][relation]["doc_{}".format(language)])

    if language == "cn":
        doc += "### 实体属性\n"
    else:
        doc += "### Attribution\n"
    for attr in predicate_gdl_source["Predicates"]["Attribution"]:
        attr_name = attr.split("(")[0]
        doc += "#### {}\n".format(attr)
        doc += "<div>\n    <img src=\"pic/{}.png\" alt=\"{}\" width=\"{}%\">\n</div>\n\n".format(
            attr_name,
            attr_name,
            predicate_gdl_source["Predicates"]["Attribution"][attr]["pic_width"]
        )
        doc += deal_item("ee_check", predicate_gdl_source["Predicates"]["Attribution"][attr]["body"]["ee_check"])
        if "fv_check" in predicate_gdl_source["Predicates"]["Attribution"][attr]["body"]:
            doc += deal_item("fv_check", predicate_gdl_source["Predicates"]["Attribution"][attr]["body"]["fv_check"])
        doc += deal_item("multi", predicate_gdl_source["Predicates"]["Attribution"][attr]["body"]["multi"])
        doc += "    sym: {}\n".format(predicate_gdl_source["Predicates"]["Attribution"][attr]["body"]["sym"])
        doc += "\n**Description**:  \n{}\n\n".format(
            predicate_gdl_source["Predicates"]["Attribution"][attr]["doc_{}".format(language)])

    theorem_gdl_source = load_json(os.path.join(path_dataset, "files", "theorem_GDL-source.json"))

    if language == "cn":
        doc += "## 自定义定理\n"
    else:
        doc += "## Custom Theorem\n"
    for t_name in theorem_gdl_source["Theorems"]:
        theorem_name = t_name.split("(")[0]
        doc += "#### {}\n".format(t_name)
        doc += "<div>\n    <img src=\"pic/{}.png\" alt=\"{}\" width=\"{}%\">\n</div>\n\n".format(
            theorem_name,
            theorem_name,
            theorem_gdl_source["Theorems"][t_name]["pic_width"])
        if len(theorem_gdl_source["Theorems"][t_name]["body"]) > 1:
            for b in theorem_gdl_source["Theorems"][t_name]["body"]:
                doc += "    # branch {}\n".format(b)
                doc += "    premise: {}\n".format(theorem_gdl_source["Theorems"][t_name]["body"][b]["premise"])
                doc += deal_item("conclusion", theorem_gdl_source["Theorems"][t_name]["body"][b]["conclusion"])
        else:
            doc += "    premise: {}\n".format(theorem_gdl_source["Theorems"][t_name]["body"]["1"]["premise"])
            doc += deal_item("conclusion", theorem_gdl_source["Theorems"][t_name]["body"]["1"]["conclusion"])
        doc += "\n**Description**:  \n{}\n\n".format(theorem_gdl_source["Theorems"][t_name]["doc_{}".format(language)])

    with open(os.path.join(path_dataset, "gdl", filename), 'w', encoding='utf-8') as f:
        f.write(doc)


if __name__ == '__main__':
    # gen_doc("../../../projects/formalgeo7k", "cn")
    # gen_doc("../../../projects/formalgeo7k", "en")
    # gen_predicate_gdl("../../../projects/formalgeo7k")
    # gen_theorem_gdl("../../../projects/formalgeo7k")

    gen_doc("../../../projects/formalgeo-imo", "cn")
    gen_doc("../../../projects/formalgeo-imo", "en")
    gen_predicate_gdl("../../../projects/formalgeo-imo")
    gen_theorem_gdl("../../../projects/formalgeo-imo")
