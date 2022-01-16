from typing import Dict
from models.docker.docker_client import DockerClient
from models.docker.docker_image import DockerImage
from models.docker.docker_container import DockerContainer
from os import getenv, getcwd, listdir, name, remove
from time import sleep
import random
from container.stress.src.stress import run


def build_website():
    image_website = {
        "name": getenv("WEB_IMAGE_NAME"),
        "version": getenv("WEB_IMAGE_VERSION"),
        "path": "{}{}".format(getcwd(), getenv("WEB_IMAGE_PATH")),
        "arg": {},
    }
    image = DockerImage(image_object=image_website)

    image.create_image()

def build_images(web_containers : Dict = None):
    for web in web_containers:
        print(web)
        image = DockerImage(image_object=web)
        image.create_image()

def build_single_image(web_container : Dict = None):
    print(web_container)
    image = DockerImage(image_object=web_container)
    image.create_image()

def build_stress_test(total_request: int, total_connection: int):
    image_stress_test_object = {
        "name": getenv("PYTHON_IMAGE_NAME"),
        "version": getenv("PYTHON_IMAGE_VERSION"),
        "path": "{}{}".format(getcwd(), getenv("PYTHON_IMAGE_PATH")),
        "arg": {
            "TOTAL_REQUEST": total_request,
            "TOTAL_CONNECTION": total_connection,
            "URL": getenv("PYTHON_IMAGE_URL")
        }
    }
    image = DockerImage(image_object=image_stress_test_object)

    image.create_image()


def run_website(cpu_count: int, cpu_percent: int, memory_limit: int):
    container_object = {
        "name": getenv("WEB_CONTAINER_NAME"),
        "image_name": getenv("WEB_IMAGE_NAME"),
        "image_version": getenv("WEB_IMAGE_VERSION"),
        "port": getenv("WEB_CONTAINER_PORT"),
        "volume": None,
        "cpu_count": cpu_count,
        "cpu_percent": cpu_percent,
        "memory_limit": memory_limit,
        "memory_swap_limit": memory_limit,
        "is_detach": True,
    }
    container = DockerContainer(container_object=container_object)

    container.create_container()
    container.run_container()

    average_response_time = run_stress_test()

    container.stop_container()
    container.remove_container()

    return average_response_time

def run_websites(cpu_count: int, cpu_percent: int, memory_limit: int, web_container: Dict):
    averages = 0.0

    for web in web_container:
        container_object = {
            "name": web["container_name"],
            "image_name": web["name"],
            "image_version": web["version"],
            "port": web["port"],
            "volume": None,
            "cpu_count": cpu_count,
            "cpu_percent": cpu_percent,
            "memory_limit": memory_limit,
            "memory_swap_limit": memory_limit,
            "is_detach": True,
        }

        container = DockerContainer(container_object=container_object)

        container.create_container()
        container.run_container()

        average_response_time = targeted_stress_test(web)

        container.stop_container()
        container.remove_container()

        averages += average_response_time
    
    return averages / len(web_container)

def run_single_website(cpu_count: int, cpu_percent: int, memory_limit: int, web: Dict):
    container_object = {
        "name": web["container_name"],
        "image_name": web["name"],
        "image_version": web["version"],
        "port": web["port"],
        "volume": None,
        "cpu_count": cpu_count,
        "cpu_percent": cpu_percent,
        "memory_limit": memory_limit,
        "memory_swap_limit": memory_limit,
        "is_detach": True,
    }

    container = DockerContainer(container_object=container_object)

    container.create_container()
    container.run_container()

    average_response_time = targeted_stress_test(web)

    container.stop_container()
    container.remove_container()
    
    return average_response_time

def run_container(web_container, configuration):
    container_object = {
        "name": web_container["container_name"],
        "image_name": web_container["name"],
        "image_version": web_container["version"],
        "port": web_container["port"],
        "volume": None,
        "cpu_count": configuration['cpu_count'],
        "cpu_percent": configuration['cpu_percent'],
        "memory_limit": configuration['memory_limit'],
        "memory_swap_limit": configuration['memory_limit'],
        "is_detach": True,
    }

    print(configuration)

    container = DockerContainer(container_object=container_object)

    container.create_container()
    container.run_container()

def targeted_stress_test(web_container : dict):
    average_time = run("http://10.22.66.111:%s/"%(web_container["port"].split(":")[0]), 10, 10)
    return float(average_time)

def run_stress_test():
    container_stress_test_object = {
        "name": getenv("PYTHON_CONTAINER_NAME"),
        "image_name": getenv("PYTHON_IMAGE_NAME"),
        "image_version": getenv("PYTHON_IMAGE_VERSION"),
        "port": getenv("PYTHON_CONTAINER_PORT"),
        "volume": "{}{}".format(getcwd(), getenv("PYTHON_CONTAINER_VOLUME")),
        "memory_limit": getenv("PYTHON_CONTAINER_MEMORY_LIMIT"),
        "memory_swap_limit": getenv("PYTHON_CONTAINER_MEMORY_LIMIT"),
        "cpu_count": int(getenv("PYTHON_CONTAINER_CPU_COUNT")),
        "cpu_percent": int(getenv("PYTHON_CONTAINER_CPU_PERCENT")),
        "is_detach": True,
    }
    container = DockerContainer(container_object=container_stress_test_object)

    container.create_container()
    container.run_container()

    result_not_found = True
    while result_not_found:
        list_file = listdir("{}/container/stress-test/src/".format(getcwd()))
        for file in list_file:
            if file == getenv("PYTHON_IMAGE_RESULT"):
                result_not_found = False
        sleep(1)

    container.stop_container()
    container.remove_container()

    average_time = open("{}/container/stress-test/src/{}".format(getcwd(), getenv("PYTHON_IMAGE_RESULT")), "r").read()
    remove("{}/container/stress-test/src/{}".format(getcwd(), getenv("PYTHON_IMAGE_RESULT")))

    return float(average_time)
