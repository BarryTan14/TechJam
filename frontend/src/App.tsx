import { Table, Button, Popconfirm, Row, Modal, Form, Input, message } from "antd"
import { DeleteOutlined, EditOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from "react";
import { fetchPrd, createPrd, deletePrd, updatePrd } from "./api";
import type { FormInstance } from 'antd/es/form';

interface PrdData {
    ID: string;
    Name: string;
    Description: string;
    Status: string;
    created_at?: string;
    updated_at?: string;
}

const tableCol = (onEditDetail: (detail: PrdData) => void, onDelete: (detail: PrdData) => void) => [
    {
        title: "ID",
        dataIndex: "ID",
        key: "ID",
    },
    {
        title: "Name",
        dataIndex: "Name",
        key: "Name",
    },
    {
        title: "Description",
        dataIndex: "Description",
        key: "Description",
    },
    {
        title: "Status",
        dataIndex: "Status",
        key: "Status",
    },
    {
    key: "Actions",
    render: (_: any, record: PrdData) => (
      <div key={record.ID} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
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

const signOut = () => {
  localStorage.removeItem("username")
  window.location.href = "../login" 
}

interface ModalFormProps {
    form: FormInstance;
    isEdit?: boolean;
    initialValues?: Partial<PrdData>;
}

const ModalForm: React.FC<ModalFormProps> = ({ form, isEdit = false, initialValues = {} }) => {
  return (
    <Form 
      form={form}
      layout="vertical"
      initialValues={initialValues}
    >     
          <Form.Item
            name="Name"
            label="Name"
            rules={[{ required: true, message: 'Please enter the PRD name!' }]}
          >
            <Input 
              placeholder="Enter name of PRD" 
            />
          </Form.Item>
          <Form.Item
            name="Description"
            label="Description"
            rules={[{ required: true, message: 'Please enter the PRD description!' }]}
          >
            <Input.TextArea 
              rows={4} 
              placeholder="Please enter description" 
            />
          </Form.Item>
          <Form.Item
            name="Status"
            label="Status"
            rules={[{ required: true, message: 'Please select the PRD status!' }]}
          >
            <Input 
              placeholder="Enter status (e.g., Draft, Review, Approved)" 
            />
          </Form.Item>
    </Form>
  )
}

export default function App() {
    if (!localStorage.getItem("username")) {
      window.location.href = "./login"
      return
    }

    const navigate = useNavigate();
    const [openModal, setOpenModal] = useState(false);
    const [isEdit, setIsEdit] = useState(false);
    const [currentPrd, setCurrentPrd] = useState<PrdData | null>(null);
    const [prdData, setPrdData] = useState<PrdData[]>([]);
    const [loading, setLoading] = useState(false);
    const [form] = Form.useForm();

    // Fetch PRDs on component mount
    useEffect(() => {
        fetchPrdData();
    }, []);

    const fetchPrdData = async () => {
        try {
            setLoading(true);
            const response = await fetchPrd();
            setPrdData(response.data);
            // Note: Backend automatically logs all operations including fetches
        } catch (error) {
            console.error('Error fetching PRDs:', error);
            message.error('Failed to fetch PRDs');
        } finally {
            setLoading(false);
        }
    };

    const showModal = (prd: PrdData | null = null) => {
        if (prd) {
            setIsEdit(true);
            setCurrentPrd(prd);
            form.setFieldsValue({
                Name: prd.Name,
                Description: prd.Description,
                Status: prd.Status
            });
        } else {
            setIsEdit(false);
            setCurrentPrd(null);
            form.resetFields();
        }
        setOpenModal(true);
    };

    const onCloseModal = () => {
        setOpenModal(false);
        setIsEdit(false);
        setCurrentPrd(null);
        form.resetFields();
    };

    const handleSubmit = async () => {
        try {
            const values = await form.validateFields();
            
            if (isEdit && currentPrd) {
                // Update existing PRD
                await updatePrd(currentPrd.ID, values);
                message.success('PRD updated successfully');
                // Note: Backend automatically logs the update operation
            } else {
                // Create new PRD
                const response = await createPrd(values);
                message.success('PRD created successfully');
                // Note: Backend automatically logs the creation operation
            }
            
            onCloseModal();
            fetchPrdData(); // Refresh the table
        } catch (error) {
            console.error('Error submitting PRD:', error);
            message.error('Failed to submit PRD');
        }
    };

    const handleDelete = async (prd: PrdData) => {
        try {
            await deletePrd(prd.ID);
            message.success('PRD deleted successfully');
            // Note: Backend automatically logs the deletion operation
            
            fetchPrdData(); // Refresh the table
        } catch (error) {
            console.error('Error deleting PRD:', error);
            message.error('Failed to delete PRD');
        }
    };

    const handleEdit = (prd: PrdData) => {
        showModal(prd);
    };

    return (
        <div style={{ padding: 24 }}>
            <div style={{display: "flex"}}>
              <h1 style={{"marginTop": 0}}>PRD FORM</h1>
              <Button style={{ marginLeft: "auto" }} onClick={() => signOut()}>Sign Out</Button>
            </div>
            <div>
              <Button style={{ marginRight: '10px' }} onClick={() => navigate('/dashboard')}>View Dashboard</Button>
              <Button onClick={() => navigate('/featureLogs')}>View Logs</Button>
            </div>
            <Row justify="end" style={{marginBottom: "10px"}}>
              <Button title="Add new PRD" onClick={() => showModal()}>Add New PRD</Button>
            </Row>
            <Modal
              title={isEdit ? "Edit PRD" : "Create a new PRD"}
              width={720}
              open={openModal}
              onCancel={onCloseModal}
              onOk={handleSubmit}
              okText={isEdit ? "Update" : "Submit"}
              styles={{
              body: {
                  paddingBottom: 80,
              },
              }}>
                <ModalForm 
                    form={form} 
                    isEdit={isEdit} 
                    initialValues={currentPrd || {}}
                />
            </Modal>
            <Table 
                columns={tableCol(handleEdit, handleDelete)}
                dataSource={prdData}
                rowKey="ID"
                loading={loading}
            />
        </div>
    )
}