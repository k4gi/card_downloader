import requests
import time
import json
import os


# We kindly ask that you insert 50 – 100 milliseconds of delay between the requests you send to the server at api.scryfall.com. (i.e., 10 requests per second on average).


def search_paging(counter, set_name, search):
	for each_card in search["data"]:
		# The file origins used by the API, located at *.scryfall.io do not have these rate limits.

		print("Card", each_card["collector_number"], each_card["name"], "(", counter, ")")
		counter = counter + 1

		new_filename = set_name+"/"+each_card["collector_number"]+" "+each_card["name"]+".png"

		if os.path.exists(new_filename):
			print(new_filename, "file already exists")
			continue

		image_response = requests.get(each_card["image_uris"]["png"], headers=head)

		print("Image Response", image_response.status_code)

		new_file = open(new_filename, "xb")
		new_file.write(image_response.content)

	if search["has_more"]:
		print("Requesting next search page...")
		search_response = requests.get(search["next_page"], headers=head)

		print("Search Response", search_response.status_code)

		search_json = json.loads(search_response.text)

		search_paging(counter, set_name, search_json)




head = {
	"User-Agent": "KagiMagicCardDownloader/0.1",
	"Accept": "*/*",
}

set_response = requests.get("https://api.scryfall.com/sets/ced", headers=head)

print("Set Response", set_response.status_code)

json_set = json.loads(set_response.text)

print("Set Name:", json_set["name"])

try:
	os.mkdir(json_set["name"])
	print(json_set["name"], "folder created")
except FileExistsError:
	print(json_set["name"], "folder already exists")
except PermissionError:
	print(json_set["name"], "folder creation permission denied")
except Exception as e:
	print(json_set["name"], "folder error:", e)


time.sleep(0.1)

search_response = requests.get(json_set["search_uri"], headers=head)

print("Search Response", search_response.status_code)

json_search = json.loads(search_response.text)

i = 1

search_paging(i, json_set["name"], json_search)


