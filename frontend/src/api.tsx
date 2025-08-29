import axios from "axios"

interface Prd {
    Name: string
    Description: string
    Status?: string
}

interface FeatureData {
    prdId: string
    data: string
}

interface Log {
    prdId: string
    log: string
}

// API endpoints for PRD operations
export const fetchPrd = () => axios.get('/api/prd')
export const createPrd = (prd: Prd) => axios.post('/api/prd', prd)
export const deletePrd = (id: string) => axios.delete(`/api/prd/${id}`)
export const updatePrd = (id: string, prd: Prd) => axios.put(`/api/prd/${id}`, prd)

// API endpoints for feature data operations
export const fetchFeatureData = (prdId: string) => axios.get(`/api/feature-data/prd/${prdId}`)
export const createFeatureData = (featureData: FeatureData) => axios.post('/api/feature-data', featureData)
export const deleteFeatureData = (id: string) => axios.delete(`/api/feature-data/${id}`)
export const updateFeatureData = (id: string, featureData: FeatureData) => axios.put(`/api/feature-data/${id}`, featureData)

// API endpoints for logs operations
export const fetchLogs = (prdId: string) => axios.get(`/api/logs/prd/${prdId}`)
export const createLog = (log: Log) => axios.post('/api/logs', log)
export const deleteLog = (id: string) => axios.delete(`/api/logs/${id}`)