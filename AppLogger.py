from datetime import datetime


class Logger:
    """
                               Method Name: Logger
                               Description: Creates a log file and write the logs in to the file
                               Output:log file
                               On Failure: Raise Exception


    """
    def __init__(self):
        pass

    def log(self, file_object, log_message):
        self.now = datetime.now()
        self.date = self.now.date()
        self.file_object = file_object
        self.current_time = self.now.strftime("%H:%M:%S")
        file_object.write(
            str(self.date) + "/" + str(self.current_time) + "\t\t" + log_message +"\n")






