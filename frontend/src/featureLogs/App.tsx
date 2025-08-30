import { Button, Table, Card, Row, Col, Spin, message, Breadcrumb } from "antd";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { HomeOutlined, DashboardOutlined, FileTextOutlined, DownloadOutlined } from '@ant-design/icons';
import './featureLogs.css';

const signOut = () => {
  localStorage.removeItem("username")
  window.location.href = "../login" 
}

// Utility function to format timestamps in Singapore time
const formatSingaporeTime = (timestamp: string) => {
  if (!timestamp) return 'N/A';
  
  try {
    const date = new Date(timestamp);
    
    // Format for Singapore timezone (UTC+8)
    return date.toLocaleString('en-SG', {
      timeZone: 'Asia/Singapore',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    });
  } catch (error) {
    console.error('Error formatting timestamp:', error);
    return 'Invalid Date';
  }
};

// Debug function to show timezone conversion details
const debugTimezone = (timestamp: string) => {
  if (!timestamp) return 'N/A';
  
  try {
    const date = new Date(timestamp);
    const utcTime = date.toISOString();
    const singaporeTime = formatSingaporeTime(timestamp);
    const localTime = date.toLocaleString();
    
    console.log('Timestamp Debug:', {
      original: timestamp,
      utc: utcTime,
      singapore: singaporeTime,
      local: localTime
    });
    
    return singaporeTime;
  } catch (error) {
    console.error('Error in debugTimezone:', error);
    return 'Invalid Date';
  }
};

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
    const [isMobile, setIsMobile] = useState(false);

    // Check screen size and update responsive state
    useEffect(() => {
        const checkScreenSize = () => {
            setIsMobile(window.innerWidth <= 768);
        };

        checkScreenSize();
        window.addEventListener('resize', checkScreenSize);
        
        return () => window.removeEventListener('resize', checkScreenSize);
    }, []);

    // Table columns for logs - conditionally show columns based on context and screen size
    const getTableColumns = () => {
        const baseColumns = [
            {
                title: "UUID",
                dataIndex: "uuid",
                key: "uuid",
                width: isMobile ? 120 : 300,
                ellipsis: isMobile,
                render: (text: string) => (
                    <span style={{ 
                        fontSize: isMobile ? '12px' : '14px', 
                        fontFamily: 'monospace',
                        wordBreak: isMobile ? 'break-all' : 'normal'
                    }}>
                        {isMobile ? (text ? `${text.substring(0, 8)}...` : 'N/A') : (text || 'N/A')}
                    </span>
                )
            },
            {
                title: "Action",
                dataIndex: "action",
                key: "action",
                width: isMobile ? 80 : 150,
                ellipsis: isMobile,
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
                            fontSize: isMobile ? '11px' : '14px'
                        }}>
                            {isMobile ? action.substring(0, 6) : action}
                        </span>
                    );
                }
            },
            {
                title: "Details",
                dataIndex: "details",
                key: "details",
                ellipsis: true,
                width: isMobile ? 120 : undefined,
                render: (text: string) => (
                    <span style={{ fontSize: isMobile ? '11px' : '14px' }}>
                        {isMobile ? (text ? `${text.substring(0, 15)}...` : 'N/A') : (text || 'N/A')}
                    </span>
                )
            },
            {
                title: isMobile ? "Time" : "Timestamp (Singapore Time)",
                dataIndex: "timestamp",
                key: "timestamp",
                width: isMobile ? 100 : 250,
                ellipsis: isMobile,
                render: (timestamp: string) => {
                    const formattedTime = debugTimezone(timestamp);
                    return (
                        <span style={{ fontSize: isMobile ? '10px' : '14px' }}>
                            {isMobile ? (formattedTime ? formattedTime.split(' ')[1] : 'N/A') : formattedTime}
                        </span>
                    );
                }
            }
        ];

        // Only show PRD UUID column when viewing all logs (no prdId) and not on mobile
        if (!prdId && !isMobile) {
            baseColumns.splice(1, 0, {
                title: "PRD UUID",
                dataIndex: "prd_uuid",
                key: "prd_uuid",
                width: 300,
                ellipsis: true,
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
        <div style={{ padding: isMobile ? 12 : 24 }}>
            {/* Header */}
            <div style={{ 
                display: "flex", 
                flexDirection: isMobile ? "column" : "row",
                alignItems: isMobile ? "stretch" : "center", 
                marginBottom: 16,
                gap: isMobile ? 8 : 0
            }}>
                <h1 style={{ 
                    marginTop: 0, 
                    marginBottom: 0,
                    fontSize: isMobile ? '20px' : '24px',
                    textAlign: isMobile ? 'center' : 'left'
                }}>
                    {pageTitle}
                </h1>
                <Button 
                    style={{ 
                        marginLeft: isMobile ? 0 : "auto",
                        width: isMobile ? '100%' : 'auto'
                    }} 
                    onClick={() => signOut()}
                >
                    Sign Out
                </Button>
            </div>

            {/* Context Information */}
            {prdId && prdInfo && (
                <Card 
                    style={{ marginBottom: 16, backgroundColor: '#f0f8ff' }}
                    size="small"
                >
                    <Row gutter={isMobile ? 8 : 16}>
                        <Col span={isMobile ? 24 : 8} style={{ marginBottom: isMobile ? 8 : 0 }}>
                            <strong>PRD Name:</strong> {prdInfo.Name}
                        </Col>
                        <Col span={isMobile ? 24 : 8} style={{ marginBottom: isMobile ? 8 : 0 }}>
                            <strong>Status:</strong> {prdInfo.Status}
                        </Col>
                        <Col span={isMobile ? 24 : 8}>
                            <strong>Total Features:</strong> {prdInfo.total_features || 'N/A'}
                        </Col>
                    </Row>
                </Card>
            )}

            {/* Navigation Buttons */}
            <div style={{ 
                marginBottom: 16, 
                display: 'flex', 
                flexDirection: isMobile ? 'column' : 'row',
                gap: 8, 
                alignItems: 'stretch'
            }}>
                <Button 
                    onClick={() => navigate('/')}
                    style={{ width: isMobile ? '100%' : 'auto' }}
                >
                    Go to PRD Form
                </Button>
                {prdId && (
                    <Button 
                        type="primary"
                        onClick={() => navigate(`/dashboard?prdId=${prdId}`)}
                        style={{ width: isMobile ? '100%' : 'auto' }}
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
                        marginLeft: isMobile ? 0 : 'auto',
                        width: isMobile ? '100%' : 'auto'
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
                            pageSize: isMobile ? 10 : 20,
                            showSizeChanger: !isMobile,
                            showQuickJumper: !isMobile,
                            showTotal: isMobile ? undefined : (total, range) => 
                                `${range[0]}-${range[1]} of ${total} items`,
                            size: isMobile ? 'small' : 'default'
                        }}
                        scroll={{ 
                            x: isMobile ? 500 : 1200,
                            y: isMobile ? 400 : undefined
                        }}
                        size={isMobile ? "small" : "middle"}
                        rowClassName={(record, index) => 
                            index % 2 === 0 ? 'table-row-light' : 'table-row-dark'
                        }
                        className={isMobile ? 'mobile-table' : ''}
                    />
                )}
            </Card>
        </div>
    );
}