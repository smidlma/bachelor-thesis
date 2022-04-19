from typing import List
from pandas import DataFrame
import etl.models.transformations as tr
import etl.models.sources as source
import etl.models.destinations as dest
import logging as log
import mongoengine as mongo


class Pipeline(mongo.Document):
    """
    Pipeline class for holding, updating and processing state of the pipeline
    """

    name = mongo.StringField()
    sources = mongo.EmbeddedDocumentListField(source.Source)
    destination = mongo.EmbeddedDocumentField(dest.Destination)
    joins = mongo.EmbeddedDocumentListField(source.Join)

    def __init__(
        self,
        name,
        sources: List[source.Source] = [],
        joins: List[source.Join] = [],
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
        df = self.sources[0].runTransformations()
        affected = self.destination.load(df)
        log.debug(f"Rows affected: {affected}")
        return affected

    def run(self):
        try:
            transformedSource = dict()
            # Run local trans of sources and save to dict
            lastTransformedId = None
            for source in self.sources:
                lastTransformedId = source.id
                transformedSource[source.id] = source.runTransformations()

            # Run joins of sources
            for join in self.joins:
                lastTransformedId = join.id
                transformedSource[join.id] = join.join(
                    transformedSource.get(join.s1.id), transformedSource.get(join.s2.id)
                )
                log.info(transformedSource[join.id])

            # Call destination to load df to db
            rowsAffected = self.moveToDestination(transformedSource[lastTransformedId])

            return {
                "success": True,
                "rowsAffected": rowsAffected,
                "message": f"Successful run with {rowsAffected} rows affected.",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def moveToDestination(self, df: DataFrame):
        return self.destination.load(df)

    def json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "sources": [s.json() for s in self.sources],
            "destination": self.destination.json() if self.destination else None,
            "joins": [j.json() for j in self.joins],
        }
