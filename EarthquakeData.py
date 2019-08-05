import json
import urllib.request


class EarthquakeData:
    """ Used to gather and manipulate the data from the USGS web site. """

    def getDataFile():
        # get data from a stored file.  When multiple requests are made, it
        # saves going to the web each time.
        # output: a JSON file. If the file does not exist it returns None.
        try:
            with open("earthquake.json", "r") as f:
                data = f.read()
        except FileNotFoundError:
            return None
        except:
            print("File error")
            return None
        return json.loads(data)

    def getWebData(urlData):
        # print(urlData)
        # get data from the web and write to a file if successful
        try:
            webUrl = urllib.request.urlopen(urlData)
        except urllib.error.URLError as e:
            msg = (
                "\nError from website - " + str(e.code) + " - " +
                str(e.reason) + " from\n" + urlData)
            if e.code == 400:
                msg = msg + "\nThis error usually occurs when file is too big."
            msg = (
                msg + "\nFor more information, paste the url into your "
                "web browser.\n\n"
            )
            print(msg)
            return None
        if webUrl.getcode() == 200:
            data = webUrl.read()
            try:
                theJSON = json.loads(data)
                # write json data to a file
                with open("earthquake.json", "w") as f:
                    json.dump(theJSON, f)
                return theJSON
            except:
                # TODO: Need better error handling
                print(
                    "File error from server, cannot retrieve results "
                    "from page  - " + str(urlData)
                )
                return None
        else:
            print(
                "Received an error from server, cannot retrieve results "
                + str(webUrl.getcode())
            )
            return None

    def loadList(JSONData):
        # Added some error checking because the occasional data problem
        # causes an abort when sorting different data types
        eList = []
        # testList = []
        for i in JSONData["features"]:
            if not i["properties"]["mag"]:
                i["properties"]["mag"] = 0.0
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
            # testList.append(type(i["properties"]["alert"]))
        try:
            s_eList = sorted(eList, key=lambda x: (x[1], x[7]), reverse=True)
            return s_eList
        except:
            print("Error sorting list - most likely bad data")
            # output = set()
            # for x in testList:
            #     output.add(x)
            # print(output)
        return eList

    def loadHeaderInfo(JSONData):
        headerInfo = {}
        headerInfo["timeStamp"] = JSONData["metadata"]["generated"]
        headerInfo["url"] = JSONData["metadata"]["url"]
        headerInfo["title"] = JSONData["metadata"]["title"]
        headerInfo["count"] = JSONData["metadata"]["count"]

        return headerInfo


# ----------- For testing purposes only ------------------------------


# def getNewData(self, timeString):

#     global urlData
#     # print(urlData)
#     x = urlData.find('summary/')
#     y = urlData.find('.geojson')
#     # print(urlData[x+8:y])
#     urlData = str(urlData.replace(urlData[x+8:y], timeString, 1))
#     # print(urlData)


def main():

    urlData = (
        "https://earthquake.usgs.gov/earthquakes/feed/v1.0/"
        "summary/2.5_day.geojson"
    )

    print(EarthquakeData.getWebData(urlData))

    JSONdata = EarthquakeData.getDataFile()
    eList = EarthquakeData.loadList(JSONdata)
    # print(eList)

    # # eList = EarthquakeDaList(JSONdata)
    # hList = EarthquakeData.loadHeaderInfo(JSONdata)
    # print(hList)
    # print(hList["title"])


# --------------------------------------------------------------------
if __name__ == "__main__":
    main()
