import { Pipeline } from '../types/Pipeline'

export default function () {
  const PORT = 8000
  const API_URL = `http://localhost:${PORT}/api`

  const getAll = async (endpoint: string): Promise<Array<any>> => {
    try {
      const resp = await fetch(`${API_URL}/${endpoint}`)
      const data = await resp.json()
      return data
    } catch {
      return []
    }
  }

  const post = async (endpoint: string, body: any) => {
    const resp = await fetch(`${API_URL}/${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })
    const data = await resp.json()
    return data
  }

  // Get all files on the server
  const getFiles = async (): Promise<Array<any>> => {
    return await getAll('files')
  }

  const getConnections = async (): Promise<Array<any>> => {
    return await getAll('connections')
  }

  const getPipelines = async (): Promise<Array<Pipeline>> => {
    return await getAll('pipelines')
  }

  const testConnection = async (body: any): Promise<any> => {
    return await post('connections/test', body)
  }

  const createPipeline = async (body: any): Promise<any> => {
    return await post('pipelines', body)
  }

  const createConnection = async (body: any): Promise<any> => {
    return await post('connections', body)
  }

  return {
    getFiles,
    getConnections,
    testConnection,
    getPipelines,
    createPipeline,
    createConnection,
    API_URL,
  }
}
