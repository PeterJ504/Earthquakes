import json
import pandas as pd
import numpy as np
import urllib.request



class EarthquakeData():
    """ Used to gather and manipulate the data from the USGS web site. """

    def __init__():
        pass

    def getDataFile():
        # get data from a stored file.  When multiple requests are made, it
        # saves going to the web each time.
        # output: a JSON file. If the file does not exist it returns None.
        try:
            with open("earthquake.json", 'r') as f:
                data = f.read()
        except FileNotFoundError:
            return None
        except:
            print("File error")
            return None
        return json.loads(data)

    def getWebData(urlData):
        print(urlData)
        # get data from the web and write to a file if successful
        try:
            webUrl = urllib.request.urlopen(urlData)
        except urllib.error.URLError as e:
            # print(e.code, e.reason)
            msg = "\nError from website - " + str(e.code) + " - " + str(e.reason) + " from\n" + urlData
            if e.code == 400:
                msg = msg + "\nThis error usually occurs when file is too big."
            msg=msg + "\nFor more information, paste the url into your web browser.\n\n"
                   
            print(msg)
            return None
        if (webUrl.getcode() == 200):
            data = webUrl.read()
            try:
                theJSON = json.loads(data)
                # write json data to a file
                with open("earthquake.json", "w") as f:
                    json.dump(theJSON, f)
                f.close()
                return theJSON
            except:
                # TODO: Need better error handling
                print("File error from server, cannot retrieve results from page  - " +
                      str(urlData))
                return None
        else:
            print("Received an error from server, cannot retrieve results " +
                  str(webUrl.getcode()))
            return None

    def loadDict(JSONData):
        eDict = {}
        row = 0
        for i in JSONData["features"]:
            eDict[row] = {}
            eDict[row]["_idName"] = i["id"]
            eDict[row]["mag"] = i["properties"]["mag"]
            eDict[row]["place"] = i["properties"]["place"]
            eDict[row]["time"] = i["properties"]["time"]
            eDict[row]["tz"] = i["properties"]["tz"]
            eDict[row]["urlName"] = i["properties"]["url"]
            eDict[row]["felt"] = i["properties"]["felt"]
            eDict[row]["alert"] = i["properties"]["alert"]
            eDict[row]["shakeMap"] = i["properties"]["mmi"]
            eDict[row]["lon"] = i["geometry"]["coordinates"][0]
            eDict[row]["lat"] = i["geometry"]["coordinates"][1]
            eDict[row]["depth"] = i["geometry"]["coordinates"][2]
            row += 1

        list = pd.DataFrame.from_records(eDict).T
        try:
            list.sort_values(by=['mag', 'alert'], inplace=True,
                             ascending=[False, True])
        except:
            print("list is empty")
        list.reset_index(drop=True, inplace=True)

        # retList = [list.columns.values.tolist()] + list.values.tolist()
        return list.values.tolist()

    def loadHeaderInfo(JSONData):
        headerInfo = {}
        headerInfo["timeStamp"] = JSONData["metadata"]["generated"]
        headerInfo["url"] = JSONData["metadata"]["url"]
        headerInfo["title"] = JSONData["metadata"]["title"]
        headerInfo["count"] = JSONData["metadata"]["count"]

        return headerInfo

# ----------- For testing purposes only ------------------------------


def getNewData(self, timeString):

    global urlData
    # print(urlData)
    x = urlData.find('summary/')
    y = urlData.find('.geojson')
    # print(urlData[x+8:y])
    urlData = str(urlData.replace(urlData[x+8:y], timeString, 1))
    print(urlData)


def main():

    urlData = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
    print(EarthquakeData.getWebData(urlData))

    # JSONdata = EarthquakeData.getDataFile()
    # # eList = EarthquakeData.loadDict(JSONdata)
    # hList = EarthquakeData.loadHeaderInfo(JSONdata)
    # print(hList)
    # print(hList["title"])


# --------------------------------------------------------------------
if __name__ == "__main__":
    main()
