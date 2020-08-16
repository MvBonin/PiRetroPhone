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