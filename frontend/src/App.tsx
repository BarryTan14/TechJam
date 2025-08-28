import { Table, Button, Popconfirm, Row, Modal, Space, Form, Select, Input } from "antd"
import { DeleteOutlined, EditOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useState } from "react";

const tableCol = (onEditDetail: (detail: any) => void, onDelete: (detail: any) => void) => [
    {
        title: "ID",
        dataIndex: "id",
        key: "id",
    },
    {
        title: "Name",
        dataIndex: "name",
        key: "name",
    },
    {
        title: "Description Status",
        dataIndex: "status",
        key: "status",
    },
    {
    key: "Actions",
    render: (_: any, record: any) => (
      <div key={record.id} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <Button onClick={() => onEditDetail(record)}>
          <EditOutlined />
        </Button>
        &nbsp;
        <Popconfirm
          title="Delete the PRD?"
          description="Are you sure to delete this?"
          okText="Yes"
          cancelText="No"
          onConfirm={() => onDelete(record)}
        >
          <Button>
            <DeleteOutlined />
          </Button>
        </Popconfirm>
      </div>
    ),  
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

const ModalForm = () => {
  return (
    <Form layout="vertical">
          <Form.Item
            name="status"
            label="Status"
          >
            <Select 
              placeholder="Please select status"
            >
            </Select>
          </Form.Item>        
          <Form.Item
            name="name"
            label="Name"
          >
            <Input 
              placeholder="Enter name of PRD" 
            />
          </Form.Item>
    </Form>
  )
}

export default function App() {
    const navigate = useNavigate();
    const [openModal, setOpenModal] = useState(false)

    // Following two functions is to handle new detail
    const showModal = () => {
        setOpenModal(true);
    };

    const onCloseModal = () => {
        setOpenModal(false);
    };

    return (
        <div style={{ padding: 24 }}>
            <h1 className='text-3xl font-extrabold' style={{"marginTop": 0}}>PRD FORM</h1>
            <div>
              <Button onClick={() => navigate('/dashboard')}>View Dashboard</Button>
            </div>
            <Row justify="end" style={{marginBottom: "10px"}}>
              <Button title="Add new PRD" onClick={showModal}>Add New PRD</Button>
            </Row>
            <Modal
              title="Create a new PRD"
              width={720}
              open={openModal}
              onCancel={onCloseModal}
              okText="Submit"
              styles={{
              body: {
                  paddingBottom: 80,
              },
              }}>
                <ModalForm></ModalForm>
            </Modal>
            <Table 
                columns={tableCol(()=>{}, () => {})}
                dataSource={sampleData}
                rowKey="id"
            />
        </div>
    )
}