import { SelectOption } from 'naive-ui'

const pandasDataTypes: Array<SelectOption> = [
  { label: 'integer', value: 'integer' },
  { label: 'number', value: 'number' },
  { label: 'boolean', value: 'boolean' },
  { label: 'string', value: 'string' },
  { label: 'category', value: 'any' },
  { label: 'datetime', value: 'datetime' },
]

const insertOptions: Array<SelectOption> = [
  { label: 'APPEND', value: 'append' },
  { label: 'REPLACE', value: 'replace' },
  { label: 'FAIL', value: 'fail' },
]

export { pandasDataTypes, insertOptions }
