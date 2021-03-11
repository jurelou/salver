import os
from typing import List
from typing import Optional
from typing import Union

import docker
from pydantic import BaseModel
from pydantic import root_validator

from opulence.agent.collectors.base import BaseCollector
from opulence.agent.collectors.base import BaseConfig


class DockerConfig(BaseModel):
    image: Optional[str] = None
    build_context: Optional[str] = None

    @root_validator
    def check_passwords_match(cls, values):
        image = values.get("image")
        build_context = values.get("build_context")

        if (not image and not build_context) or (image and build_context):
            raise ValueError(
                "Docker config should contains one of `image` or `build_context`",
            )
        return values


class BaseDockerConfig(BaseConfig):
    docker: DockerConfig


class DockerCollector(BaseCollector):
    def configure(self):
        self.config = BaseDockerConfig(**self.config)
        self.__client = docker.from_env()
        if self.config.docker.build_context:
            self.__build_image(
                self.config.docker.build_context, tag=f"opu_{self.config.name}",
            )
            self.__image = f"opu_{self.config.name}"
        else:
            self.__pull_image(self.config.docker.image)
            self.__image = self.config.docker.image

    def __pull_image(self, image, **kwargs):
        return self.__client.images.pull(image, **kwargs)

    def __build_image(self, path, tag, rm=True, **kwargs):
        return self.__client.images.build(path=path, tag=tag, rm=rm, **kwargs)

    def run_container(self, command: Union[str, List[str]], **kwargs):
        return self.__client.containers.run(
            self.__image, command, detach=False, remove=True, **kwargs,
        ).decode("utf-8")
