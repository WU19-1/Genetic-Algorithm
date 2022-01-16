from controller.stress_test_controller import build_website, build_stress_test, run_website

CONNECTION = 25
REQUEST = 60


def manual_stress_test():
    global CONNECTION, REQUEST

    cpu_count = None
    cpu_percentage = None
    memory = None

    is_limit = input("[?] Limit Resource [y|n] >> ")
    if is_limit == 'y':
        cpu_count = int(input("[?] CPU Count >> "))
        cpu_percentage = int(input("[?] CPU Percentage: >> "))
        memory = input("[?] Memory: >> ")

    build_website()

    for i in range(6):
        build_stress_test(str(REQUEST), str(CONNECTION))
        average_response_time = run_website(cpu_count, cpu_percentage, memory)
        print("[*] {} connection (@{} request/connection) => {} ms".format(CONNECTION, REQUEST, average_response_time))
        CONNECTION *= 2
