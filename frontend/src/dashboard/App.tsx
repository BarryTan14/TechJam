import { Card, Row, Col, Button, Select } from 'antd';
import { ResponsiveChoropleth } from '@nivo/geo'
import countries from '../usa_states.json'
import { useNavigate } from 'react-router-dom';

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
            "value": 50000
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

    const navigate = useNavigate();

    return (
        <div style={{ padding: 24 }}>
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
                    <Card title="PRD" style={{marginBottom: "10px"}}>
                        <span> STH STH STH </span>
                    </Card>
                    <Card title="Feature" style={{marginBottom: "10px"}}>
                       <Select
                        style={{ width: 120 }}
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
                    <Card>
                        <div style={{ minHeight: 400 }}>
                        <ResponsiveChoropleth /* or Choropleth for fixed dimensions */
                            data={sampleHeatMapData}
                            features={countries.features}
                            margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
                            colors="nivo"
                            domain={[0, 1000000]}
                            unknownColor="#666666"
                            label="properties.name"
                            valueFormat=".2s"
                            // enableGraticule={true}
                            // graticuleLineColor="#dddddd"
                            borderWidth={0.5}
                            borderColor="#152538"
                            legends={[
                                {
                                    anchor: 'bottom-left',
                                    direction: 'column',
                                    justify: true,
                                    translateX: 20,
                                    translateY: -100,
                                    itemsSpacing: 0,
                                    itemWidth: 94,
                                    itemHeight: 18,
                                    itemDirection: 'left-to-right',
                                    itemTextColor: '#444444',
                                    itemOpacity: 0.85,
                                    symbolSize: 18
                                }
                            ]}
                            projectionScale={260}
                            projectionTranslation={[1.4, 1.2]}
                        />
                        </div>
                    </Card>
                </Col>
                <Col span={5}>
                    <Card style={{marginBottom: "10px"}} title="Analysis">
                        <p>
                            Analysis HERE
                        </p>
                        <div style={{ display: "flex", justifyContent: "center", gap: "16px", marginTop: "5px" }} >
                            <Button style={{marginRight:"10px"}}>Upload</Button>
                        </div>
                    </Card>
                    <Card title="Recommendation">
                        <p>
                            Recommendation HERE
                        </p>
                        <div style={{ display: "flex", justifyContent: "center", gap: "16px", marginTop: "5px"}} >
                            <Button style={{marginRight:"10px"}}>Approve</Button><Button>Reject</Button>
                        </div>
                    </Card>
                </Col>
            </Row>
            
        </div>
    );
}
