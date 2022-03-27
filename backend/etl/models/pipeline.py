import asyncio
from time import sleep
import etl.models.transformations as tr
import etl.models.sources as source
import etl.models.destinations as dest
import logging as log
import mongoengine as mongo

# Pipeline class for holding and updating state of the pipeline


class Pipeline(mongo.Document):
    name = mongo.StringField()
    sources = mongo.EmbeddedDocumentListField(source.Source)
    destination = mongo.EmbeddedDocumentField(dest.Destination)
    joins = mongo.EmbeddedDocumentListField(source.Join)

    def __init__(
        self,
        name,
        sources: list[source.Source] = [],
        joins: list[source.Join] = [],
        destination=None,
        **data,
    ) -> None:
        super(Pipeline, self).__init__(
            name=name, sources=sources, joins=joins, destination=destination, **data
        )

    def addSource(self, source: source.Source):
        self.sources.append(source)

    def addJoin(self, join: source.Join):
        self.joins.append(join)

    def setDestination(self, destination: dest.Destination):
        self.destination = destination

    def runTest(self):
        log.debug(f"Running pipeline: {self.name}")
        df = self.sources[0].extract()
        affected = self.destination.load(df, dest.InsertOption.REPLACE)
        log.debug(f"Rows affected: {affected}")
        return affected

    async def run(self):
        try:
            transformedSource = dict()
            # Run local trans of sources and save to dict
            for source in self.sources:
                transformedSource[source.id] = source.runTransformations()
                # log.info(source.id)

            # log.info(transformedSource)

            for join in self.joins:
                transformedSource[join.id] = join.join(
                    transformedSource.get(join.s1.id), transformedSource.get(join.s2.id)
                )

                log.info(transformedSource[join.id])
            print("going to sleep")
            await asyncio.sleep(10)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def moveToDestination(self):
        pass

    def json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "sources": [s.json() for s in self.sources],
            "destination": self.destination.json() if self.destination else None,
            "joins": [j.json() for j in self.joins],
        }
