from .sources import Source
from .destinations import Destination, TableOptions
from .transformations import Transformation
import logging as log


class Pipeline:
    def __init__(self, name, sources: list[Source] = [], transformations: list[Transformation] = [], destination=None) -> None:
        self.name = name
        self.sources = sources
        self.destination = destination
        self.transformations = transformations

    def addSource(self, source: Source):
        self.sources.append(source)

    def addTransformation(self, transformation: Transformation):
        self.transformations.append(transformation)

    def setDestination(self, destination: Destination):
        self.destination = destination

    def run(self):
        log.debug(f'Running pipeline: {self.name}')
        df = self.sources[0].extract()
        affected = self.destination.load(df, TableOptions.REPLACE)
        log.debug(f'Rows affected: {affected}')
        
