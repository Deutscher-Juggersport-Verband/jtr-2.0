import os
from collections import defaultdict
from typing import List

import yaml
from flask import Blueprint

from DataDomain.Model import Response

externalApiFolder = Blueprint(
    'external_api',
    __name__,
    static_folder=os.path.join(
        '/home/backend/ExternalApi')
)


class GetSwaggerFileHandler:

    def handle(self) -> Response:
        """Get swagger file"""

        yamlFiles = []

        for root, dirs, files in os.walk(externalApiFolder.static_folder):
            for file in files:
                if file.endswith('.yaml'):
                    yamlFiles.append(os.path.join(root, file))

        yamlUrls = [os.path.abspath(file) for file in yamlFiles]

        return Response(
            response=self.__mergeYamlFiles(yamlUrls),
            status=200,
        )

    @staticmethod
    def __mergeYamlFiles(yamlFilePaths: List[str]) -> dict:
        """Merge multiple yaml files into a single dictionary"""

        mergedData = {
            'openapi': '3.0.0',
            'info': {
                'title': 'JTR API',
                'version': '1.0.0'
            },
            'paths': defaultdict(dict)
        }

        """Merge the paths from each file"""

        for file_path in yamlFilePaths:
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)

                for path, pathData in data.get('paths', {}).items():
                    if path in mergedData['paths']:

                        mergedData['paths'][path].update(pathData)

                    else:
                        mergedData['paths'][path] = pathData

        """Convert the default-dict to a regular dict"""

        mergedData['paths'] = dict(mergedData['paths'])

        return mergedData
