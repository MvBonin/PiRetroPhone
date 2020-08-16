import json
class Settings:
    def __init__(self):
        self.fileName = "saves.json"
        self.loadData()


    def loadData(self):
        with open(self.fileName, "r") as json_data_file:
            self.data = json.load(json_data_file)
        print("Data Loaded from %s" % self.fileName)
        print(self.data)

    def writeData(self):
        with open(self.fileName, 'w') as outfile:
            json.dump(self.data, outfile)
        print("Saved Data")

    def getContact(self, nr):
        print("get contact")
        if int(nr) >= 0 and int(nr) < 10:
            return self.data["contacts"][str(nr)]

    def setContact(self, nr, contactNr):
        if int(nr) >= 0 and int(nr) < 10 and contactNr != "":
            self.data["contacts"][str(nr)] = str(contactNr)
            ##print("Now writing:")
            self.writeData()
    def setAlarm(self, timeStr):
        ##got 4 or 3 character time String.
        print("Alarmset fnctn")
        if len(timeStr) == 3 and int(timeStr[:2]) < 61:
            print("Valid timestring")
            self.data["alarm"] = timeStr
        if len(timeStr) == 4:
            if int(timeStr[2:]) < 25 and int(timeStr[:2]) < 61:
                print("Valid timestring")
                self.data["alarm"] = timeStr
        self.writeData()

    def isAlarmSet(self):
        if self.data["alarm"] != "....":
            return True
        else:
            return False

    def deleteAlarm(self):
        self.data["alarm"] = "...."
        self.writeData()

    def getRingtone(self):
        return self.data["ringtone"]
    
    def setRingtone(self, ring):
        self.data["ringtone"] = str(ring)
        self.writeData