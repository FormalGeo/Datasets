import os
from formalgeo.tools import load_json, save_json, get_user_input

cowork_log = {
    "weeks": {
        "1": [
            {"worker": "XiaokaiZhang", "dataset": "Geometry3k-Triangle", "pid": [1584, 1864]}
        ]
    },
    "date": {
        "1": "2023-03-12"
    }
}

expanded_log = {
    "break_pid": 1,
    "pid_count": 6982
}

inverse_parse_log = {
    "start_pid": 6982,
    "cn": {},
    "en": {}
}


def overwrite(filepath):
    if os.path.exists(filepath) and \
            get_user_input("'{}' already exists. Overwrite the file?".format(filepath)) == "n":
        return False
    return True


def get_authors(path_dataset, authors_email=None):
    if authors_email is None:
        authors_email = {}
    if not overwrite(os.path.join(path_dataset, "files/AUTHORS")):
        return

    authors = {}
    for filename in os.listdir(os.path.join(path_dataset, "problems/")):
        author = load_json(os.path.join(path_dataset, "problems/", filename))["annotation"].split("_")[0]
        if author in authors:
            authors[author] += 1
        else:
            authors[author] = 1
    authors = dict(sorted(authors.items(), key=lambda item: item[1], reverse=True))
    total = load_json(os.path.join(path_dataset, "info.json"))["problem_number"]
    text = "All people who contributed to {}.\n\n{} problems contributed by {} authors:\n\n".format(
        os.path.basename(os.path.normpath(path_dataset)),
        load_json(os.path.join(path_dataset, "info.json"))["problem_number"],
        len(authors)
    )
    for author in authors:
        one_author = "{} <> ({}, {:.2f}%)\n".format(author, authors[author], authors[author] / total * 100)
        if author in authors_email:
            one_author = one_author.replace("<>", "<{}>".format(authors_email[author]))
        text += one_author

    with open(os.path.join(path_dataset, "files/AUTHORS"), "w") as file:
        file.write(text)


def get_pid_mapping(path_dataset):
    if not overwrite(os.path.join(path_dataset, "files/pid_mapping.json")):
        return

    pid_mapping = {}
    for filename in sorted(os.listdir(os.path.join(path_dataset, "expanded")), key=lambda x: int(x.split(".")[0])):
        pid = int(filename.split(".")[0])
        data = load_json(os.path.join(path_dataset, "expanded", filename))
        for expanded_pid in data:
            pid_mapping[expanded_pid] = pid
        print("{} ok".format(filename))

    save_json(pid_mapping, os.path.join(path_dataset, "files/pid_mapping.json"))


def get_t_info(path_dataset):
    if not overwrite(os.path.join(path_dataset, "files/t_info.json")):
        return

    t_info = {}
    theorem_GDL_source = load_json(os.path.join(path_dataset, "files/theorem_GDL-source.json"))["Theorems"]
    for theorem in theorem_GDL_source:
        t_info[theorem.split("(")[0]] = [theorem_GDL_source[theorem]["category"], 0]

    for filename in os.listdir(os.path.join(path_dataset, "problems/")):
        for theorem in load_json(os.path.join(path_dataset, "problems/", filename))["theorem_seqs"]:
            t_info[theorem.split("(")[0]][1] += 1
        print("{} ok".format(filename))

    save_json(t_info, os.path.join(path_dataset, "files/t_info.json"))


if __name__ == '__main__':
    # get_authors("../../../projects/formalgeo7k",
    #             {"XiaokaiZhang": "xiaokaizhang1999@163.com", "NaZhu": "nazhu@shu.edu.cn",
    #              "YimingHe": "hym123@shu.edu.cn", "JiaZou": "zouj@shu.edu.cn", "QikeHuang": "qkhuang112@163.com",
    #              "XiaoxiaoJin": "leo_jxx@163.com", "YanjunGuo": "yanjunguo@163.com",
    #              "ChenyangMao": "shadymao@shu.edu.com", "ZheZhu": "zhuzhe@shu.edu.cn", "DengfengYue": "ydf@shu.edu.cn",
    #              "FangzhenZhu": "zhufz@shu.edu.cn", "YangLi": "laying2000@outlook.com",
    #              "YifanWang": "wangyifan0216@shu.edu.cn", "YiwenHuang": "15967121844@163.com",
    #              "RunanWang": "luckyrunan@163.com", "ChengQin": "karllonrenz@outlook.com"})
    # get_pid_mapping("../../../projects/formalgeo7k")
    # get_t_info("../../../projects/formalgeo7k")

    # get_authors("../../../projects/formalgeo-imo",
    #             {"XiaokaiZhang": "xiaokaizhang1999@163.com", "NaZhu": "nazhu@shu.edu.cn",
    #              "YimingHe": "hym123@shu.edu.cn", "JiaZou": "zouj@shu.edu.cn", "QikeHuang": "qkhuang112@163.com",
    #              "XiaoxiaoJin": "leo_jxx@163.com", "YanjunGuo": "yanjunguo@163.com",
    #              "ChenyangMao": "shadymao@shu.edu.com", "ZheZhu": "zhuzhe@shu.edu.cn", "DengfengYue": "ydf@shu.edu.cn",
    #              "FangzhenZhu": "zhufz@shu.edu.cn", "YangLi": "laying2000@outlook.com",
    #              "YifanWang": "wangyifan0216@shu.edu.cn", "YiwenHuang": "15967121844@163.com",
    #              "RunanWang": "luckyrunan@163.com", "ChengQin": "karllonrenz@outlook.com"})
    get_pid_mapping("../../../projects/formalgeo-imo")
    # get_t_info("../../../projects/formalgeo-imo")
