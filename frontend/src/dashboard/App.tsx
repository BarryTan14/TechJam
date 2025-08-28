import { Card, Row, Col, Table, Input, Collapse, CollapseProps, Button, Divider } from 'antd';
import { ResponsiveChoropleth } from '@nivo/geo'
import countries from '../world_countries.json'
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const CollapsableFilter = () => {
    const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([])

    // Selection handler
    const rowSelection = {
        selectedRowKeys,
        onChange: (newSelectedRowKeys: React.Key[], selectedRows: any[]) => {
            setSelectedRowKeys(newSelectedRowKeys);
        },
    };

    const collapseItems: CollapseProps['items'] = [
    {
        key: '1',
        label: 'Features',
        children: 
        <>
            <Table 
                columns={[{
                    title: "Features",
                    dataIndex: "name"
                }]}
                dataSource={[{
                    "name": "Feature 1"
                }]}
                rowSelection={rowSelection}
            />
            <Input placeholder='Input Feature ID'/>
        </>,
    },
    {
        key: '2',
        label: 'Region',
        children: <></>,
    },
    {
        key: '3',
        label: 'Status',
        children: <></>,
    },
    {
        key: '4',
        label: 'Others',
        children: <></>,
    },
    ];

    return (
        <Collapse items={collapseItems} defaultActiveKey={['1']} />
    )
}


const sampleHeatMapData = 
    [
        {
            "id": "USA",
            "value": 863184
        },
        {
            "id": "Alaska",
            "value": 50000
        },
        {
            "id": "Hawaii",
            "value": 450000
        }
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
            <Row className="mt-2" justify="space-evenly">
                <Col span={5}>
                    <Card title="Filtering">
                        <CollapsableFilter />
                    </Card>
                </Col>
                <Col span={12}>
                    <Card>
                        <div style={{ height: 400 }}>
                        <ResponsiveChoropleth /* or Choropleth for fixed dimensions */
                            data={sampleHeatMapData}
                            features={countries.features}
                            margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
                            colors="nivo"
                            domain={[0, 1000000]}
                            unknownColor="#666666"
                            label="properties.name"
                            valueFormat=".2s"
                            enableGraticule={true}
                            graticuleLineColor="#dddddd"
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
                            projectionScale={255}
                            projectionTranslation={[1.48, 1.15]}
                        />
                        </div>
                        <p
                        style={{
                            border: '0.5px solid #333',
                            borderRadius: '8px',
                            padding: '8px',
                            maxWidth: '100%',
                            backgroundColor: '#f9f9f9',
                            boxShadow: '1px 1px 2px rgba(0,0,0,0.1)',
                        }}>
                            Analysis HERE
                        </p>
                    </Card>
                </Col>
                <Col span={5}>
                    <Card>
                        <h3>PRD</h3>
                        <Divider></Divider>
                        <p
                        style={{
                            border: '0.5px solid #333',
                            borderRadius: '8px',
                            padding: '8px',
                            maxWidth: '100%',
                            backgroundColor: '#f9f9f9',
                            boxShadow: '1px 1px 2px rgba(0,0,0,0.1)',
                        }}>
                            PRD description HERE
                        </p>
                        <div style={{marginTop:"50px", marginBottom:"50px"}}></div>
                        <h3>Feature</h3>
                        <Divider></Divider>
                        <p
                        style={{
                            border: '0.5px solid #333',
                            borderRadius: '8px',
                            padding: '8px',
                            maxWidth: '100%',
                            backgroundColor: '#f9f9f9',
                            boxShadow: '1px 1px 2px rgba(0,0,0,0.1)',
                        }}>
                            Feature description HERE
                        </p>
                    </Card>
                </Col>
            </Row>
            
        </div>
    );
}
