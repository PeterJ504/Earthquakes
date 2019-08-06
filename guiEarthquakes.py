"""
Description: My first attempt at a GUI for the earthquake data

"""

# Imports
import webbrowser
from datetime import datetime, timedelta, timezone
from tkinter import Menu, StringVar, Tk, messagebox, ttk

import pytz
from tzlocal import get_localzone
from EarthquakeData import getDataFile, getWebData, loadHeaderInfo, loadList

urlData = "https://earthquake.usgs.gov/earthquakes/"\
    "feed/v1.0/summary/2.5_day.geojson"


class EarthquakeGUI:
    def _quit(self):
        # Quit program
        quit()  # win will exist when this function is called
        Tk.destroy(self)
        exit()

    def _refreshData(self):
        t1 = datetime.now()
        JSONdata = getWebData(urlData)
        t2 = datetime.now()
        tdweb = t2 - t1
        print("Web Retrieval - {}".format(tdweb.total_seconds()))
        if JSONdata:
            hList = loadHeaderInfo(JSONdata)
            eList = loadList(JSONdata)
            self.updateComboBoxData(eList)
            recNum = 0
            self.updateHeaderFields(hList)
            self.updateFields(eList, recNum)
        else:
            messagebox.showerror(
                "USGS File error",
                "Error retrieving "
                "data from USGS web site.  This normally"
                " occurs when the number of data lines"
                " has been exceeded.",
            )
            print("guiEarthquakeData - error getting file")

    def _comboCallbackFunc(self, event, data):
        # When combo box changes, updated data with new selection
        self.updateFields(data, self.summarySelected.current())

    def _webCallbackFunc(self, data):
        print(data)
        webbrowser.open_new(data)

    def getNewData(self, timeString):

        global urlData
        x = urlData.find("summary/")
        y = urlData.find(".geojson")
        # print(urlData[x+8:y])
        urlData = str(urlData.replace(urlData[x + 8: y], timeString, 1))
        # print(urlData)

        self._refreshData()
        # When combo box changes, updated data with new selection
        # self.updateFields(data, self.summarySelected.current())
        # return urlData

    def updateComboBoxData(self, data):
        dropdownlist = []
        self.summarySelected.delete(0)
        # print(self.summarySelected.width)
        if len(data) > 0:
            for n, i in enumerate(data):
                dropdownlist.append(str(data[n][1]*1.0) + "  -  " +
                                    str(data[n][2]))
            self.summarySelected["values"] = dropdownlist
            self.summarySelected.current(0)
            self.summarySelected.bind("<<ComboboxSelected>>", lambda event,
                                      arg=data: self._comboCallbackFunc(
                                          event, arg),)
        else:
            self.summarySelected["values"] = dropdownlist
            self.summarySelected.set("")

    def __init__(self, data, header):
        # test
        self.win = Tk()
        self.win.title("USGS Current Earthquake Data")  # Title

        # ----- Menu Bar - Create the Menu Bar -------------------------
        menuBar = Menu()
        self.win.config(menu=menuBar)
        fileMenu = Menu(menuBar, tearoff=False)
        dataMenu = Menu(menuBar, tearoff=False)
        helpMenu = Menu(menuBar, tearoff=False)
        menuBar.add_cascade(menu=fileMenu, label="File")
        menuBar.add_cascade(menu=dataMenu, label="Data")
        menuBar.add_cascade(menu=helpMenu, label="Help")
        # ----- Menu Bar - Create the File Menu ------------------------
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self._quit)
        # ----- Menu Bar - Create the Data Menu-------------------------
        dataMenu.add_command(label="Refresh current Data source",
                             command=self._refreshData)
        dataMenu.add_separator()
        dataSubMenu = Menu(dataMenu, tearoff=False)
        dataMenu.add_cascade(menu=dataSubMenu, label="New Data Source")
        # ----- Menu Bar - Create the Data submenu ---------------------
        d1 = [
            ["Significant", "significant"],
            ["Magnitude 4.5+", "4.5"],
            ["Magnitude 2.5+", "2.5"],
            ["Magnitude 1.0+", "1.0"],
            ["All Earthquakes+", "all"],
        ]
        d2 = [
            ["hour", "hour"],
            ["day", "day"],
            ["7 days", "week"],
            ["30 days", "month"],
        ]
        for i in range(len(d2)):
            for j in range(len(d1)):
                s1 = str(d1[j][0] + ", past " + d2[i][0])
                s2 = str(d1[j][1] + "_" + d2[i][1])
                dataSubMenu.add_command(
                    label=s1, command=lambda widget=s2:
                        self.getNewData(widget)
                )
                if j == (len(d1) - 1) and i != (len(d2) - 1):
                    dataSubMenu.add_separator()
        # ----- Set up frames and subframes to store widgets -----------
        self.mainFrame = ttk.LabelFrame()
        self.headings_frame = ttk.LabelFrame(self.mainFrame)
        self.headings_frame.grid(row=0)
        self.selection_frame = ttk.LabelFrame(
            self.headings_frame, text="selection frame"
        )
        self.selection_frame.configure(text=header["title"])
        self.selection_frame.grid(column=0, columnspan=2, row=0,
                                  sticky="NW")
        self.file_frame = ttk.LabelFrame(self.headings_frame,
                                         text="File Info")
        self.file_frame.grid(column=2, row=0, rowspan=3, sticky="NW")
        self.details_frame = ttk.LabelFrame(self.mainFrame)
        self.details_frame.grid(row=1)
        self.summary_frame = ttk.LabelFrame(self.details_frame,
                                            text="Event Details")
        self.summary_frame.grid(row=0, columnspan=2)
        self.location_frame = ttk.LabelFrame(self.details_frame,
                                             text="Event Location")
        self.location_frame.grid(row=1, column=0, sticky="NW")
        self.time_frame = ttk.LabelFrame(self.details_frame,
                                         text="Time of Event")
        self.time_frame.grid(row=1, column=1, sticky="NW")
        ttk.Label(self.selection_frame).grid(column=0, row=0,
                                             sticky="W")
        # ----- Set up combo box and data to populate it ---------------
        self.summarySelected = ttk.Combobox(
            self.selection_frame, width=85, state="readonly"
        )
        self.summarySelected.grid(column=0, row=1)
        self.updateComboBoxData(data)
        # ----- Add File widget - File delta ---------------------------
        self.fileDelta = StringVar()
        fileDeltaEntry = ttk.Label(
            self.file_frame, width=25, textvariable=self.fileDelta,
            state="readonly"
        )
        fileDeltaEntry.grid(column=1, row=0, columnspan=2, sticky="W")
        # ----- Add File widget - File Time ----------------------------
        ttk.Label(self.file_frame, text="File Time:").grid(
            column=0, row=1, sticky="E")
        self.fileTime = StringVar()
        fileTimeEntry = ttk.Label(
            self.file_frame, width=25, textvariable=self.fileTime,
            state="readonly"
        )
        fileTimeEntry.grid(column=1, row=1, sticky="W")
        # ----- Add File widget - Event count --------------------------
        ttk.Label(self.file_frame, text="Count:").grid(column=0, row=2,
                                                       sticky="E")
        self.fileCount = StringVar()
        fileCountEntry = ttk.Label(
            self.file_frame, width=25, textvariable=self.fileCount,
            state="readonly"
        )
        fileCountEntry.grid(column=1, row=2, sticky="W")
        # ----- Add Summary widget - Magnitude -------------------------
        ttk.Label(self.summary_frame, text="Magnitude:").grid(
            column=0, row=0, sticky="E"
        )
        self.mag = StringVar()
        magEntry = ttk.Label(
            self.summary_frame, width=7, textvariable=self.mag,
            state="readonly"
        )
        magEntry.grid(column=1, row=0, sticky="W")
        # ----- Add Summary widget - Alert -----------------------------
        ttk.Label(self.summary_frame, text="Alert:").grid(
            column=2, row=0, sticky="E")
        self.alert = StringVar()
        alertEntry = ttk.Label(
            self.summary_frame, width=7, textvariable=self.alert,
            state="readonly"
        )
        alertEntry.grid(column=3, row=0, sticky="W")
        # ----- Add Summary widget - Shake -----------------------------
        ttk.Label(self.summary_frame, text="Shake:").grid(
            column=4, row=0, sticky="E")
        self.shake = StringVar()
        shakeEntry = ttk.Label(
            self.summary_frame, width=7, textvariable=self.shake,
            state="readonly"
        )
        shakeEntry.grid(column=5, row=0, sticky="W")
        # ----- Add Summary widget - Report Felt -----------------------
        ttk.Label(self.summary_frame, text="Reported felt:").grid(
            column=6, row=0, sticky="E")
        self.felt = StringVar()
        feltEntry = ttk.Label(
            self.summary_frame, width=7, textvariable=self.felt,
            state="readonly"
        )
        feltEntry.grid(column=7, row=0, sticky="W")
        # ----- Add Summary widget - Url/More Info ---------------------
        ttk.Label(self.summary_frame, text="More info:").grid(
            column=0, row=1, sticky="E"
        )
        self.urlName = StringVar()
        self.urlEntry = ttk.Button(self.summary_frame)
        self.urlEntry.grid(column=2, row=1, columnspan=5, sticky="W")
        # ----- Add Location widget - Place ----------------------------
        ttk.Label(self.location_frame, text="Place:").grid(
            column=0, row=4, sticky="E")
        self.place = StringVar()
        locEntry = ttk.Label(
            self.location_frame, width=45, textvariable=self.place,
            state="readonly")
        locEntry.grid(column=1, row=4, sticky="W")
        # ----- Add Location widget - Latitude -------------------------
        ttk.Label(self.location_frame, text="Latitude:").grid(
            column=0, row=10, sticky="E")
        self.lat = StringVar()
        latEntry = ttk.Label(
            self.location_frame, width=25, textvariable=self.lat,
            state="readonly")
        latEntry.grid(column=1, row=10, sticky="W")
        # ----- Add Location widget - Longitude ------------------------
        ttk.Label(self.location_frame, text="Longitude:").grid(
            column=0, row=11, sticky="E")
        self.lon = StringVar()
        longEntry = ttk.Label(
            self.location_frame, width=25, textvariable=self.lon,
            state="readonly")
        longEntry.grid(column=1, row=11, sticky="W")
        # ----- Add Location widget - Depth ----------------------------
        ttk.Label(self.location_frame, text="Depth:").grid(
            column=0, row=12, sticky="E")
        self.depth = StringVar()
        depthEntry = ttk.Label(
            self.location_frame, width=25, textvariable=self.depth,
            state="readonly")
        depthEntry.grid(column=1, row=12, sticky="W")
        # ----- Add Time widget - Event delta --------------------------
        self.deltaEntry = StringVar()
        deltaEntry = ttk.Label(
            self.time_frame, width=25, textvariable=self.deltaEntry,
            state="readonly")
        deltaEntry.grid(column=1, row=0, sticky="W")
        # ----- Add Time widget - Event Time ---------------------------
        ttk.Label(self.time_frame, text="Time:").grid(
            column=0, row=1, sticky="E")
        self.time = StringVar()
        timeEntry = ttk.Label(
            self.time_frame, width=25, textvariable=self.time,
            state="readonly")
        timeEntry.grid(column=1, row=1, sticky="W")
        # ----- Add Time widget - Event Local Time ---------------------
        ttk.Label(self.time_frame, text="Your local time:").grid(
            column=0, row=2, sticky="E")
        self.tz = StringVar()
        tzEntry = ttk.Label(
            self.time_frame, width=25, textvariable=self.tz,
            state="readonly")
        tzEntry.grid(column=1, row=2, sticky="W")
        # ----- Add padding around fields
        self.mainFrame.grid_configure(padx=8, pady=4)
        for child in self.mainFrame.winfo_children():
            child.grid_configure(padx=8, pady=4)
            for grandChild in child.winfo_children():
                grandChild.grid_configure(padx=8, pady=4)
                for widget in grandChild.winfo_children():
                    widget.grid_configure(padx=8, pady=4)

        # ----- Call funtion to update fields --------------------------
        recNum = 0
        self.updateHeaderFields(header)
        self.updateFields(data, recNum)

    def updateHeaderFields(self, header):
        # Update header fields for the file
        self.selection_frame.configure(text=header["title"])
        self.fileCount.set(header["count"])
        utc_time = datetime.utcfromtimestamp(
            header["timeStamp"] / 1000).replace(tzinfo=pytz.utc)
        self.fileTime.set(utc_time.strftime("%Y-%m-%d %H:%M:%S %Z"))
        self.fileDelta.set(deltaTime(self, utc_time))

    def updateFields(self, data, rec):
        # print('Record {}'.format(rec))
        if len(data) > 0:
            # Update fields in the display from the data record
            self.mag.set(data[rec][1])
            self.place.set(data[rec][2])
            utc_time = datetime.utcfromtimestamp(
                data[rec][3] / 1000).replace(tzinfo=pytz.utc)
            self.time.set(utc_time.strftime("%Y-%m-%d %H:%M:%S %Z"))
            current_tz = utc_time.astimezone(get_localzone())
            self.tz.set(current_tz.strftime("%Y-%m-%d %H:%M:%S %Z"))
            self.urlName.set(data[rec][5])
            self.felt.set(data[rec][6])
            self.alert.set(data[rec][7])
            self.shake.set(data[rec][8])
            tmpLat = data[rec][10]
            if tmpLat == 0:
                self.lat.set("{} \xb0".format(tmpLat))
            elif tmpLat > 0:
                self.lat.set("{} \xb0 N".format(tmpLat))
            else:
                tmpLat *= -1
                self.lat.set("{} \xb0 S".format(tmpLat))
            tmpLong = data[rec][9]
            if tmpLong == 0:
                self.lon.set("{} \xb0".format(tmpLong))
            elif tmpLong > 0:
                self.lon.set("{} \xb0 E".format(tmpLong))
            else:
                tmpLong *= -1
                self.lon.set("{} \xb0 W".format(tmpLong))
            self.depth.set("{} km".format(data[rec][11]))
            # self.lon.set(data[rec][5])
            self.deltaEntry.set(deltaTime(self, utc_time))
        else:
            self.mag.set(None)
            self.place.set(None)
            self.time.set(None)
            self.tz.set(None)
            self.urlName.set(None)
            self.felt.set(None)
            self.alert.set(None)
            self.shake.set(None)
            self.lat.set(None)
            self.lon.set(None)
            self.depth.set(None)
            self.deltaEntry.set(None)
        self.urlEntry.config(
            text=self.urlName.get(),
            command=lambda arg=self.urlName.get():
                self._webCallbackFunc(arg)
        )


def deltaTime(self, timeCheck):
    # Tells how long a date is from now (rounded to minutes, hours
    # or days)
    utc_now = datetime.now(timezone.utc)
    delta = utc_now - timeCheck
    hours = delta.total_seconds() / 3600
    minutes = delta.total_seconds() / 60
    if hours > 48:
        days = hours / 24
        return str("about " + "{:.0f}".format(days) + " days ago")
    elif hours >= 2:
        return str("about " + "{:.0f}".format(hours) + " hours ago")
    elif delta.total_seconds() > 90:
        return str("about " + "{:.0f}".format(minutes) + " minutes ago")
    else:
        return str("about a minute ago")


def main():

    # root = Tk()

    # Get data from file.  If the does not exist then go to the
    # web to update it.
    JSONdata = getDataFile()
    if not JSONdata:
        JSONdata = getWebData(urlData)
        if not JSONdata:
            print("error getting file")
    hList = loadHeaderInfo(JSONdata)
    eList = loadList(JSONdata)
    root = EarthquakeGUI(eList, hList)
    root.win.mainloop()


if __name__ == "__main__":
    main()
