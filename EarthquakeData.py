import json
import urllib.request

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)5s:%(lineno)4s:%(filename)20s:'
    '%(funcName)20s:%(message)s', datefmt='%Y%m%d %H:%M:%S',)


JSONFile = 'earthquake.json'


def getDataFile():
    # get data from a stored file.  When multiple requests are made, it
    # saves going to the web each time.
    # output: a JSON file. If the file does not exist it returns None.
    logging.debug(f"")
    try:
        with open(JSONFile, "r") as f:
            data = f.read()
    except FileNotFoundError:
        return None
    except OSError:
        logging.error(
            f"\nError reading file - {JSONFile}.")
        return None
    return json.loads(data)


def getWebData(urlData):
    logging.debug(
        f"\nReading url - {urlData}.")
    # get data from the web and write to a file if successful
    try:
        webUrl = urllib.request.urlopen(urlData)
    except urllib.error.URLError as e:
        logging.error(f"URL access error - {e.reason}")
        return None
    if webUrl.getcode() == 200:
        data = webUrl.read()
        try:
            theJSON = json.loads(data)
            # write json data to a file
            with open(JSONFile, "w") as f:
                json.dump(theJSON, f)
            return theJSON
        except:
            logging.error(
                f"\nUnknown error from website \n{urlData}")
            return None
    else:
        logging.error(
            f"\nError from website - code: {webUrl.getcode()}\n{urlData}")
        return None


def loadList(JSONData):
    # Added some error checking because the occasional data problem
    # causes an abort when sorting different data types
    logging.debug(f"")
    eList = []
    # testList = []
    for i in JSONData["features"]:
        if not i["properties"]["mag"]:
            i["properties"]["mag"] = 0.0
        if not i["properties"]["mmi"]:
            i["properties"]["mmi"] = 0.0
        if not i["properties"]["alert"]:
            i["properties"]["alert"] = ""
        eList.append(
            [
                i["id"],
                i["properties"]["mag"],
                i["properties"]["place"],
                i["properties"]["time"],
                i["properties"]["tz"],
                i["properties"]["url"],
                i["properties"]["felt"],
                i["properties"]["alert"],
                i["properties"]["mmi"],
                i["geometry"]["coordinates"][0],
                i["geometry"]["coordinates"][1],
                i["geometry"]["coordinates"][2],
            ]
        )
    return eList


def loadHeaderInfo(JSONData):
    logging.debug(f"")
    return {
        "timeStamp": JSONData["metadata"]["generated"],
        "url": JSONData["metadata"]["url"],
        "title": JSONData["metadata"]["title"],
        "count": JSONData["metadata"]["count"]
    }


# ----------- For testing purposes only --------------------------------


def main():

    urlData = (
        "https://earthquake.usgs.gov/earthquakes/feed/v1.0/"
        "summary/2.5_day.geojson"
    )

    output = getWebData(urlData)
    logging.debug(output)

    # JSONdata = getDataFile()
    # if JSONdata:
    #     eList = loadList(JSONdata)
    #     print(eList)

    # # eList = EarthquakeDaList(JSONdata)
    # hList = loadHeaderInfo(JSONdata)
    # print(hList)
    # print(hList["title"])


# --------------------------------------------------------------------
if __name__ == "__main__":
    main()
