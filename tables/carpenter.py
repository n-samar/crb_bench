from pathlib import Path
import os

def process_all(folder: Path):
    pathlist = folder.glob("**/tbl_*.tex")
    for template_file in pathlist:
        process_file(template_file)

def dict_string(data_dict):
    result = ""
    for key, value in data_dict.items():
        result += "\\newcommand{\\" + str(key) + "}{" + str(value) + "}\n"
    return result


def process_file(template_file: Path):
    print(f"Processing {template_file}")
    parent_dir = template_file.parents[0]

    # blah.carpenter -> ag_blah.carpenter_dict
    data_file = parent_dir / ("ag_" + template_file.stem + ".carpenter_dict")

    # blah.carpenter -> ag_blah.py
    preprocessor = parent_dir / (template_file.stem + ".py")
    os.system(f"python3 {preprocessor} > {data_file}")

    data_dict = eval(data_file.read_text())
    # blah.carpenter -> ag_blah.tex
    ag_filepath = parent_dir / ("ag_" + template_file.stem + ".tex")
    result = "{\n" + dict_string(data_dict) + template_file.read_text() + "\n}\n"
    with ag_filepath.open("w", encoding="utf-8") as f:
        f.write(result)

if __name__ == "__main__":
    process_all(Path("./"))
