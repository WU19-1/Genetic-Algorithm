from threading import Thread, Event, current_thread
from datetime import datetime
from tabulate import tabulate
import argparse
import requests
import time

arguments = {
    "URL": "",
    "connection": 10,
    "output": "result.txt",
    "request": 128,
    "timeout": 10,
}

result = {
    "time_list": {},
    "status_code_list": {},
    "total_time": 0
}

log = {
    "total_error": 0,
    "error_list": []
}

event = Event()
thread_list = []


def read_arguments():
    global arguments

    parser = argparse.ArgumentParser()
    parser.add_argument("URL",
                        help="URL is any valid http or https url.")
    parser.add_argument("-c", "--connection",
                        help="the number of concurrent connections to use. default: 10.")
    parser.add_argument("-o", "--output",
                        help="the output file name. default: result.txt")
    parser.add_argument("-r", "--request",
                        help="the amount of requests to make per connection. default: 128")
    parser.add_argument("-t", "--timeout",
                        help="the number of seconds before timing out and resetting a connection. default: 10")
    args = parser.parse_args()

    arguments["URL"] = args.URL
    if args.connection:
        arguments["connection"] = int(args.connection)
    if args.output:
        arguments["output"] = args.output
    if args.request:
        arguments["request"] = int(args.request)
    if args.timeout:
        arguments["timeout"] = int(args.timeout)


def file_handler(file_name, string):
    file = open(file_name, "a")
    file.write(string)


def send_request(url, request, timeout):
    global result, log, thread_list

    for _ in range(request):
        try:
            start_time = round(time.time() * 1000.0)

            # respond = requests.get(url, timeout=timeout, headers={"connection": "close"})  # close connection
            respond = requests.get(url, timeout=timeout)  # open connection
            respond.close()

            end_time = round(time.time() * 1000.0)

            try:
                result["time_list"][str(end_time - start_time) + " ms"] += 1
            except Exception:
                result["time_list"][str(end_time - start_time) + " ms"] = 1

            try:
                result["status_code_list"][str(respond.status_code)] += 1
            except Exception:
                result["status_code_list"][str(respond.status_code)] = 1

            result["total_time"] += (end_time - start_time)

        except Exception as e:
            log["error_list"].append(e)
            log["total_error"] += 1

    thread_list.remove(current_thread())

def check_thread():
    try:
        while thread_list[0]:
            pass
    except Exception:
        event.set()

def run(url: str, request: int, connection: int, timeout: int=10) -> float:
    global result, thread_list, event

    result = {
        "time_list": {},
        "status_code_list": {},
        "total_time": 0
    }
    event = Event()
    thread_list = []

    for _ in range(connection):
        thread = Thread(target=send_request, args=(url, request, timeout))
        thread.setDaemon(True)
        thread.start()
        thread_list.append(thread)

    checker_thread = Thread(target=check_thread)
    checker_thread.start()

    event.wait()

    result["time_list"] = sorted(result["time_list"].items(), key=lambda item: int(item[0].split(" ")[0]))
    result["status_code_list"] = sorted(result["status_code_list"].items(), key=lambda item: int(item[0]))

    time_average : float = result["total_time"] / (arguments["request"] * arguments["connection"])
    return time_average

if __name__ == "__main__":
    read_arguments()
    start_time = datetime.now()

    for _ in range(arguments["connection"]):
        thread = Thread(target=send_request, args=(arguments["URL"], arguments["request"], arguments["timeout"]))
        thread.setDaemon(True)
        thread.start()
        thread_list.append(thread)

    checker_thread = Thread(target=check_thread)
    checker_thread.start()

    event.wait()

    result["time_list"] = sorted(result["time_list"].items(), key=lambda item: int(item[0].split(" ")[0]))
    result["status_code_list"] = sorted(result["status_code_list"].items(), key=lambda item: int(item[0]))

    end_time = datetime.now()
    time_average : int = result["total_time"] / (arguments["request"] * arguments["connection"])
    print(time_average)
    # result_write = "{}".format(result["total_time"] / (arguments["request"] * arguments["connection"]))
#     result_summary_write = """
# =========================================================================
# StressTest version 1.0 by RX, WU, and WT.

# Started at {start_time}.
# Finished at {end_time}.

# StressTest for {url} with a total of {connection} connections ({request} request/connection, timeout: {timeout} s).

# Average Response Time: {time_average} ms

# Status Code List:
# {status_code_list}
# =========================================================================
#     """.format(
#         start_time=start_time,
#         end_time=end_time,
#         url=arguments["URL"],
#         connection=arguments["connection"],
#         request=arguments["request"],
#         timeout=arguments["timeout"],
#         time_average=result["total_time"] / (arguments["request"] * arguments["connection"]),
#         status_code_list=tabulate(result["status_code_list"], headers=["Status Code", "Total Request"],
#                                   tablefmt="pretty"))

#     file_handler("result.res", result_write)
#     file_handler(arguments["output"], result_summary_write)
    
