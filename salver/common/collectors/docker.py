# -*- coding: utf-8 -*-
import os
from typing import List, Union, Optional

import docker as docker_cli
from loguru import logger
from pydantic import BaseModel, ValidationError, root_validator

from .base import BaseCollector, CollectorBaseConfig


class DockerConfig(BaseModel):
    image: Optional[str] = None
    build_context: Optional[str] = None

    @root_validator
    def check_image(cls, values):
        image = values.get('image')
        build_context = values.get('build_context')

        if build_context and not os.path.exists(build_context):
            raise ValidationError(
                f'Docker build context {build_context} does not exists',
            )

        if (not image and not build_context) or (image and build_context):
            raise ValidationError(
                'Docker config should contains one of `image` or `build_context`',
            )
        return values


class BaseDockerConfig(CollectorBaseConfig):
    docker: DockerConfig


class DockerCollector(BaseCollector):
    def configure(self):
        self.config = BaseDockerConfig(**self.config)
        self.__client = docker_cli.from_env()
        build_context = self.config.docker.build_context

        if build_context:
            logger.debug(
                f'Building docker image {self.config.name} from {build_context}',
            )
            self.__build_image(build_context, tag=f'salver_{self.config.name}')

            self._image = f'salver_{self.config.name}'
        else:
            logger.debug(f'Pulling docker image {self.config.docker.image}')
            self.__pull_image(self.config.docker.image)
            self._image = self.config.docker.image

    def __pull_image(self, image, **kwargs):
        return self.__client.images.pull(image, **kwargs)

    def __build_image(self, path, tag, rm=True, **kwargs):
        return self.__client.images.build(path=path, tag=tag, rm=rm, **kwargs)

    def run_container(self, command: Union[str, List[str]], **kwargs):
        logger.debug(f'Run container {self._image} with {command}')
        return self.__client.containers.run(
            self._image,
            command,
            detach=False,
            remove=True,
            **kwargs,
        ).decode('utf-8')
