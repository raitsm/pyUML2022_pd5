import sys
class WorldHistory:
    # takes a list of dimensions (the objects that will be accounted for) as input
    # Example ["Bears","Fish"]
    def __init__(self, headers : list) -> None:
        self.__history = {}
        for k in headers:
            self.__history[k.upper()] = []
    
    # adds a history record for an object specified
    def addHistoryItem(self, object_name: str, value) -> None:
        if object_name.upper() in self.__history:
            self.__history[object_name.upper()].append(value)

    # exports history to a file specified. CSV format will be used for output.
    # NB, it is important that all objects have same number of history records
    #
    def exportHistory(self, file_name="world_history.csv") -> None:
        f_out = open(file_name,"w")
        # f_out = sys.stdout
        tmp = "TIME"+","
        for k in self.__history:
            tmp = tmp + k + ","
        print(tmp[:-1],file=f_out)
        for i in range(0, len(self.__history[list(self.__history)[0]])):
            tmp = str(i)+","
            for k in self.__history:
                tmp = tmp + str(self.__history[k][i]) + ","
            print(tmp[:-1],file=f_out)
        f_out.close()
    
    

if __name__ == "__main__":
    wh = WorldHistory(["header1", "header2"])
    wh.addHistoryItem("header1", 123)
    wh.addHistoryItem("header2", 145)
    wh.addHistoryItem("header1", 223)
    wh.addHistoryItem("header2", 245)

    # wh.printHistory()
    wh.exportHistory()
    