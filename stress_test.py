from threading import Thread, Event, current_thread
import requests
import time

arguments = {
    "URL": "",
    "connection": 20,
    "output": "result.txt",
    "request": 64,
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

def send_request(url, request, timeout):
    global result, log, thread_list

    for _ in range(request):
        try:
            start_time = round(time.time() * 1000.0)

            respond = requests.get(url, timeout=timeout)
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
    except:
        event.set()

def stress_test(arguments):
    for _ in range(arguments["connection"]):
        thread = Thread(target=send_request,args=(arguments["URL"], arguments["request"], arguments["timeout"]))
        thread.setDaemon(True)
        thread.start()
        thread_list.append(thread)

    checker_thread = Thread(target=check_thread)
    checker_thread.start()

    event.wait()

    return result["total_time"] / (arguments["request"] * arguments["connection"])