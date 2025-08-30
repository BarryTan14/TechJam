import { Card, Row, Col, Button, Select, Modal, Spin, message } from 'antd';
import { ResponsiveChoropleth } from '@nivo/geo'
import countries from '../usa_states.json'
import { useNavigate, useSearchParams } from 'react-router-dom';
import { SetStateAction, useState, useEffect } from 'react';
import { fetchDashboardData } from '../api';

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

    const [searchParams] = useSearchParams();
    const prdId = searchParams.get('prdId');
    
    const [openModal, setOpenModal] = useState(false);
    const [buttonValue, setButtonValue] = useState("");
    const [loading, setLoading] = useState(true);
    const [dashboardData, setDashboardData] = useState<any>(null);
    const [selectedFeature, setSelectedFeature] = useState<any>(null);
    const [featureOptions, setFeatureOptions] = useState<any[]>([]);

    const showModal = (value: SetStateAction<string>) => {
        setOpenModal(true);
        setButtonValue(value)
    };

    const onCloseModal = () => {
        setOpenModal(false);
        setButtonValue("")
    };

    const navigate = useNavigate();

    // Fetch dashboard data when component mounts
    useEffect(() => {
        const fetchData = async () => {
            if (!prdId) {
                message.error('No PRD ID provided');
                setLoading(false);
                return;
            }

            try {
                setLoading(true);
                const response = await fetchDashboardData(prdId);
                const data = response.data;
                console.log(data)
                setDashboardData(data);
                
                // Prepare feature options for the select dropdown
                const options = data.features.map((feature: any) => ({
                    value: feature.uuid,
                    label: feature.data.feature_name || 'Unknown Feature'
                }));
                setFeatureOptions(options);
                
                // Set first feature as selected by default
                if (data.features.length > 0) {
                    setSelectedFeature(data.features[0]);
                }
                
                setLoading(false);
            } catch (error) {
                console.error('Error fetching dashboard data:', error);
                message.error('Failed to load dashboard data');
                setLoading(false);
            }
        };

        fetchData();
    }, [prdId]);

    if (loading) {
        return (
            <div style={{ padding: 20, textAlign: 'center' }}>
                <Spin size="large" />
                <p>Loading dashboard data...</p>
            </div>
        );
    }

    if (!dashboardData) {
        return (
            <div style={{ padding: 20, textAlign: 'center' }}>
                <p>No dashboard data available</p>
                <Button onClick={() => navigate('/')}>Go Back</Button>
            </div>
        );
    }

    return (
        <div style={{ padding: 20 }}>
            <div style={{display: "flex"}}>
                <h1 style={{"marginTop": 0}}>DASHBOARD - {dashboardData.prd?.Name || 'Unknown PRD'}</h1>
                <Button style={{ marginLeft: "auto" }} onClick={() => signOut()}>Sign Out</Button>
            </div>
            <div style={{marginBottom: "20px"}}>
              <Button style={{ marginRight: '10px' }} onClick={() => navigate('/')}>Go to PRD Form</Button>
              <Button onClick={() => navigate('/featureLogs')}>View Logs</Button>
            </div>
            <Row justify="space-evenly">
                <Col span={5}>
                    <Card title="PRD" style={{marginBottom: "10px", maxHeight: "40%", overflowY: "scroll"}}>
                        <div>
                            <p><strong>Name:</strong> {dashboardData.prd?.Name || 'N/A'}</p>
                            <p><strong>Description:</strong> {dashboardData.prd?.Description || 'N/A'}</p>
                            <p><strong>Status:</strong> {dashboardData.prd?.Status || 'N/A'}</p>
                            <p><strong>Created:</strong> {dashboardData.prd?.created_at ? new Date(dashboardData.prd.created_at).toLocaleDateString() : 'N/A'}</p>
                            <p><strong>Total Features:</strong> {dashboardData.total_features || 0}</p>
                            <p><strong>High Risk:</strong> {dashboardData.features_with_high_risk || 0}</p>
                            <p><strong>Medium Risk:</strong> {dashboardData.features_with_medium_risk || 0}</p>
                            <p><strong>Low Risk:</strong> {dashboardData.features_with_low_risk || 0}</p>
                        </div>
                        <div style={{ display: "flex", justifyContent: "center", gap: "16px", marginTop: "5px" }} >
                            <Button style={{marginRight:"10px"}}>Upload</Button>
                        </div>
                    </Card>
                    <Card title="Feature" style={{marginBottom: "10px", maxHeight: "40%", overflowY: "scroll"}}>
                       <Select
                        style={{ width: "100%", marginBottom: "10px" }}
                        onChange={(value) => {
                            const feature = dashboardData.features.find((f: any) => f.uuid === value);
                            setSelectedFeature(feature);
                        }}
                        options={featureOptions}
                        placeholder="Select a feature"
                        />
                        {selectedFeature && (
                            <div>
                                <span style={{ display: "block" }}><strong>Name:</strong> {selectedFeature.data.feature_name || 'N/A'}</span>
                                <span style={{ display: "block" }}><strong>Description:</strong> {selectedFeature.data.feature_description || 'N/A'}</span>
                                <span style={{ display: "block" }}><strong>Priority:</strong> {selectedFeature.data.priority || 'N/A'}</span>
                                <span style={{ display: "block" }}><strong>Complexity:</strong> {selectedFeature.data.complexity || 'N/A'}</span>
                                <span style={{ display: "block" }}><strong>Risk Level:</strong> {selectedFeature.data.risk_level || 'N/A'}</span>
                                <span style={{ display: "block" }}><strong>Confidence:</strong> {selectedFeature.data.confidence_score ? `${(selectedFeature.data.confidence_score * 100).toFixed(1)}%` : 'N/A'}</span>
                                <span style={{ display: "block" }}><strong>Latest Update:</strong> {selectedFeature.updated_at ? new Date(selectedFeature.updated_at).toLocaleDateString() : 'N/A'}</span>
                            </div>
                        )}
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
                        {selectedFeature ? (
                            <div>
                                <p><strong>Risk Level:</strong> {selectedFeature.data.risk_level?.toUpperCase() || 'N/A'}</p>
                                <p><strong>Confidence Score:</strong> {selectedFeature.data.confidence_score ? `${(selectedFeature.data.confidence_score * 100).toFixed(1)}%` : 'N/A'}</p>
                                <p><strong>Compliance Flags:</strong></p>
                                <ul>
                                    {selectedFeature.data.compliance_flags?.map((flag: string, index: number) => (
                                        <li key={index}>{flag}</li>
                                    )) || <li>None</li>}
                                </ul>
                                <p><strong>Non-Compliant States:</strong> {selectedFeature.data.non_compliant_states?.length || 0} states</p>
                                <p><strong>Processing Time:</strong> {selectedFeature.data.processing_time ? `${selectedFeature.data.processing_time.toFixed(2)}s` : 'N/A'}</p>
                            </div>
                        ) : (
                            <p>Select a feature to view analysis</p>
                        )}
                    </Card>
                    <Card style={{marginBottom: "10px", maxHeight: "40%", overflowY: "scroll"}} title="Executive Report">
                        {dashboardData.prd?.executive_report ? (
                            <div>
                                <p><strong>Report ID:</strong> {dashboardData.prd.executive_report.report_id || 'N/A'}</p>
                                <p><strong>Generated:</strong> {dashboardData.prd.executive_report.generated_at ? new Date(dashboardData.prd.executive_report.generated_at).toLocaleString() : 'N/A'}</p>
                                <div style={{ marginTop: '10px' }}>
                                    <p><strong>Executive Summary:</strong></p>
                                    <div style={{ 
                                        fontSize: '12px', 
                                        maxHeight: '150px', 
                                        overflowY: 'auto', 
                                        border: '1px solid #d9d9d9', 
                                        padding: '8px', 
                                        borderRadius: '4px',
                                        backgroundColor: '#fafafa'
                                    }}>
                                        {dashboardData.prd.executive_report.executive_summary || 'No summary available'}
                                    </div>
                                </div>
                                <div style={{ marginTop: '10px' }}>
                                    <p><strong>Key Findings:</strong></p>
                                    <ul style={{ fontSize: '11px', marginLeft: '15px' }}>
                                        {dashboardData.prd.executive_report.key_findings?.slice(0, 3).map((finding: string, index: number) => (
                                            <li key={index}>{finding}</li>
                                        )) || <li>No findings available</li>}
                                    </ul>
                                </div>
                                <div style={{ marginTop: '10px' }}>
                                    <p><strong>Next Steps:</strong></p>
                                    <ul style={{ fontSize: '11px', marginLeft: '15px' }}>
                                        {dashboardData.prd.executive_report.next_steps?.slice(0, 2).map((step: string, index: number) => (
                                            <li key={index}>{step}</li>
                                        )) || <li>No next steps available</li>}
                                    </ul>
                                </div>
                            </div>
                        ) : (
                            <p>No executive report available</p>
                        )}
                    </Card>
                    <Card style={{maxHeight: "40%", overflowY: "scroll"}} title="Recommendation">
                        {selectedFeature ? (
                            <div>
                                <p><strong>Recommendations:</strong></p>
                                <ul>
                                    {selectedFeature.data.recommendations?.slice(0, 3).map((rec: string, index: number) => (
                                        <li key={index} style={{ fontSize: '12px', marginBottom: '5px' }}>{rec}</li>
                                    )) || <li>No recommendations available</li>}
                                </ul>
                                <div style={{ display: "flex", justifyContent: "center", gap: "16px", marginTop: "5px"}} >
                                    <Button style={{marginRight:"10px"}} onClick={() => showModal('approve')}>Approve</Button><Button onClick={() => showModal('reject')} >Reject</Button>
                                </div>
                            </div>
                        ) : (
                            <p>Select a feature to view recommendations</p>
                        )}
                        <Modal
                            title="Recommendation(s)"
                            onCancel={onCloseModal}
                            onOk={onCloseModal}
                            open={openModal}
                        >
                            <p>
                                Feature Name: {selectedFeature?.data.feature_name || 'N/A'} <br />
                                Agent: LangGraph Analysis <br />
                                Reason of {buttonValue === 'approve' ? 'approval' : "rejection"}: {selectedFeature?.data.reasoning || 'N/A'} <br />
                                Evidence (optional): <Button>Upload</Button>
                            </p>
                        </Modal>
                    </Card>
                </Col>
            </Row>   
        </div>
    );
}
