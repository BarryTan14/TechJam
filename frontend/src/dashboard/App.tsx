import { Card, Row, Col, Button, Select, Modal } from 'antd';
import { ResponsiveChoropleth } from '@nivo/geo'
import countries from '../usa_states.json'
import { useNavigate } from 'react-router-dom';
import { SetStateAction, useState } from 'react';

const options = [
    {
        value: 'jack',
        label: (
                <span>Feature 1</span>
        ),
    },
]

const sampleHeatMapData = 
    [
        {
            "id": "AK",
            "value": 0.5,
        },
        {
            "id": "NY",
            "value": 1,
        },
        {
            "id": "CA",
            "value": 0,
        },
    ]

const signOut = () => {
  localStorage.removeItem("username")
  window.location.href = "../login" 
}

export default function Dashboard() {
    if (!localStorage.getItem("username")) {
      window.location.href = "./login"
      return
    }

    const [openModal, setOpenModal] = useState(false);
    const [buttonValue, setButtonValue] = useState("")

    const showModal = (value: SetStateAction<string>) => {
        setOpenModal(true);
        setButtonValue(value)
    };

    const onCloseModal = () => {
        setOpenModal(false);
        setButtonValue("")
    };

    const navigate = useNavigate();

    return (
        <div style={{ padding: 20 }}>
            <div style={{display: "flex"}}>
                <h1 style={{"marginTop": 0}}>DASHBOARD</h1>
                <Button style={{ marginLeft: "auto" }} onClick={() => signOut()}>Sign Out</Button>
            </div>
            <div style={{marginBottom: "20px"}}>
              <Button style={{ marginRight: '10px' }} onClick={() => navigate('/')}>Go to PRD Form</Button>
              <Button onClick={() => navigate('/featureLogs')}>View Logs</Button>
            </div>
            <Row justify="space-evenly">
                <Col span={5}>
                    <Card title="PRD" style={{marginBottom: "10px", maxHeight: "40%", overflowY: "scroll"}}>
                        <span> STH STH STH </span>
                        <div style={{ display: "flex", justifyContent: "center", gap: "16px", marginTop: "5px" }} >
                            <Button style={{marginRight:"10px"}}>Upload</Button>
                        </div>
                    </Card>
                    <Card title="Feature" style={{marginBottom: "10px", maxHeight: "40%", overflowY: "scroll"}}>
                       <Select
                        style={{ width: "100%", marginBottom: "10px" }}
                        onChange={() => {}}
                        options={options}
                        />
                        <span style={{ display: "block" }}>Name: {}</span>
                        <span style={{ display: "block" }}>Description: {}</span>
                        <span style={{ display: "block" }}>Status: {}</span>
                        <span style={{ display: "block" }}>Latest Update: {}</span>
                    </Card>
                </Col>
                <Col span={12}>
                    <Card title="UNITED STATES OF AMERICA" headStyle={{ textAlign: 'center' }}>
                        <div style={{ height: 365 }}>
                        <ResponsiveChoropleth /* or Choropleth for fixed dimensions */
                            data={sampleHeatMapData}
                            features={countries.features}
                            colors={['#008000', '#FFA500', '#FF0000']}
                            domain={[0, 1]}
                            unknownColor="#666666"
                            label="properties.name"
                            valueFormat=".2s"
                            borderWidth={0.5}
                            borderColor="#152538"
                            projectionScale={515}
                            projectionTranslation={[2.1, 1.4]}
                        />
                            <div style={{ position: 'absolute', right: 10, bottom: 10, background: 'white', padding: 10, borderRadius: 6 }}>
                                <div style={{ display: 'flex', alignItems: 'center', marginBottom: 4 }}>
                                <div style={{ width: 15, height: 15, background: '#FF0000', marginRight: 8 }}></div>
                                    <span>High</span>
                                </div>
                                <div style={{ display: 'flex', alignItems: 'center', marginBottom: 4 }}>
                                <div style={{ width: 15, height: 15, background: '#FFA500', marginRight: 8 }}></div>
                                    <span>Medium</span>
                                </div>
                                <div style={{ display: 'flex', alignItems: 'center' }}>
                                <div style={{ width: 15, height: 15, background: '#008000', marginRight: 8 }}></div>
                                    <span>Low</span>
                                </div>
                            </div>
                        </div>
                    </Card>
                </Col>
                <Col span={5}>
                    <Card style={{marginBottom: "10px", maxHeight: "40%", overflowY: "scroll"}} title="Analysis">
                        <p>
                            Analysis HERE<br />Analysis HERE<br />Analysis HERE<br />Analysis HERE<br />Analysis HERE<br />Analysis HERE<br />Analysis HERE<br />Analysis HERE<br />Analysis HERE<br />Analysis HERE
                        </p>
                    </Card>
                    <Card style={{maxHeight: "40%", overflowY: "scroll"}} title="Recommendation">
                        <p>
                            Recommendation HERE
                        </p>
                        <div style={{ display: "flex", justifyContent: "center", gap: "16px", marginTop: "5px"}} >
                            <Button style={{marginRight:"10px"}} onClick={() => showModal('approve')}>Approve</Button><Button onClick={() => showModal('reject')} >Reject</Button>
                        </div>
                        <Modal
                            title="Recommendation(s)"
                            onCancel={onCloseModal}
                            onOk={onCloseModal}
                            visible={openModal}
                        >
                            <p>
                                Feature Name: {} <br />
                                Agent: {} <br />
                                Reason of {buttonValue === 'approve' ? 'approval' : "rejection"}: {} <br />
                                Evidence (optional): <Button>Upload</Button>
                            </p>
                        </Modal>
                    </Card>
                </Col>
            </Row>   
        </div>
    );
}
