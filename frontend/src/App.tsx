import { Table, Button, Popconfirm, Row, Modal, Form, Input, Descriptions } from "antd";
import { DeleteOutlined, EditOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from "react";
import sampleData from "./sampleData.json"

const { TextArea } = Input;

const tableCol = (onEditDetail: (detail: any) => void, onDelete: (detail: any) => void) => [
  {
    title: "ID",
    dataIndex: "prd_id",
    key: "prd_id",
  },
  {
    title: "Name",
    dataIndex: "prd_name",
    key: "prd_name",
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
        <Button style={{ marginRight: "3px" }} onClick={() => { window.location.href = "./dashboard" }}>
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
];

const ModalForm = ({ visible, onCancel, onSubmit, initialValues }: any) => {
  const [form] = Form.useForm();

  useEffect(() => {
    if (visible) {
      form.setFieldsValue(initialValues);
    }
  }, [visible, initialValues, form]);

  const handleFinish = (values: any) => {
    onSubmit(values);
  };

  return (
    <Modal
      title={initialValues && initialValues.id ? "Edit PRD" : "Create a new PRD"}
      visible={visible}
      onCancel={onCancel}
      onOk={() => form.submit()}
      okText="Submit"
      width={720}
      bodyStyle={{ paddingBottom: 80 }}
    >
      <Form
        layout="vertical"
        form={form}
        onFinish={handleFinish}
      >
        <Form.Item
          name="id"
          label="ID"
          hidden
        >
          <Input readOnly />
        </Form.Item>
        <Form.Item
          name="name"
          label="Name"
          rules={[{ required: true, message: 'Please enter the name of PRD' }]}
        >
          <Input placeholder="Enter name of PRD" />
        </Form.Item>
        <Form.Item
          name="description"
          label="Description"
          rules={[{ required: true, message: 'Please enter description' }]}
        >
          <TextArea placeholder="Please enter description" />
        </Form.Item>
        <Button>Upload</Button>
      </Form>
    </Modal>
  );
};

export default function App() {
  const navigate = useNavigate();
  const [openModal, setOpenModal] = useState(false);
  const [editRecord, setEditRecord] = useState<any>(null);
  const [data, setData] = useState([sampleData.prd_info]);

  if (!localStorage.getItem("username")) {
    window.location.href = "./login";
    return null;
  }

  const showModal = () => {
    setOpenModal(true);
  };

  const onCloseModal = () => {
    setOpenModal(false);
    setEditRecord(null);
  };

  const onEditDetail = (record: any) => {
    setEditRecord(record);
    setOpenModal(true);
  };

  const onDelete = (record: any) => {
    setData((current: any[]) => current.filter(item => item.id !== record.id));
  };

  const onModalSubmit = (values: any) => {
    if (values.id) {
      // Edit existing record
      setData((current: any[]) => current.map(item => item.id === values.id ? values : item));
    } else {
      // Add new record - assign new id, and remove any id in values to prevent clash
      const newId = data.length > 0 ? Math.max(...data.map(d => parseInt(d.prd_id))) + 1 : 1;
      const newEntry = { ...values, id: newId, status: "Pending" };
      setData((current: any) => [...current, newEntry]);
    }
    onCloseModal();
  };

  return (
    <div style={{ padding: 24 }}>
      <div style={{ display: "flex" }}>
        <h1 style={{ marginTop: 0 }}>PRD FORM</h1>
        <Button style={{ marginLeft: "auto" }} onClick={() => {
          localStorage.removeItem("username");
          window.location.href = "../login";
        }}>Sign Out</Button>
      </div>
      <div>
        <Button onClick={() => navigate('/featureLogs')}>View Logs</Button>
      </div>
      <Row justify="end" style={{ marginBottom: "10px" }}>
        <Button title="Add new PRD" onClick={() => {
          setEditRecord(null);
          showModal();
        }}>Add New PRD</Button>
      </Row>
      <ModalForm
        visible={openModal}
        onCancel={onCloseModal}
        onSubmit={onModalSubmit}
        initialValues={editRecord || { name: '', description: '' }}
      />
      <Table
        columns={tableCol(onEditDetail, onDelete)}
        dataSource={data}
        rowKey="prd_id"
      />
    </div>
  );
}
