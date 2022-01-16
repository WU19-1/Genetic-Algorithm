from models.docker.docker_client import DockerClient


class DockerImage:

    def __init__(self, image_object):
        self.name = image_object["name"]
        self.version = image_object["version"]
        self.full_name = "{}:{}".format(self.name, self.version)
        self.path = image_object["path"]
        self.arg = image_object["arg"]

    def create_image(self):
        image = DockerClient().get_docker_image(name=self.name)
        if image is not None:
            DockerClient().remove_docker_image(name=self.name, tag=self.version, isForce=True)

        DockerClient().build_docker_image(name=self.name, tag=self.version, path=self.path, arg=self.arg)

    def remove_image(self):
        image = DockerClient().get_docker_image(name=self.name)
        if image is not None:
            DockerClient().remove_docker_image(name=self.name, tag=self.version, isForce=True)
