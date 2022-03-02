from .sources import Source
from .destinations import Destination, InsertOption
from .transformations import Transformation
import logging as log
import mongoengine as mongo

# Pipeline class for holding and updating state of the pipeline
class Pipeline(mongo.Document):
    name = mongo.StringField()
    sources = mongo.ListField(mongo.ReferenceField(Source))
    destination = mongo.ReferenceField(Destination)
    transformations = mongo.ListField(mongo.ReferenceField(Transformation))

    def __init__(self, name, sources: list[Source] = [], transformations: list[Transformation] = [], destination=None, **data) -> None:
        super(Pipeline, self).__init__(name=name, sources=sources, transformations=transformations, destination=destination, **data)

    def addSource(self, source: Source):
        self.sources.append(source)

    def addTransformation(self, transformation: Transformation):
        self.transformations.append(transformation)

    def setDestination(self, destination: Destination):
        self.destination = destination

    def run(self):
        log.debug(f'Running pipeline: {self.name}')
        df = self.sources[0].extract()
        affected = self.destination.load(df, InsertOption.REPLACE)
        log.debug(f'Rows affected: {affected}')
        return affected
