import os.path
import string
import re
import random
from formalgeo.tools import load_json, save_json, safe_save_json
from fgdat.formalgeo7k_v1.problems.inverse_parse import parse_geo_predicate, inverse_parse_gdl
from fgdat.formalgeo7k_v1.problems.inverse_parse import inverse_parse_logic, parse_raw_gdl


class ParseError(Exception):

    def __init__(self, pid, message):
        self.pid = pid
        super().__init__(message)

    def __str__(self):
        return f"[ParseError(pid={self.pid})]: {self.args[0]}"


def inverse_parse_equal(s, language, gdl, log, pid):
    pattern1 = (r"^Equal\("
                r"LengthOfLine\([A-Z]{2}\)"
                r","
                r"LengthOfLine\([A-Z]{2}\)"
                r"\)$")
    pattern2 = (r"^Equal\("
                r"MeasureOfAngle\([A-Z]{3}\)"
                r","
                r"MeasureOfAngle\([A-Z]{3}\)"
                r"\)$")
    pattern3 = (r"^Equal\("
                r"MeasureOfArc\([A-Z]{3}\)"
                r","
                r"MeasureOfArc\([A-Z]{3}\)"
                r"\)$")
    pattern4 = (r"^Equal\("
                r"LengthOfLine\([A-Z]{2}\)"
                r","
                r"\s*[\d+\-*/a-z\s\(\)]+|\d+(\.\d+)?(?:\s*\w+\([\d+\-*/a-z\s\(\)]+\))*"
                r"\)$")
    pattern5 = (r"^Equal\("
                r"MeasureOfAngle\([A-Z]{3}\)"
                r","
                r"\s*[\d+\-*/a-z\s\(\)]+|\d+(\.\d+)?(?:\s*\w+\([\d+\-*/a-z\s\(\)]+\))*"
                r"\)$")
    pattern6 = (r"^Equal\("
                r"MeasureOfArc\([A-Z]{3}\)"
                r","
                r"\s*[\d+\-*/a-z\s\(\)]+|\d+(\.\d+)?(?:\s*\w+\([\d+\-*/a-z\s\(\)]+\))*"
                r"\)$")
    pattern7 = (r"^Equal\("
                r"[a-zA-Z]+\([A-Z,]+\)"
                r","
                r"[a-zA-Z]+\([A-Z,]+\)\)$")
    pattern8 = (r"Equal\("
                r"[a-zA-Z]+\([A-Z,]+\)"
                r","
                r"\s*[\d+\-*/a-z\s\(\)]+|\d+(\.\d+)?(?:\s*\w+\([\d+\-*/a-z\s\(\)]+\))*"
                r"\)$")
    pattern9 = (r"Equal\("  # Equal(a+b,c+3)
                r"\s*[\d+\-*/a-z\s\(\)]+|\d+(\.\d+)?(?:\s*\w+\([\d+\-*/a-z\s\(\)]+\))*"
                r","
                r"\s*[\d+\-*/a-z\s\(\)]+|\d+(\.\d+)?(?:\s*\w+\([\d+\-*/a-z\s\(\)]+\))*"
                r"\)$")
    pattern10 = (r"Equal\("  # Equal(Mul(LengthOfLine(IJ),LengthOfLine(YJ)),Mul(LengthOfLine(HJ),LengthOfLine(XJ)))
                 r"Mul\(LengthOfLine\([A-Z]{2}\),LengthOfLine\([A-Z]{2}\)\)"
                 r","
                 r"Mul\(LengthOfLine\([A-Z]{2}\),LengthOfLine\([A-Z]{2}\)\)"
                 r"\)$")
    pattern11 = (r"^Equal\("  # Equal(LengthOfLine(AG),Mul(LengthOfLine(HA),2))
                 r"LengthOfLine\([A-Z]{2}\)"
                 r","
                 r"Mul\(LengthOfLine\([A-Z]{2}\),\s*[\d+\-*/a-z\s\(\)]+|\d+(\.\d+)?(?:\s*\w+\([\d+\-*/a-z\s\(\)]+\))*\)"
                 r"\)$")
    pattern12 = (r"^Equal\("  # Equal(MeasureOfAngle(AGC),Mul(MeasureOfAngle(HAD),2))
                 r"MeasureOfAngle\([A-Z]{3}\)"
                 r","
                 r"Mul\(MeasureOfAngle\([A-Z]{3}\),\s*[\d+\-*/a-z\s\(\)]+|\d+(\.\d+)?(?:\s*\w+\([\d+\-*/a-z\s\(\)]+\))*\)"
                 r"\)$")
    pattern13 = (r"^Equal\("  # Equal(Sub(AreaOfQuadrilateral(MHCD),AreaOfSector(OHM)),x)
                 r"Sub\([a-zA-Z]+\([A-Z,]+\),[a-zA-Z]+\([A-Z,]+\)\)"
                 r","
                 r"\s*[\d+\-*/a-z\s\(\)]+|\d+(\.\d+)?(?:\s*\w+\([\d+\-*/a-z\s\(\)]+\))*"
                 r"\)$")
    pattern14 = (r"^Equal\("  # Equal(Add(AreaOfQuadrilateral(MHCD),AreaOfSector(OHM)),x)
                 r"Add\([a-zA-Z]+\([A-Z,]+\),[a-zA-Z]+\([A-Z,]+\)\)"
                 r","
                 r"\s*[\d+\-*/a-z\s\(\)]+|\d+(\.\d+)?(?:\s*\w+\([\d+\-*/a-z\s\(\)]+\))*"
                 r"\)$")
    pattern15 = (r"^Equal\("  # Equal(Div(LengthOfLine(OM),LengthOfLine(OP)),4/5)
                 r"Div\(LengthOfLine\([A-Z]{2}\),LengthOfLine\([A-Z]{2}\)\)"
                 r","
                 r"\s*[\d+\-*/a-z\s\(\)]+|\d+(\.\d+)?(?:\s*\w+\([\d+\-*/a-z\s\(\)]+\))*"
                 r"\)$")
    pattern16 = (r"^Equal\("  # Equal(Tan(MeasureOfAngle(BAC)),1/2)
                 r"[a-zA-Z]+\(MeasureOfAngle\([A-Z]{3}\)\)"
                 r","
                 r"\s*[\d+\-*/a-z\s\(\)]+|\d+(\.\d+)?(?:\s*\w+\([\d+\-*/a-z\s\(\)]+\))*"
                 r"\)$")
    pattern17 = (r"^Equal\("  # Equal(Div(AreaOfTriangle(DEO),AreaOfTriangle(AOC)),1/9)
                 r"Div\([a-zA-Z]+\([A-Z,]+\),[a-zA-Z]+\([A-Z,]+\)\)"
                 r","
                 r"\s*[\d+\-*/a-z\s\(\)]+|\d+(\.\d+)?(?:\s*\w+\([\d+\-*/a-z\s\(\)]+\))*"
                 r"\)$")
    pattern18 = (r"Equal\("  # Equal(Div(LengthOfLine(IJ),LengthOfLine(YJ)),Div(LengthOfLine(HJ),LengthOfLine(XJ)))
                 r"Div\(LengthOfLine\([A-Z]{2}\),LengthOfLine\([A-Z]{2}\)\)"
                 r","
                 r"Div\(LengthOfLine\([A-Z]{2}\),LengthOfLine\([A-Z]{2}\)\)"
                 r"\)$")
    pattern19 = (r"^Equal\("  # Equal(LengthOfLine(AG),Mul(2,LengthOfLine(HA)))
                 r"LengthOfLine\([A-Z]{2}\)"
                 r","
                 r"Mul\(\s*[\d+\-*/a-z\s\(\)]+|\d+(\.\d+)?(?:\s*\w+\([\d+\-*/a-z\s\(\)]+\))*,LengthOfLine\([A-Z]{2}\)\)"
                 r"\)$")
    pattern20 = (r"^Equal\("  # Equal(MeasureOfAngle(AGC),Mul(2,MeasureOfAngle(HAD)))
                 r"MeasureOfAngle\([A-Z]{3}\)"
                 r","
                 r"Mul\(\s*[\d+\-*/a-z\s\(\)]+|\d+(\.\d+)?(?:\s*\w+\([\d+\-*/a-z\s\(\)]+\))*,MeasureOfAngle\([A-Z]{3}\)\)"
                 r"\)$")

    if re.match(pattern1, s):
        return "{}={}".format(s[19:21], s[36:38])
    elif re.match(pattern2, s):
        return "∠{}=∠{}".format(s[21:24], s[41:44])
    elif re.match(pattern3, s):
        return "⌒{}=⌒{}".format(s[19:22], s[37:40])
    elif re.match(pattern4, s):
        return "{}={}".format(s[19:21], s[23:len(s) - 1])
    elif re.match(pattern5, s):
        return "∠{}={}°".format(s[21:24], s[26:len(s) - 1])
    elif re.match(pattern6, s):
        return "∠{}={}°".format(s[19:22], s[24:len(s) - 1])
    elif re.match(pattern7, s):
        attrs = re.findall(r"[a-zA-Z]+\([A-Z,]+\)", s)
        attr1_name, attr1_para = parse_geo_predicate(attrs[0])
        attr2_name, attr2_para = parse_geo_predicate(attrs[1])
        if language == "cn":
            return "{}与{}相等".format(
                random.sample(gdl[attr1_name]["cn"], 1)[0].format(*attr1_para),
                random.sample(gdl[attr2_name]["cn"], 1)[0].format(*attr2_para)
            )
        else:
            return "{} is equal to {}".format(
                random.sample(gdl[attr1_name]["en"], 1)[0].format(*attr1_para),
                random.sample(gdl[attr2_name]["en"], 1)[0].format(*attr2_para)
            )
    elif re.match(pattern8, s):
        attr = re.findall(r"[a-zA-Z]+\([A-Z,]+\)", s)[0]
        attr_name, attr_para = parse_geo_predicate(attr)
        value = s[len(attr) + 7:len(s) - 1]
        if language == "cn":
            return "{}为{}".format(random.sample(gdl[attr_name]["cn"], 1)[0].format(*attr_para), value)
        else:
            return "{} is {}".format(random.sample(gdl[attr_name]["en"], 1)[0].format(*attr_para), value)
    elif re.match(pattern9, s):
        s = s[6:len(s) - 1].split(",")
        return "{}={}".format(s[0], s[1])
    elif re.match(pattern10, s):
        return "{}*{}={}*{}".format(s[23:25], s[40:42], s[62:64], s[79:81])
    elif re.match(pattern11, s):
        ratio = s.split(",")[2][:-2]
        return "{}={}{}".format(s[19:21], ratio, s[40:42])
    elif re.match(pattern12, s):
        ratio = s.split(",")[2][:-2]
        return "∠{}={}∠{}".format(s[21:24], ratio, s[45:48])
    elif re.match(pattern13, s):  # Equal(Sub(AreaOfQuadrilateral(MHCD),AreaOfSector(OHM)),x)
        attrs = re.findall(r"[a-zA-Z]+\([A-Z,]+\)", s)
        attr1_name, attr1_para = parse_geo_predicate(attrs[0])
        attr2_name, attr2_para = parse_geo_predicate(attrs[1])
        value = s[len(attrs[0]) + len(attrs[1]) + 13:len(s) - 1]
        if language == "cn":
            return "{}减去{}的差为{}".format(
                random.sample(gdl[attr1_name]["cn"], 1)[0].format(*attr1_para),
                random.sample(gdl[attr2_name]["cn"], 1)[0].format(*attr2_para),
                value
            )
        else:
            return "the difference between {} and {} is {}".format(
                random.sample(gdl[attr1_name]["en"], 1)[0].format(*attr1_para),
                random.sample(gdl[attr2_name]["en"], 1)[0].format(*attr2_para),
                value
            )
    elif re.match(pattern14, s):
        attrs = re.findall(r"[a-zA-Z]+\([A-Z,]+\)", s)
        attr1_name, attr1_para = parse_geo_predicate(attrs[0])
        attr2_name, attr2_para = parse_geo_predicate(attrs[1])
        value = s[len(attrs[0]) + len(attrs[1]) + 13:len(s) - 1]
        if language == "cn":
            return "{}与{}的和为{}".format(
                random.sample(gdl[attr1_name]["cn"], 1)[0].format(*attr1_para),
                random.sample(gdl[attr2_name]["cn"], 1)[0].format(*attr2_para),
                value
            )
        else:
            return "the sum of {} and {} is {}".format(
                random.sample(gdl[attr1_name]["en"], 1)[0].format(*attr1_para),
                random.sample(gdl[attr2_name]["en"], 1)[0].format(*attr2_para),
                value
            )
    elif re.match(pattern15, s):
        ratio = s.split(",")[2][:-1]
        return "{}/{}={}".format(s[23:25], s[40:42], ratio)
    elif re.match(pattern16, s):
        ratio = s.split(",")[1][:-1]
        return "{}({})={}".format(s[6:9], s[25:28], ratio)
    elif re.match(pattern17, s):  # Equal(Div(AreaOfTriangle(DEO),AreaOfTriangle(AOC)),1/9)
        attrs = re.findall(r"[a-zA-Z]+\([A-Z,]+\)", s)
        attr1_name, attr1_para = parse_geo_predicate(attrs[0])
        attr2_name, attr2_para = parse_geo_predicate(attrs[1])
        value = s[len(attrs[0]) + len(attrs[1]) + 13:len(s) - 1]
        if language == "cn":
            return "{}与{}之比为{}".format(
                random.sample(gdl[attr1_name]["cn"], 1)[0].format(*attr1_para),
                random.sample(gdl[attr2_name]["cn"], 1)[0].format(*attr2_para),
                value
            )
        else:
            return "the difference between {} and {} is {}".format(
                random.sample(gdl[attr1_name]["en"], 1)[0].format(*attr1_para),
                random.sample(gdl[attr2_name]["en"], 1)[0].format(*attr2_para),
                value
            )
    elif re.match(pattern18, s):
        return "{}/{}={}/{}".format(s[23:25], s[40:42], s[62:64], s[79:81])
    elif re.match(pattern19, s):
        ratio = s.split(",")[1][4:]
        return "{}={}{}".format(s[19:21], ratio, s.split(",")[2][13:15])
    elif re.match(pattern20, s):
        ratio = s.split(",")[1][4:]
        return "∠{}={}∠{}".format(s[21:24], ratio, s.split(",")[2][15:18])
    elif s in log["equal"][language]:
        return log["equal"][language][s]
    else:
        input_s = input("pid={}, type={}, language={}, s={}:".format(pid, "cdl", language, s))
        log["equal"][language][s] = input_s
        return input_s


