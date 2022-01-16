from models.docker.docker_client import DockerClient
from hurry.filesize import size, si
import psutil


def show_docker_information():
    version = DockerClient().get_docker_version()
    info = DockerClient().get_docker_info()
    data_usage = DockerClient().get_docker_data_usage()

    if version is None or info is None or data_usage is None:
        return

    print("%s (%s %s)" % (version["Platform"]["Name"], version["Os"], version["Arch"]))
    print("Version: %s" % (version["Version"]))
    print("API Version: %s" % (version["ApiVersion"]), end="\n\n")

    print("Images (%s)" % (str(info["Images"])))
    for image in data_usage["Images"]:
        print("- %-30s %s" % (image["RepoTags"][0], size(image["Size"], system=si)))
    print()

    print("Container (%s/%s) " % (str(info["ContainersRunning"]), str(info["Containers"])))
    for container in data_usage["Containers"]:
        print("- %-30s %-10s (%s)" % (container["Names"][0], container["State"], container["Status"]))
    print()


def show_docker_usage():
    print("[HOST] - [MEM] : %s/%s (%s%%)" % (size(psutil.virtual_memory().used, system=si),
                                             size(psutil.virtual_memory().total, system=si),
                                             str(psutil.virtual_memory().percent)))
    print("[HOST] - [CPU] : %s%%" % (psutil.cpu_percent()), end="\n\n")

    containers = DockerClient().get_docker_container_list()
    if containers is None:
        return

    for container in containers:
        status = container.stats(stream=False)
        print("Container %s" % status["name"])
        print("[CONT] - [MEM] : %s/%s (max: %s)" % (size(status["memory_stats"]["usage"], system=si),
                                                      size(status["memory_stats"]["limit"], system=si),
                                                      size(status["memory_stats"]["max_usage"], system=si)))
        cpu_percent = 0.0
        cpu_delta = float(status["cpu_stats"]["cpu_usage"]["total_usage"]) - \
                    float(status["precpu_stats"]["cpu_usage"]["total_usage"])
        system_delta = float(status["cpu_stats"]["system_cpu_usage"]) - \
                       float(status["precpu_stats"]["system_cpu_usage"])
        if system_delta > 0.0:
            cpu_percent = (cpu_delta / system_delta) * status["cpu_stats"]["online_cpus"] * 100.0
        print("[CONT] - [CPU] : %.2f%%" % float(cpu_percent), end="\n\n")


