# terminal code: "cd Remnote2Obsidian && python Remnote2Obsidian.py"

import sys, os, json

# user-input variables: ----------------------------------------
jsonPath = "rem.json"
# jsonPath = sys.argv[1]
# homepageName = "Personal"
homepageID = "pAbgiAqZ45tLDzSpS" # you can find this in the URL (eg: https://www.remnote.io/document/HrxrQbMC3fXbBpWPB)
folderName = "Rem2Obs"
# ---------------------------------------------------------------

dir_path = os.path.dirname(os.path.realpath(__file__))
Rem2ObsPath = os.path.join(dir_path, folderName)
os.makedirs(Rem2ObsPath, exist_ok=True)

j = json.load(open(jsonPath, mode="rt", encoding="utf-8", errors="ignore"))
RemnoteDocs = j["docs"]

def expandChildren(pages, ID):
    childID = [x["children"] for x in pages if x["_id"] == ID][0]
    # print([[x["key"], x["_id"]] for x in RemnoteDocs if x["key"] == [homepageName]])
    mainPages = [x for x in RemnoteDocs if x["_id"] in childID]
    # Rem with "contains:" in key are auto-generated. So those will be removed
    filteredChildren = []
    for x in mainPages:
         if not x["key"] == [] and not "contains:" in x["key"] and not "rcrp" in x:
            if "type" in x and x["type"] == 6:
                 pass
            else:
                filteredChildren.append(x)
            

    return filteredChildren


filteredPages = expandChildren(RemnoteDocs, homepageID)

for file in filteredPages:
    # print(file["key"][0])
    filename = os.path.join(Rem2ObsPath, file["key"][0] + ".md")

    child = expandChildren(RemnoteDocs, file["_id"])
    bullets = []
    for x in child:
        print({file["_id"], file["key"][0], x["_id"], str(x["key"])})

        if (len(x["key"])>1):
            text = x["key"][0]["text"]
        else:
            text = x["key"][0]
        bullets.append("* " + str(text) + "\n")
    with open(filename, mode="wt", encoding="utf-8") as f:
        f.write("# " + file["key"][0] + "\n" + str(str(bullets)))

print(str(len(filteredPages)) + " files generated")
