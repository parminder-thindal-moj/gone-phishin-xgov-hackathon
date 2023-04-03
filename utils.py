#### Set the Template ID for Spam Msgs on GOV.UK Notify
SPAM_MSG_ID = "ed5edbf5-76e0-42be-9c06-3b3717ce00ad"
NOT_SPAM_MSG_ID = "5e107ed8-c631-492f-ad7d-91c73919a42e"

### Set the SPAM Threshold
SPAM_THRESHOLD = 0.75

### API reload interval
TIME_INTERVAL_SECS = 1

import sys
import time
import threading

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False