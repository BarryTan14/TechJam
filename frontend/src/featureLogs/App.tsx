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

const signOut = () => {
  localStorage.removeItem("username")
  window.location.href = "../login" 
}

export default function Logs() {
    if (!localStorage.getItem("username")) {
      window.location.href = "./login"
      return
    }

    const navigate = useNavigate();

    return (
        <div style={{ padding: 24 }}>
            <div style={{display: "flex"}}>
                <h1 style={{"marginTop": 0}}>LOGS</h1>
                <Button style={{ marginLeft: "auto" }} onClick={() => signOut()}>Sign Out</Button>
            </div>
            <div style={{"marginBottom": "10px"}}>
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