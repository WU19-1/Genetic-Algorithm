from threading import Thread, Event, current_thread
import requests
import time


class StressTest:

    def __init__(self, stress_test_object):
        self.url = stress_test_object["url"]
        self.connection = stress_test_object["connection"]
        self.output = stress_test_object["output"]
        self.request = stress_test_object["request"]
        self.timeout = stress_test_object["timeout"]

        self.event = Event()
        self.thread_list = []

        self.total_time = 0

    def send_request(self):
        for _ in range(self.request):
            try:
                start_time = round(time.time() * 1000.0)

                respond = requests.get(self.url, timeout=self.timeout)
                respond.close()

                end_time = round(time.time() * 1000.0)

                self.total_time += (end_time - start_time)
            except Exception:
                print("[!] Failed request to {}.".format(self.url))

        self.thread_list.remove(current_thread())

    def check_thread(self):
        try:
            while self.thread_list[0]:
                pass
        except Exception:
            self.event.set()

    def stress_test(self):
        for _ in range(self.connection):
            thread = Thread(target=self.send_request)
            thread.setDaemon(True)
            thread.start()
            self.thread_list.append(thread)

        checker_thread = Thread(target=self.check_thread)
        checker_thread.start()

        self.event.wait()

        return self.total_time / (self.request * self.connection)
