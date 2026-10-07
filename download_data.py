import os
import urllib.request

os.makedirs("data", exist_ok=True)
base = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/"

for name in ["KDDTrain+", "KDDTest+"]:
    saved = False
    for ext in [".txt", ".csv"]:
        url = base + name.replace("+", "%2B") + ext
        try:
            urllib.request.urlretrieve(url, f"data/{name}.txt")
            print("Downloaded", name, "from", url)
            saved = True
            break
        except Exception as e:
            print("Failed:", url, e)
    if not saved:
        print("Could not download", name)