def inverse_parse_target(s, language, gdl, log, pid):
    try:
        if s.startswith("Value"):
            s = s.replace("Value(", "")
            s = s[0:len(s) - 1]
            if s[0] in string.ascii_lowercase:
                if language == "cn":
                    return "求{}的值。".format(s)
                else:
                    return "Find the value of {}.".format(s)
            elif re.match(r"[a-zA-Z]+\([A-Z,]+\)", s):
                attr_name, attr_para = parse_geo_predicate(s)
                if language == "cn":
                    return "求{}。".format(random.sample(gdl[attr_name]["cn"], 1)[0].format(*attr_para))
                else:
                    return "Find {}.".format(random.sample(gdl[attr_name]["en"], 1)[0].format(*attr_para))
            elif re.match(r"[a-zA-Z]{3}\(MeasureOfAngle\([A-Z]{3}\)\)", s):
                if language == "cn":
                    return "求{}({})的值。".format(s[0:3].lower(), s[19:21])
                else:
                    return "Find the value of {}({}).".format(s[0:3].lower(), s[19:21])
            elif re.match(r"[a-zA-Z]{3}\([a-zA-Z]+\([A-Z,]+\)(,[a-zA-Z]+\([A-Z,]+\))+\)", s):
                anti_parsed_attrs = []
                for attr in re.findall(r"[a-zA-Z]+\([A-Z,]+\)", s):
                    attr_name, attr_para = parse_geo_predicate(attr)
                    anti_parsed_attrs.append(random.sample(gdl[attr_name][language], 1)[0].format(*attr_para))
                if s[0:3] == "Add":
                    if language == "cn":
                        return "求{}与{}之和。".format(
                            "、".join(anti_parsed_attrs[0:len(anti_parsed_attrs) - 1]),
                            anti_parsed_attrs[-1]
                        )
                    else:
                        return "Find the sum of {} and {}.".format(
                            ", ".join(anti_parsed_attrs[0:len(anti_parsed_attrs) - 1]),
                            anti_parsed_attrs[-1]
                        )
                elif s[0:3] == "Sub":
                    if language == "cn":
                        return "求{}减去{}。".format(*anti_parsed_attrs)
                    else:
                        return "Find {} minus {}.".format(*anti_parsed_attrs)
                elif s[0:3] == "Div":
                    if language == "cn":
                        return "求{}与{}之比。".format(*anti_parsed_attrs)
                    else:
                        return "Find the ratio of {} to {}.".format(*anti_parsed_attrs)
        elif s.startswith("Relation"):
            s = s.replace("Relation(", "")
            s = s[0:len(s) - 1]
            p_name, p_para = parse_geo_predicate(s)
            if language == "cn":
                return "求证{}。".format(random.sample(gdl[p_name][language], 1)[0].format(*p_para))
            else:
                return "Prove that {}.".format(random.sample(gdl[p_name][language], 1)[0].format(*p_para))

    except Exception as e:
        print("Exception: {}".format(repr(e)))

    if s in log["target"][language]:
        return log["target"][language][s]
    else:
        input_s = input("pid={}, type={}, language={}, s={}:".format(pid, "target", language, s))
        log["target"][language][s] = input_s
        return input_s


