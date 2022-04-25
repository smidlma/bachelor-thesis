import { HOST, PORT } from '../config'
import { Pipeline } from '../types/Pipeline'

export default function () {
  const API_URL = `http://${HOST}:${PORT}/api`

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

  const runPipeline = async (id: string) => {
    const resp = await fetch(`${API_URL}/pipelines/run/${id}`)
    const data = await resp.json()
    return data
  }

  return {
    runPipeline,
    getFiles,
    getConnections,
    testConnection,
    getPipelines,
    createPipeline,
    createConnection,
    API_URL,
  }
}
