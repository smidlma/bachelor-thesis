
import etl.models.transformations as tr
import etl.models.sources as source
import etl.models.destinations as dest
import logging as log
import mongoengine as mongo

# Pipeline class for holding and updating state of the pipeline


class Pipeline(mongo.Document):
    name = mongo.StringField()
    sources = mongo.ListField(mongo.ReferenceField(source.Source))
    destination = mongo.ReferenceField(dest.Destination)
    joins = mongo.ListField(mongo.ReferenceField(source.Join))

    def __init__(self, name, sources: list[source.Source] = [], joins: list[source.Join] = [], destination=None, **data) -> None:
        super(Pipeline, self).__init__(name=name, sources=sources,
                                       joins=joins, destination=destination, **data)

    def addSource(self, source: source.Source):
        self.sources.append(source)

    def addJoin(self, join: source.Join):
        self.joins.append(join)

    def setDestination(self, destination: dest.Destination):
        self.destination = destination

    def runTest(self):

        log.debug(f'Running pipeline: {self.name}')
        df = self.sources[0].extract()
        affected = self.destination.load(df, dest.InsertOption.REPLACE)
        log.debug(f'Rows affected: {affected}')
        return affected

    def run(self):
        transformedSource = dict()
        # Run local trans of sources and save to dict
        for source in self.sources:
            transformedSource[source.id] = source.runTransformations()

        log.info(transformedSource)

        for join in self.joins:
            join.join()

    def moveToDestination(self):
        pass
