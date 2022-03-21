import Field from './Field'
interface Pipeline {
  id: number
  name: string
  sources: Array<Source>
  joins: Array<Join>
  destination: Destination
}

interface Join {
  s1: Source
  s2: Source
  how: string
  on: string
  lsuffix: string
  rsuffix: string
}

interface Transformation {}

interface Schema {
  fields: Array<Field>
  primaryKey: Array<string>
}

interface Source {
  id: string
  name: string
  defaultSchema: Schema
  mappedSchema: Schema
  transformations: Array<Object>
  preview: Array<Object>
}

interface Connection {
  host: string
  port: number
  user: string
  password: string
  database: string
}

interface Destination {
  id: string
  destinationName: string
  targetTable: string
  connection: Connection
  mergeType: string
}

interface TableRow {
  name: string
  value: any
}

export {
  Pipeline,
  Transformation,
  Schema,
  Source,
  Connection,
  Destination,
  TableRow,
}
