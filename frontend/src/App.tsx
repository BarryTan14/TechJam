import { Card, Row, Col } from 'antd';


export default function Dashboard() {
    return (
        <div style={{ padding: 24 }}>
            <h1 className='text-3xl font-extrabold' style={{"marginTop": 0}}>DASHBOARD</h1>
            <Row className="mt-2" justify="space-evenly">
                <Col span={4}>
                    <Card></Card>
                </Col>
                <Col span={12}>
                    <Card></Card>
                </Col>
                <Col span={4}>
                    <Card></Card>
                </Col>
            </Row>
            
        </div>
    );
}
