import requests

api_key = "rGjc2LP1AWXkyfHCdJjy"
data = "MSFT"

url = "https://www.quandl.com/api/v3/datasets/EOD/%s.json?api_key=%s" % (data, api_key)

# Download the data
r = requests.get(url)
if r.status_code == 200:
    data_json = r.json()
    print("Download good")
else:
    print("Download failed")
