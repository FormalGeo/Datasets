import os
from formalgeo.tools import load_json


def get_authors(authors_email):
    authors = {"problem": {}, "img": {}}
    for filename in os.listdir("problems/"):
        author = load_json(f"problems/{filename}")["annotation"].split("_")[0]
        if author in authors["problem"]:
            authors["problem"][author] += 1
        else:
            authors["problem"][author] = 1
        author = load_json(f"problems/{filename}")["annotation_img"].split("_")[0]
        if author in authors["img"]:
            authors["img"][author] += 1
        else:
            authors["img"][author] = 1
    total = load_json("info.json")["problem_number"]
    text = "People who contributed to formalgeo7k-v2."

    sorted_authors = dict(sorted(authors["problem"].items(), key=lambda item: item[1], reverse=True))
    text += f"\n\n\n{total} problems contributed by {len(sorted_authors)} authors:\n"
    for author in sorted_authors:
        one_author = "{} <> ({}, {:.2f}%)\n".format(
            author, sorted_authors[author], sorted_authors[author] / total * 100)
        if author in authors_email:
            one_author = one_author.replace("<>", "<{}>".format(authors_email[author]))
        text += one_author

    sorted_authors = dict(sorted(authors["img"].items(), key=lambda item: item[1], reverse=True))
    text += f"\n{total} diagrams contributed by {len(sorted_authors)} authors:\n"
    for author in sorted_authors:
        one_author = "{} <> ({}, {:.2f}%)\n".format(
            author, sorted_authors[author], sorted_authors[author] / total * 100)
        if author in authors_email:
            one_author = one_author.replace("<>", "<{}>".format(authors_email[author]))
        text += one_author

    print(text)


if __name__ == '__main__':
    working_directory = "../../../../projects/formalgeo7k-v2"
    os.chdir(working_directory)

    email = {
        "XiaokaiZhang": "xiaokaizhang1999@163.com",
        "NaZhu": "nazhu@shu.edu.cn",
        "YimingHe": "hym123@shu.edu.cn",
        "JiaZou": "zouj@shu.edu.cn",
        "QikeHuang": "qkhuang112@163.com",
        "XiaoxiaoJin": "leo_jxx@163.com",
        "YanjunGuo": "yanjunguo@163.com",
        "ChenyangMao": "shadymao@shu.edu.com",
        "ZheZhu": "zhuzhe@shu.edu.cn",
        "DengfengYue": "ydf@shu.edu.cn",
        "FangzhenZhu": "zhufz@shu.edu.cn",
        "YangLi": "laying2000@outlook.com",
        "YifanWang": "wangyifan0216@shu.edu.cn",
        "YiwenHuang": "15967121844@163.com",
        "RunanWang": "luckyrunan@163.com",
        "ChengQin": "karllonrenz@outlook.com",
        "ZhengyuHu": "huzhengyu2016@gmail.com"
    }
    get_authors(email)
