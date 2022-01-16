from models.docker.docker_client import DockerClient


class DockerContainer:

    def __init__(self, container_object):
        self.name = container_object["name"]
        self.image_name = container_object["image_name"]
        self.image_version = container_object["image_version"]
        self.image_full_name = "{}:{}".format(self.image_name, self.image_version)
        self.port_str = container_object["port"]
        self.port = {"{}/tcp".format(self.port_str.split(":")[1]): int(self.port_str.split(":")[0])}
        self.volume_str = container_object["volume"]
        self.volume = {"{}".format(self.volume_str.rsplit(":", 1)[0]): {
                    "bind": "{}".format(self.volume_str.rsplit(":", 1)[1]),
                    "mode": "rw"
                    }
                } if self.volume_str is not None \
                else None
        self.cpu_count = container_object["cpu_count"]
        self.cpu_percent = container_object["cpu_percent"]
        self.memory_limit = container_object["memory_limit"]
        self.memory_swap_limit = container_object["memory_swap_limit"]
        self.is_detach = container_object["is_detach"]

    def create_container(self):
        container = DockerClient().get_docker_container(name=self.name)
        if container is not None:
            DockerClient().remove_docker_container(name=self.name, isForce=True)

        DockerClient().create_docker_container(image=self.image_full_name, name=self.name, port=self.port,
                                               cpu_count=self.cpu_count, cpu_percent=self.cpu_percent,
                                               mem_limit=self.memory_limit, volume=self.volume,
                                               is_detach=self.is_detach)

    def run_container(self):
        container = DockerClient().get_docker_container(name=self.name)
        if container is not None:
            DockerClient().start_docker_container(name=self.name)

    def stop_container(self):
        container = DockerClient().get_docker_container(name=self.name)
        if container is not None:
            DockerClient().stop_docker_container(name=self.name)

    def remove_container(self):
        container = DockerClient().get_docker_container(name=self.name)
        if container is not None:
            DockerClient().remove_docker_container(name=self.name, isForce=True)
