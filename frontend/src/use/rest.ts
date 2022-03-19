export default function () {
  const PORT = 8000
  const API_URL = `http://localhost:${PORT}/api`

  // Get all files on the server
  const getFiles = async (): Promise<Array<any>> => {
    const resp = await fetch(`${API_URL}/files`)
    const data = await resp.json()
    return data
  }

  const getConnections = async (): Promise<Array<any>> => {
    const resp = await fetch(`${API_URL}/connections`)
    const data = await resp.json()
    return data
  }
  return { getFiles, getConnections }
}
