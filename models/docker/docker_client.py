from docker import from_env, errors
from models.core.singleton import Singleton


class DockerClient(metaclass=Singleton):
    client = None

    def __init__(self):
        try:
            self.client = from_env()
        except errors.APIError:
            print("[!] Failed to connect to docker API.")
            exit()

    def get_docker_info(self):
        try:
            return self.client.info()
        except errors.APIError:
            print("[!] Failed to fetch docker info.")

    def get_docker_data_usage(self):
        try:
            return self.client.df()
        except errors.APIError:
            print("[!] Failed to fetch docker data usage.")

    def get_docker_version(self):
        try:
            return self.client.version()
        except errors.APIError:
            print("[!] Failed to fetch docker version.")

    def get_docker_image(self, name: str = None):
        try:
            return self.client.images.get(name)
        except errors.ImageNotFound:
            pass
        except errors.APIError:
            print("[!] Failed to fetch specific docker images.")

    def get_docker_image_list(self):
        try:
            return self.client.images.list()
        except errors.APIError:
            print("[!] Failed to list of fetch docker image.")

    def build_docker_image(self, name: str = None, tag: str = "latest", path: str = None, arg: dict = None):
        try:
            return self.client.images.build(tag="{}:{}".format(name, tag), path=path, buildargs=arg,
                                            network_mode="host")
        except errors.BuildError:
            print("[!] Failed to build docker image.")
        except errors.APIError:
            print("[!] Failed to build docker image.")
        except TypeError:
            print("[!] Invalid dockerfile path.")

    def remove_docker_image(self, name: str = None, tag: str = "latest", isForce: bool = False):
        try:
            return self.client.images.remove("{}:{}".format(name, tag), force=isForce)
        except errors.APIError:
            print("[!] Failed to remove specific docker image.")

    def get_docker_container(self, name: str = None):
        try:
            return self.client.containers.get(name)
        except errors.NotFound:
            pass
        except errors.APIError:
            print("[!] Failed to fetch specific docker container.")

    def get_docker_container_list(self, isAll: bool = False):
        try:
            return self.client.containers.list(all=isAll)
        except errors.APIError:
            print("[!] Failed to fetch list of docker container.")

    def create_docker_container(self, image: str = None, name: str = None, is_detach: bool = True, env: list = None,
                                port: dict = None, volume: dict = None, cpu_count: int = None, cpu_percent: int = None,
                                mem_limit: str = None, mem_swappiness: int = 60, memswap_limit: str = None):
        try:
            return self.client.containers.create(image=image, name=name, detach=is_detach, environment=env, ports=port,
                                                 volumes=volume, cpu_count=cpu_count, cpu_percent=cpu_percent,
                                                 mem_limit=mem_limit, mem_swappiness=mem_swappiness,
                                                 memswap_limit=memswap_limit,network_mode="bridge")
        except errors.ImageNotFound:
            print("[!] Docker image not found.")
        except errors.APIError:
            print("[!] Failed to create docker container.")

    def start_docker_container(self, name: str = None):
        try:
            container = self.client.containers.get(name)
            container.start()
            return container
        except errors.APIError:
            print("[!] Failed to start docker container.")

    def stop_docker_container(self, name: str = None):
        try:
            container = self.client.containers.get(name)
            container.stop()
            return container
        except errors.APIError:
            print("[!] failed to stop docker container.")

    def update_docker_container(self, name: str = None, mem_limit: str = None, memswap_limit: str = None):
        try:
            container = self.client.containers.get(name)
            container.update(mem_limit=mem_limit, memswap_limit=memswap_limit)
            return container
        except errors.APIError:
            print("[!] Failed to update docker container.")

    def remove_docker_container(self, name: str = None, isForce: bool = False):
        try:
            container = self.client.containers.get(name)
            container.remove(force=isForce)
            return container
        except errors.APIError:
            print("[!] Failed to remove docker container.")
