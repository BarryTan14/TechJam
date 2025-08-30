import { Card, Row, Col, Button, Select, Modal, Spin, message, Collapse, CollapseProps } from 'antd';
import { ResponsiveChoropleth } from '@nivo/geo'
import countries from '../usa_states.json'
import { useNavigate, useSearchParams } from 'react-router-dom';
import { SetStateAction, useState, useEffect, Key } from 'react';
import { fetchDashboardData } from '../api';
import { CheckCircleOutlined, GlobalOutlined, WarningOutlined } from '@ant-design/icons'

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
    const [allFeatues, setAllFeatures] = useState<any[]>([])
    const [mapData, setMapData] = useState<any[]>([])
    const [openStateModal, setOpenStateModal] = useState(false)
    const [stateModalData, setStateModalData] = useState(null)


    const showModal = (value: SetStateAction<string>) => {
        setOpenModal(true);
        setButtonValue(value)
    };

    const onCloseModal = () => {
        setOpenModal(false);
        setButtonValue("")
    };

    const showStateModal = (feature: any) => {
        setOpenStateModal(true)
        setStateModalData(feature)
    }

    const closeStateModal = () => {
        setOpenStateModal(false)
    }

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
                setLoading(false);
            } catch (error) {
                console.error('Error fetching dashboard data:', error);
                message.error('Failed to load dashboard data');
                setLoading(false);
            }
        };

        fetchData();
    }, [prdId]);

    useEffect(() => {
        if (dashboardData?.prd?.langgraph_analysis?.feature_compliance_results) {
            setAllFeatures(dashboardData.prd.langgraph_analysis.feature_compliance_results)
            const options = dashboardData.prd.langgraph_analysis.feature_compliance_results.map((item: { feature: { feature_id: any; feature_name: any; priority: any}; }) => ({
                value: item.feature.feature_id,
                label: item.feature.feature_name || 'Unknown Feature',
                priority: item.feature.priority,
            }));
            
            setFeatureOptions(options);
            setSelectedFeature(dashboardData.prd.langgraph_analysis.feature_compliance_results[0])
        }
    }, [dashboardData])

    useEffect(() => {
        if (selectedFeature) {
            setMapData([])
            const stateComplianceScore = selectedFeature.state_compliance_scores
            const list = Object.values(stateComplianceScore).map((state) => ({
                id: state.state_code,
                value: state.compliance_score > 0.4 ? 1 : 0
            }));
            setMapData(list)
        }
    }, [selectedFeature])

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

    const featureOptionsWithCircles = featureOptions.map(option => ({
        value: option.value,
        label: (
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <span
                style={{
                display: 'inline-block',
                width: 12,
                height: 12,
                borderRadius: '50%',
                backgroundColor: 
                Object.values(selectedFeature.state_compliance_scores).map((state) => ({
                    id: state.state_code,
                    value: state.compliance_score > 0.4 ? 1 : 0
                })).filter(state => state.value > 0.4).length > 0  ? 'red' :
                Object.values(selectedFeature.state_compliance_scores).map((state) => ({
                    id: state.state_code,
                    value: state.compliance_score > 0.4 ? 1 : 0
                })).filter(state => state.value <= 0.4).length > 0  ? 'green' : "grey", // default color for undefined priority
                }}
            />
            <span>{option.label}</span>
            </div>
        ),
    }));

    const items: CollapseProps['items'] = [
    {
        key: '1',
        label: <span style={{color: '#800080'}}>Social Friction</span>,
        children: <p style={{color: '#800080'}}>More Info</p>,
    },
    ];

  return (
    <div style={{ padding: 20 }}>
      <div style={{ display: "flex", alignItems: "center", maxWidth: "100%" }}>
        <h1 style={{ marginTop: 0, maxWidth: "75%", fontSize: "28px" }}>
            DASHBOARD
        </h1>
        <div style={{ marginLeft: "auto", display: "flex", gap: "3px" }}>
            <Button onClick={() => navigate('/')}>Go to PRD Form</Button>
            <Button onClick={() => signOut()}>Sign Out</Button>
        </div>
      </div>

      <Row style={{marginBottom:"10px"}}>
        <Card title={dashboardData.prd?.Name && <span>PRD - {dashboardData.prd?.Name}</span>} style={{ marginBottom: "10px", flex: 1 }} bodyStyle={{ paddingBottom: "0px", paddingTop: "7px" }} >
        <Row style={{fontWeight:500}} justify="space-evenly">
            <Col span={18}>
                <p><strong>Description:</strong> {dashboardData.prd?.Description || 'N/A'}</p>
            </Col>
            <Col span={6} style={{marginTop: 6, justifyItems:"end"}}>
                <Button style={{ marginRight: 1 }} onClick={() => navigate(`/featureLogs?prdId=${prdId}`)}>View Logs</Button>
                <Button>Download</Button>
            </Col>
        </Row>
        </Card>
      </Row>

      <Row justify="space-evenly" style={{ display: 'flex', alignItems: 'stretch' }}>
        <Col span={11} style={{ display: 'flex', flexDirection: 'column' }}>
            <Card
            title="HEATMAP"
            headStyle={{ textAlign: 'center' }}
            bodyStyle={{ position: 'relative', overflow: 'hidden' }}
            style={{ marginBottom: "10px", flex: 1}}
          >
            {/* Make the parent positioned so the legend anchors to it */}
            <div style={{ height: 365, position: 'relative', cursor: "pointer" }}>
              <ResponsiveChoropleth
                data={mapData}
                features={countries.features}
                colors={['#008000','#FF0000']}
                domain={[0, 1]}
                unknownColor="#666666"
                label="properties.name"
                // valueFormat=".2s"
                borderWidth={0.5}
                borderColor="#152538"

                /* IMPORTANT: keep the projection centered and stable */
                // projectionCenter={[-98, 38]}           // approx center of contiguous US
                projectionTranslation={[0.5, 0.5]}    // center within the SVG viewBox
                projectionScale={440}                  // tuned for ~365px tall container

                margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
                enableGraticule={false}
                tooltip={({ feature }) => {
                    if (!feature) return null;
                    const { properties, data } = feature;
                    return (
                    <div
                        style={{
                        background: 'white',
                        padding: '6px 9px',
                        border: '1px solid #ccc',
                        borderRadius: 3,
                        }}
                    >
                        <strong>{properties?.name || 'Unknown State'}</strong>
                        <br />
                        Score: {data?.value != null ? data.value : 'N/A'}
                    </div>
                    );
                }}
                onClick={(feature) => {showStateModal(feature)}}
              />

              {/* Legend pinned to the map container (not the page) */}
              <div
                style={{
                  position: 'absolute',
                  right: 10,
                  bottom: 10,
                  background: 'white',
                  padding: 10,
                  borderRadius: 6,
                  boxShadow: '0 1px 4px rgba(0,0,0,0.1)'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', marginBottom: 4 }}>
                  <div style={{ width: 15, height: 15, background: '#FF0000', marginRight: 8 }}></div>
                  <span>High</span>
                </div>
                {/* <div style={{ display: 'flex', alignItems: 'center', marginBottom: 4 }}>
                  <div style={{ width: 15, height: 15, background: '#ffa600ff', marginRight: 8 }}></div>
                  <span>Medium</span>
                </div> */}
                <div style={{ display: 'flex', alignItems: 'center' }}>
                  <div style={{ width: 15, height: 15, background: '#008000', marginRight: 8 }}></div>
                  <span>Low</span>
                </div>
              </div>
            </div>
            <Card style={{ marginBottom: "10px", overflowY: "scroll", flex: 1 }}>
                <>
                    <div>
                        Feature:{" "} 
                        <Select
                        style={{ width: "70%" }}
                        defaultValue={dashboardData.prd.langgraph_analysis.feature_compliance_results[0]?.feature.feature_name || ""}
                        onChange={(value) => {
                            const feature = allFeatues.find((f: { feature: { feature_id: any; feature_name: any; }; }) => f.feature.feature_id === value);
                            setSelectedFeature(feature);
                        }}
                        options={featureOptionsWithCircles}
                        placeholder="Select a feature"
                        />
                    </div>
                    <div style={{marginTop: "20px", marginBottom:"5px"}}><b>Description</b>:</div>
                    <div>{selectedFeature?.feature.feature_description}</div>
                </>
            </Card> 
          </Card>
        </Col>
        <Col span={11} style={{ display: 'flex', flexDirection: 'column' }}>
            <Card style={{ flex: 1, overflowY: "scroll" }} headStyle={{ textAlign: 'center' }} title="ANALYSIS">
                <div style={{textAlign:"center", fontSize:"16px", marginTop: "5px", marginBottom:"9px"}}>States Compliance</div>
                    <Row justify={"center"}>
                        <Col span={11} style={{textAlign:"center"}}>
                            <Card style={{ backgroundColor: "#d9f7be", color: "green", marginRight:"8px", height: '85%', fontSize: "12px" }}>
                                <CheckCircleOutlined style={{fontSize: "20px"}} /><br />
                                {selectedFeature ? (mapData.filter(state => state.value <= 0.4).length || 0) : ("NA")}<br />
                                Compliant
                            </Card>
                        </Col>
                        <Col span={11} style={{textAlign:"center"}}>
                            <Card style={{ backgroundColor: "#FFCCCC", color: "red", marginRight:"8px", height: '85%', fontSize: "12px" }}>
                                <WarningOutlined style={{fontSize: "20px"}}/><br />
                                {selectedFeature ? (mapData.filter(state => state.value > 0.4).length || 0) : ("NA")}<br />
                                Non-compliant
                            </Card>
                        </Col>
                    </Row>
                    <Row justify={"center"}>
                        <Col span={22}>
                            <div style={{
                                position: "absolute",
                                zIndex: 3,
                                width: "100%",
                                backgroundColor: '#E6E6FA',
                                color: "purple",
                                marginRight:"8px",
                                fontSize: "12px",
                                borderRadius: "8px", // adjust the radius as needed
                                padding: "10px",     // optional padding for better appearance
                                boxSizing: "border-box", // ensures padding doesn’t affect width
                                }}
                            >
                                <Collapse style={{backgroundColor: '#E6E6FA'}} items={items} bordered={false}/>
                            </div>
                        </Col>
                    </Row>
                <div style={{textAlign:"center", fontSize:"16px", marginTop: "90px", marginBottom:"5px"}}>Recommendation</div>
            {selectedFeature ? (
              <div>
                {selectedFeature?.recommendations && selectedFeature?.recommendations.length > 0 ? (
                    <ul>
                        {selectedFeature?.recommendations.map((rec: string, index: Key | null | undefined) => (
                        <li key={index}>{rec}</li>
                        ))}
                    </ul>
                ) : (
                <p>N/A</p>
                )}
                <div style={{ display: "flex", justifyContent: "center", gap: "16px", marginTop: "5px" }} >
                  <Button style={{ marginRight: "10px" }} onClick={() => showModal('approve')}>Approve</Button>
                  <Button onClick={() => showModal('reject')}>Reject</Button>
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
                Feature Name: {selectedFeature?.feature_name || 'N/A'} <br />
                Agent: LangGraph Analysis <br />
                Reason of {buttonValue === 'approve' ? 'approval' : "rejection"}: {selectedFeature?.reasoning || 'N/A'} <br />
                Evidence (optional): <Button>Upload</Button>
              </p>
            </Modal>
          </Card>
        </Col>
      </Row>
      <Modal
        open={openStateModal}
        onCancel={() => {closeStateModal()}}
      >
        {stateModalData?.label}
      </Modal>
    </div>
  );
}
