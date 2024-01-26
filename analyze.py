from collections import Counter
import re
import os
import json
from tqdm import tqdm

# helper to find all the JSON data files ... probably an easier way to do this with a library
def find_json_files(directory):
    json_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files


if __name__ == "__main__":
    target_folder = os.getcwd()
    json_files = find_json_files(target_folder)
    all_refs = Counter()

    for json_file in tqdm(json_files):
        with open(json_file, "r") as file:
            try:
                data = json.load(file)
                # load the references for each file
                ref_docs = data["ref_docs"]
                doc_strs = []
                for ref in ref_docs:
                    doi = str(ref["doi"])
                    title = ref["title"] or ref["sourcetitle"]
                    refid = str(ref["id"])
                    doc_strs.append(f"{doi}\t{title}\t{refid}")

                # add each reference to a running counter
                all_refs.update(doc_strs)

            except json.JSONDecodeError as e:
                print(f"Error reading {json_file}: {e}")

    top_items = all_refs.most_common(100)

    for item, count in top_items:
        print(f"{item}\t{count}")
