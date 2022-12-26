import requests
from bs4 import BeautifulSoup
import json
import os
import eyed3
import time

source = None

while not source:
    try:
        filename = input("File path:").replace("\"","")
        file = open(filename, encoding='utf-8')
        source = json.load(file)
        file.close()
    except:
        if filename == "exit()":
            exit()
        print("Please input the path to a JSON file.")

dir = filename[0:-5] + " downloads"
dirs = input("Download folder (default: " + dir + "\) : " if os.name == "nt" else "/) : ").replace("\"","")
dir = dirs if dirs.strip() != "" else dir

print()

ann = None
anime = None
if not os.path.exists(dir):
    os.mkdir(dir)
ins = 1
progress = 0

for L in source:
    url = L['urls']['catbox']['0']
    if ann != str(L['annId']):
        print("Fetching next ANN entry")
        ann = str(L['annId'])
        r = requests.get("https://www.animenewsnetwork.com/encyclopedia/anime.php?id=" + ann)
        soup = BeautifulSoup(r.content, 'html.parser')
        anime = soup.select_one('#page_header').text.strip()
        print("Fetched " + anime)
        ins = 1

    print("Downloading " + L['name'] + " from catbox.moe")
    response = requests.get(url)
    if L['type'][0] == "I":
        type = "Insert " + str(ins)
        ins+=1
    else:
        type = L['type']
    print("Complete")

    print("Writing on file")
    name = anime + " - " + type + " (" + L['name'] + " by " + L['artist'] + ")"
    namefile = ""
    for i in range(len(name)):
        if name[i] not in ["/", "\\", "*", "|", ":", "?", "\"", "<", ">"]:
            namefile += name[i]
    namefile = dir + "\\" + namefile + ".mp3"
    open(namefile, "wb").write(response.content)
    print("Written")

    print('Adding metadata')
    audiofile = eyed3.load(namefile)
    if not audiofile.tag:
        audiofile.initTag()

    audiofile.tag.artist = L['artist']
    audiofile.tag.title = L['name'] + " (" + anime + " - " + type + ")"
    audiofile.tag.save()
    print("Added")
    progress+=1
    print("{0} complete, to next song! {1}/{2} ({3}%)\n".format(name, progress, len(source), round(progress/len(source)*100), 2))


input("Done! Press Enter to exit.")