def inverse_parse(skip_special_fl):
    gdl = parse_raw_gdl(load_json("files/predicate_GDL-source.json"))
    log = load_json("inverse_parsed_problem/inverse_parse_log.json")

    for pid in range(1, 7001):
        problem = load_json(f"problems/{pid}.json")
        problem["text_cdl"] = sorted(list(set(problem["text_cdl"])))
        problem["image_cdl"] = sorted(list(set(problem["image_cdl"])))
        text_cn = []
        text_en = []
        try:
            for cdl in problem["text_cdl"]:
                if cdl.startswith("Equal"):
                    text_cn.append(inverse_parse_equal(cdl, "cn", gdl, log, pid))
                    text_en.append(inverse_parse_equal(cdl, "en", gdl, log, pid))
                else:
                    text_cn.append(inverse_parse_logic(cdl, "cn", gdl))
                    text_en.append(inverse_parse_logic(cdl, "en", gdl))
        except ParseError as e:
            print(e)
            if not skip_special_fl:
                break

        target_cn = inverse_parse_target(problem["goal_cdl"], "cn", gdl, log, pid)
        target_en = inverse_parse_target(problem["goal_cdl"], "en", gdl, log, pid)
        problem["problem_text_cn"] = "如图所示，" + "，".join(text_cn) + "。" + target_cn
        problem["problem_text_en"] = "As shown in the diagram, " + ", ".join(text_en) + ". " + target_en

        save_json(problem, f"inverse_parsed_problem/{pid}.json")
        safe_save_json(log, "inverse_parsed_problem/inverse_parse_log.json")
        print("{} ok.".format(pid))


def check_inverse_parse():
    check_words = ["Sub", "Add", "Mul", "Div"]
    for attr in load_json("gdl/predicate_GDL.json")["Attribution"]:
        check_words.append(attr.split("(")[0])

    for pid in range(1, 7001):
        text_cn = load_json(f"inverse_parsed_problem/{pid}.json")["problem_text_cn"]
        for word in check_words:
            if word in text_cn:
                print(pid)
                break


if __name__ == '__main__':
    working_directory = "../../../../projects/formalgeo7k-v2"
    os.chdir(working_directory)
    random.seed(619)

    if not os.path.exists("inverse_parsed_problem"):
        os.makedirs("inverse_parsed_problem")
        init_log = {
            "target": {"cn": {}, "en": {}},
            "equal": {"cn": {}, "en": {}},
            "parsed_pid": []
        }
        save_json(init_log, "inverse_parse_log.json")

    # inverse_parse(skip_special_fl=False)
    check_inverse_parse()
