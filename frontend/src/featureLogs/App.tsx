import { Button, Table } from "antd";
import { useNavigate } from "react-router-dom";

const tableCol = [
    {
        title: "ID",
        dataIndex: "id",
        key: "id",
    },
    {
        title: "Name of Feature",
        dataIndex: "name",
        key: "name",
    },
    {
        title: "Description Status",
        dataIndex: "status",
        key: "status",
    },
]

const sampleData = [
    {
        "id": 1,
        "name": "XXX Name",
        "status": "Pending"
    },
    {
        "id": 2,
        "name": "XXX Name",
        "status": "Review"
    },
]

export default function Logs() {
    const navigate = useNavigate();
    return (
        <div style={{ padding: 24 }}>
            <h1 style={{"marginTop": 0}}>LOGS</h1>
            <div style={{"marginBottom": "10px"}}>
              <Button style={{ marginRight: '10px' }} onClick={() => navigate('/dashboard')}>View Dashboard</Button>
              <Button onClick={() => navigate('/')}>Go to PRD Form</Button>
            </div>
            <Table 
                columns={tableCol}
                dataSource={sampleData}
                rowKey="id"
            />
        </div>
    )
}