from handler import DockerHandler
from os import cpu_count

DOCKER_HANDLER = DockerHandler()

def create_image(web_configuration):
    image_name = web_configuration["name"]
    image_version = web_configuration["version"]
    image_path = web_configuration["path"]
    image_full = "{}:{}".format(image_name, image_version)

    image = DOCKER_HANDLER.get_docker_image(name=image_name)
    if image != None:
        print("[*] Removing {} docker image".format(image_full))
        DOCKER_HANDLER.remove_docker_image(name=image_name, tag=image_version, isForce=True)
        print("[*] Successfully to remove {} docker image".format(image_full))

    print("[*] Creating {} docker image".format(image_full))
    image = DOCKER_HANDLER.build_docker_image(name=image_name, tag=image_version, path=image_path)
    print("[*] Succesfully to create {} docker image".format(image_full))

def create_container(web_configuration):
    image_name = web_configuration["name"]
    image_version = web_configuration["version"]
    image_full = "{}:{}".format(image_name, image_version)

    container_name = web_configuration["name"]
    container_port_str = web_configuration["port"]
    container_port = {"{}/tcp".format(container_port_str.split(":")[1]) : int(container_port_str.split(":")[0])}
    container_mem_limit = web_configuration["mem_limit"]
    container_cpu_count = web_configuration["cpu_count"]
    container_cpu_percent = web_configuration["cpu_percent"]

    container = DOCKER_HANDLER.get_docker_container(name=container_name)
    if container != None:
        print("[*] Removing {} docker container".format(container_name))
        DOCKER_HANDLER.remove_docker_container(name=container_name, isForce=True)
        print("[*] Successfully to remove {} docker container".format(container_name))

    print("[*] Creating {} docker container".format(container_name))
    container = DOCKER_HANDLER.create_docker_container(image=image_full, name=container_name, port=container_port, 
                                                        mem_limit=container_mem_limit, 
                                                        cpu_count=container_cpu_count, cpu_percent=container_cpu_percent)
    print("[*] Successfully to create {} docker container".format(container_name))
    print("[*] Running {} docker container".format(container_name))
    container.start()
    print("[*] Successfully to run {} docker container".format(container_name))

def run_container(web_configuration):
    container_name = web_configuration["name"]

    container = DOCKER_HANDLER.get_docker_container(name=container_name)
    if container != None:
        print("[*] Running {} docker container".format(container_name))
        container.start()
        print("[*] Successfully to run {} docker container".format(container_name))

def stop_container(web_configuration):
    container_name = web_configuration["name"]

    container = DOCKER_HANDLER.get_docker_container(name=container_name)
    if container != None:
        print("[*] Stopping {} docker container".format(container_name))
        DOCKER_HANDLER.stop_docker_container(name=container_name)
        print("[*] Successfully to stop {} docker container".format(container_name))
        DOCKER_HANDLER.remove_docker_container(name=container_name)