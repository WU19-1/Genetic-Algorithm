import docker

class DockerHandler:

    def __init__(self):
        self.client = None
        try:
            self.client = docker.from_env()
        except Exception as e:
            print("[!] Failed to connect to docker API. {}".format(e.args[-1]))

    def get_docker_info(self):
        try:
            return self.client.info()
        except Exception as e:
            print("[!] Failed to fetch docker info. {}.".format(e.args[-1]))
        return None

    def get_docker_data_usage(self):
        try:
            return self.client.df()
        except Exception as e:
            print("[!] Failed to fetch docker data usage. {}.".format(e.args[-1]))
        return None

    def get_docker_version(self):
        try:
            return self.client.version()
        except Exception as e:
            print("[!] Failed to fetch docker version. {}.".format(e.args[-1]))
        return None

    def get_docker_image(self, name=None):
        try:
            return self.client.images.get(name)
        except Exception as e:
            print("[!] Failed to fetch specific docker images. {}.".format(e.args[-1]))
        return None

    def get_docker_image_list(self):
        try:
            return self.client.images.list()
        except Exception as e:
            print("[!] Failed to fetch docker image list. {}.".format(e.args[-1]))
        return None

    def build_docker_image(self, name=None, tag="latest", path=None, arg={}):
        try:
            return self.client.images.build(tag="{}:{}".format(name, tag), path=path, buildargs=arg, network_mode="host")
        except Exception as e:
            print("[!] Failed to build docker image. {}.".format(e.args[-1]))

    def remove_docker_image(self, name=None, tag="latest", isForce=False):
        try:
            return self.client.images.remove("{}:{}".format(name, tag), force=isForce)
        except Exception as e:
            print("[!] Failed to remove specific docker image. {}.".format(e.args[-1]))

    def get_docker_container(self, name=None):
        try:
            return self.client.containers.get(name)
        except Exception as e:
            print("[!] Failed to fetch specific docker container. {}.".format(e.args[-1]))
        return None

    def get_docker_container_list(self, isAll=False):
        try:
            return self.client.containers.list(all=isAll)
        except Exception as e:
            print("[!] Failed to fetch docker container list. {}.".format(e.args[-1]))
        return None

    def create_docker_container(self, image=None, name=None, isDetach=True, env=[], port=None, volume={}, mem_limit=None, mem_reservation=None, mem_swappiness=None, memswap_limit=None, cpu_count=None, cpu_percent=None):
        try:
            return self.client.containers.create(image=image, name=name, detach=isDetach, environment=env, ports=port, volumes=volume, 
                                                 mem_limit=mem_limit, mem_reservation=mem_reservation, mem_swappiness=mem_swappiness, memswap_limit=memswap_limit,
                                                 cpu_count=cpu_count, cpu_percent=cpu_percent)
        except Exception as e:
            print("[!] Failed to create docker container. {}.".format(e.args[-1]))
        return None

    def start_docker_container(self, name=None):
        try:
            container = self.client.containers.get(name) 
            container.start()
            return container
        except Exception as e:
            print("[!] Failed to start docker container. {}.".format(e.args[-1]))
        return None

    def stop_docker_container(self, name=None):
        try:
            container = self.client.containers.get(name)
            container.stop()
            return container
        except Exception as e:
            print("[!] failed to stop docker container. {}.".format(e.args[-1]))
        return None

    def update_docker_container(self, name=None, mem_limit=None, mem_reservation=None, memswap_limit=None):
        try:
            container = self.client.containers.get(name)
            container.update(mem_limit=mem_limit, mem_reservation=mem_reservation, memswap_limit=memswap_limit)
            return container
        except Exception as e:
            print("[!] Failed to update docker container. {}.".format(e.args[-1]))
            print(e)
        return None

    def remove_docker_container(self, name=None, isForce=False):
        try:
            container = self.client.containers.get(name)
            container.remove(force=isForce)
            return container
        except Exception as e:
            print("[!] Failed to remove docker container. {}.".format(e.args[-1]))
        return None