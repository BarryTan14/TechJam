import { Table, Button, Popconfirm, Row, Modal, Form, Input, message, Radio, Space, Upload } from "antd";
import { DeleteOutlined, EditOutlined, UploadOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from "react";
import { fetchPrd, createPrd, createPrdFromFile, deletePrd, updatePrd } from "./api";
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
        <Button style={{ marginRight: "3px" }} onClick={() => { window.location.href = `./dashboard?prdId=${record.ID}` }}>
          View Dashboard
        </Button>
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
    inputType: 'text' | 'file';
    onInputTypeChange: (type: 'text' | 'file') => void;
    fileList: any[];
    onFileChange: (info: any) => void;
}

const ModalForm: React.FC<ModalFormProps> = ({ 
    form, 
    isEdit = false, 
    initialValues = {}, 
    inputType,
    onInputTypeChange,
    fileList,
    onFileChange
}) => {
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
          
          <Form.Item label="Input Type">
            <Radio.Group value={inputType} onChange={(e) => onInputTypeChange(e.target.value)}>
              <Space direction="vertical">
                <Radio value="text">Text Input</Radio>
                <Radio value="file">File Upload</Radio>
              </Space>
            </Radio.Group>
          </Form.Item>
          
          {inputType === 'text' ? (
            <>
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
            </>
          ) : (
            <Form.Item
              name="file"
              label="Upload File"
              rules={[{ required: true, message: 'Please upload a file!' }]}
            >
              <Upload
                beforeUpload={() => false} // Prevent auto upload
                fileList={fileList}
                onChange={onFileChange}
                accept=".txt,.md,.doc,.docx"
                maxCount={1}
              >
                <Button icon={<UploadOutlined />}>Click to Upload</Button>
              </Upload>
            </Form.Item>
          )}
          
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
  const [data, setData] = useState([]);

  if (!localStorage.getItem("username")) {
    window.location.href = "./login";
    return null;
  }

    const navigate = useNavigate();
    const [openModal, setOpenModal] = useState(false);
    const [isEdit, setIsEdit] = useState(false);
    const [currentPrd, setCurrentPrd] = useState<PrdData | null>(null);
    const [prdData, setPrdData] = useState<PrdData[]>([]);
    const [loading, setLoading] = useState(false);
    const [form] = Form.useForm();
    const [inputType, setInputType] = useState<'text' | 'file'>('text');
    const [fileList, setFileList] = useState<any[]>([]);

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
            setInputType('text'); // Edit mode only supports text
            form.setFieldsValue({
                Name: prd.Name,
                Description: prd.Description,
                Status: "Draft"
            });
        } else {
            setIsEdit(false);
            setCurrentPrd(null);
            setInputType('text');
            setFileList([]);
            form.resetFields();
        }
        setOpenModal(true);
    };

    const handleFileChange = (info: any) => {
        setFileList(info.fileList);
    };

    const handleInputTypeChange = (type: 'text' | 'file') => {
        setInputType(type);
        if (type === 'text') {
            setFileList([]);
        }
    };

  const onCloseModal = () => {
      form.resetFields();
      setCurrentPrd(null);
      setOpenModal(false);
      setIsEdit(false);
    setOpenModal(false);
        setIsEdit(false);
        setCurrentPrd(null);
        setInputType('text');
        setFileList([]);
        form.resetFields();
    };

    const handleSubmit = async () => {
        try {
            const values = await form.validateFields();
            
            if (isEdit && currentPrd) {
                // Update existing PRD (only supports text)
                await updatePrd(currentPrd.ID, values);
                message.success('PRD updated successfully');
                // Note: Backend automatically logs the update operation
            } else {
                // Create new PRD
                if (inputType === 'file') {
                    // Handle file upload
                    if (fileList.length === 0) {
                        message.error('Please upload a file');
                        return;
                    }
                    
                    const formData = new FormData();
                    formData.append('Name', values.Name);
                    formData.append('Status', values.Status || 'Draft');
                    formData.append('file', fileList[0].originFileObj);
                    
                    const response = await createPrdFromFile(formData);
                    message.success('PRD created successfully from file');
                } else {
                    // Handle text input
                    const response = await createPrd(values);
                    message.success('PRD created successfully');
                }
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
    // setEditRecord(null);
  };



    return (
        <div style={{ padding: 24 }}>
            <div style={{display: "flex"}}>
              <h1 style={{"marginTop": 0}}>PRD FORM</h1>
              <Button style={{ marginLeft: "auto" }} onClick={() => signOut()}>Sign Out</Button>
            </div>
            <div>
              {/* <Button style={{ marginRight: '10px' }} onClick={() => navigate('/dashboard')}>View Dashboard</Button> */}
              {/*<Button onClick={() => navigate('/featureLogs')}>View Logs</Button>*/}
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
                    
                    inputType={inputType}
                    onInputTypeChange={handleInputTypeChange}
                    fileList={fileList}
                    onFileChange={handleFileChange}
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
