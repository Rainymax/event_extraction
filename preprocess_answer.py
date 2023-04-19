# %%
import json
import os

# trigger data
def process_trigger_data(file):
    with open(f"./data/raw/{file}.json", encoding="utf-8")as f:
        lines = f.readlines()
    outlines = []
    for line in lines:
        trigger_dict = dict()
        line = line.strip()
        d = json.loads(line)
        text = d["text"]
        for label in d["labels"]:
            start = label["trigger"][1]
            end = start + len(label["trigger"][0])
            tmp_dict = dict(zip(range(start, end), ["B-EVENT"] + ["I-EVENT"] * (end-start-1)))
            # trigger_dict = dict(trigger_dict, **tmp_dict)
            trigger_dict.update(tmp_dict)
        for i in range(len(text)):
            outlines.append(" ".join([text[i], trigger_dict.get(i, "O")]))
        outlines.append("")
    if not os.path.exists("./data/processed/trigger"):
        os.makedirs("./data/processed/trigger", exist_ok=True)
    with open(f"./data/processed/trigger/{file}.txt", "w")as f:
        f.writelines("\n".join(outlines))
# %%
# argument data
def process_argument_data(file):
    with open(f"./data/raw/{file}.json", encoding="utf-8")as f:
        lines = f.readlines()
    outlines = []
    for line in lines:
        trigger_start = []
        trigger_end = []
        argument_dict = dict()
        line = line.strip()
        d = json.loads(line)
        id_ = d["id"]
        text = d["text"]
        for label in d["labels"]:
            trigger_start.append(label["trigger"][1])
            trigger_end.append(label["trigger"][1] + len(label["trigger"][0]))

            for k in label:
                if k == "trigger":
                    continue
                if label[k]:
                    start = label[k][1]
                    end = start + len(label[k][0])
                    tmp_dict = dict(zip(range(start, end), [f"B-{k}"] + [f"I-{k}"] * (end-start-1)))
                    argument_dict.update(tmp_dict)
        for i in range(len(text)):
            if i in trigger_start:
                outlines.append("<event> O")
            if i in trigger_end:
                outlines.append("<event/> O")
            outlines.append(" ".join([text[i], argument_dict.get(i, "O")]))
        outlines.append("")

    if not os.path.exists("./data/argument"):
        os.makedirs("./data/processed/argument", exist_ok=True)
    with open(f"./data/processed/argument/{file}.txt", "w")as f:
        f.writelines("\n".join(outlines))

def gen_labels(mode):
    path = f"./data/processed/{mode}/train.txt"
    labels = []
    with open(path)as f:
        lines = f.readlines()
    for line in lines:
        labels.append(line.strip().split(" ")[-1])
    labels = list(set(labels))
    if "" in labels:
        labels.remove("")
    with open(f"./data/processed/{mode}/labels.txt", "w")as f:
        f.writelines("\n".join(labels))
# %%
files = ["train", "dev"]
for f in files:
    process_argument_data(f)
    process_trigger_data(f)
gen_labels("trigger")
gen_labels("argument")

# %%
