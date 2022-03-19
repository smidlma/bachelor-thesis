import Field from './Field'
interface Pipeline {
  id: number
  name: string
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

export { Pipeline, Transformation, Schema, Source }
