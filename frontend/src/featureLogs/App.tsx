import { Button, Table, Card, Row, Col, Spin, message, Breadcrumb } from "antd";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { HomeOutlined, DashboardOutlined, FileTextOutlined, DownloadOutlined } from '@ant-design/icons';
import './featureLogs.css';

const signOut = () => {
  localStorage.removeItem("username")
  window.location.href = "../login" 
}

export default function FeatureLogs() {
    if (!localStorage.getItem("username")) {
      window.location.href = "./login"
      return
    }

    const [searchParams] = useSearchParams();
    const prdId = searchParams.get('prdId');
    
    const navigate = useNavigate();
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(false);
    const [prdInfo, setPrdInfo] = useState<any>(null);

    // Table columns for logs - conditionally show columns based on context
    const getTableColumns = () => {
        const baseColumns = [
            {
                title: "UUID",
                dataIndex: "uuid",
                key: "uuid",
                width: 300,
                render: (text: string) => (
                    <span style={{ fontSize: '14px', fontFamily: 'monospace' }}>
                        {text || 'N/A'}
                    </span>
                )
            },
            {
                title: "Action",
                dataIndex: "action",
                key: "action",
                width: 150,
                render: (action: string) => {
                    let color = 'default';
                    if (action.includes('CREATE')) color = 'green';
                    if (action.includes('UPDATE')) color = 'blue';
                    if (action.includes('DELETE')) color = 'red';
                    if (action.includes('ERROR')) color = 'red';
                    if (action.includes('WARNING')) color = 'orange';
                    
                    return (
                        <span style={{ 
                            color: color === 'default' ? undefined : color,
                            fontWeight: 'bold',
                            fontSize: '14px'
                        }}>
                            {action}
                        </span>
                    );
                }
            },
            {
                title: "Details",
                dataIndex: "details",
                key: "details",
                ellipsis: true,
                render: (text: string) => (
                    <span style={{ fontSize: '14px' }}>
                        {text || 'N/A'}
                    </span>
                )
            },
            {
                title: "Timestamp",
                dataIndex: "timestamp",
                key: "timestamp",
                width: 200,
                render: (timestamp: string) => {
                    if (!timestamp) return 'N/A';
                    return (
                        <span style={{ fontSize: '14px' }}>
                            {new Date(timestamp).toLocaleString()}
                        </span>
                    );
                }
            }
        ];

        // Only show PRD UUID column when viewing all logs (no prdId)
        if (!prdId) {
            baseColumns.splice(1, 0, {
                title: "PRD UUID",
                dataIndex: "prd_uuid",
                key: "prd_uuid",
                width: 300,
                render: (text: string) => (
                    <span style={{ fontSize: '14px', fontFamily: 'monospace' }}>
                        {text || 'N/A'}
                    </span>
                )
            });
        }

        return baseColumns;
    };

    // CSV Export function
    const exportToCSV = () => {
        if (logs.length === 0) {
            message.warning('No data to export');
            return;
        }

        try {
            // Get the current columns based on context
            const columns = getTableColumns();
            
            // Create CSV header
            const headers = columns.map(col => col.title).join(',');
            
            // Create CSV rows
            const csvRows = logs.map((log: any) => {
                const row = columns.map(col => {
                    let value = log[col.dataIndex];
                    
                    // Format timestamp if it exists
                    if (col.dataIndex === 'timestamp' && value) {
                        value = new Date(value).toLocaleString();
                    }
                    
                    // Handle special characters and wrap in quotes if needed
                    if (typeof value === 'string' && (value.includes(',') || value.includes('"') || value.includes('\n'))) {
                        value = `"${value.replace(/"/g, '""')}"`;
                    }
                    
                    return value || 'N/A';
                });
                return row.join(',');
            });
            
            // Combine header and rows
            const csvContent = [headers, ...csvRows].join('\n');
            
            // Create and download file
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            const url = URL.createObjectURL(blob);
            
            // Generate filename based on context
            const timestamp = new Date().toISOString().split('T')[0];
            const filename = prdId 
                ? `feature_logs_${prdInfo?.Name || prdId}_${timestamp}.csv`
                : `all_feature_logs_${timestamp}.csv`;
            
            link.setAttribute('href', url);
            link.setAttribute('download', filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            message.success('CSV exported successfully');
        } catch (error) {
            console.error('Error exporting CSV:', error);
            message.error('Failed to export CSV');
        }
    };

    // Fetch logs based on whether prdId is provided
    useEffect(() => {
        const fetchLogs = async () => {
            setLoading(true);
            try {
                let url = '/api/logs';
                if (prdId) {
                    url = `/api/logs/prd/${prdId}`;
                }
                
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                setLogs(data);
                
                // If we have a prdId, also fetch PRD info for context
                if (prdId) {
                    try {
                        const prdResponse = await fetch(`/api/prd/${prdId}`);
                        if (prdResponse.ok) {
                            const prdData = await prdResponse.json();
                            setPrdInfo(prdData);
                        }
                    } catch (error) {
                        console.warn('Could not fetch PRD info:', error);
                    }
                }
                
            } catch (error) {
                console.error('Error fetching logs:', error);
                message.error('Failed to fetch logs');
            } finally {
                setLoading(false);
            }
        };

        fetchLogs();
    }, [prdId]);

    // Breadcrumb items
    const breadcrumbItems = [
        {
            title: <HomeOutlined />,
            href: '/',
        },
        ...(prdId ? [
            {
                title: <DashboardOutlined />,
                href: `/dashboard?prdId=${prdId}`,
            }
        ] : []),
        {
            title: <FileTextOutlined />,
            href: `/featureLogs${prdId ? `?prdId=${prdId}` : ''}`,
        }
    ];

    // Page title based on context
    const pageTitle = prdId 
        ? `Logs for PRD: ${prdInfo?.Name || prdId}`
        : 'All Feature Logs';

    return (
        <div style={{ padding: 24 }}>
            {/* Header */}
            <div style={{ display: "flex", alignItems: "center", marginBottom: 16 }}>
                <h1 style={{ marginTop: 0, marginBottom: 0 }}>{pageTitle}</h1>
                <Button style={{ marginLeft: "auto" }} onClick={() => signOut()}>Sign Out</Button>
            </div>

            {/* Breadcrumb Navigation */}
            {/* <Breadcrumb 
                items={breadcrumbItems}
                style={{ marginBottom: 16 }}
            /> */}

            {/* Context Information */}
            {prdId && prdInfo && (
                <Card 
                    style={{ marginBottom: 16, backgroundColor: '#f0f8ff' }}
                    size="small"
                >
                    <Row gutter={16}>
                        <Col span={8}>
                            <strong>PRD Name:</strong> {prdInfo.Name}
                        </Col>
                        <Col span={8}>
                            <strong>Status:</strong> {prdInfo.Status}
                        </Col>
                        <Col span={8}>
                            <strong>Total Features:</strong> {prdInfo.total_features || 'N/A'}
                        </Col>
                    </Row>
                </Card>
            )}

            {/* Navigation Buttons */}
            <div style={{ marginBottom: 16, display: 'flex', gap: 8, alignItems: 'center' }}>
                <Button onClick={() => navigate('/')}>Go to PRD Form</Button>
                {prdId && (
                    <Button 
                        type="primary"
                        onClick={() => navigate(`/dashboard?prdId=${prdId}`)}
                    >
                        ← Back to PRD Dashboard
                    </Button>
                )}
                
                {/* CSV Export Button */}
                <Button 
                    type="default"
                    icon={<DownloadOutlined />}
                    onClick={exportToCSV}
                    className="csv-export-btn"
                    style={{
                        marginLeft: 'auto'
                    }}
                >
                    Export to CSV
                </Button>
            </div>

            {/* Logs Table */}
            <Card title={`Logs (${logs.length} entries)`}>
                {loading ? (
                    <div style={{ textAlign: 'center', padding: '40px' }}>
                        <Spin size="large" />
                        <p>Loading logs...</p>
                    </div>
                ) : (
                    <Table 
                        columns={getTableColumns()}
                        dataSource={logs}
                        rowKey="uuid"
                        pagination={{
                            pageSize: 20,
                            showSizeChanger: true,
                            showQuickJumper: true,
                            showTotal: (total, range) => 
                                `${range[0]}-${range[1]} of ${total} items`
                        }}
                        scroll={{ x: 1200 }}
                        size="middle"
                        rowClassName={(record, index) => 
                            index % 2 === 0 ? 'table-row-light' : 'table-row-dark'
                        }
                    />
                )}
            </Card>
        </div>
    );
}