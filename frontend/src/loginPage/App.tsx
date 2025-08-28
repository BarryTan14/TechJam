import { Card, Input, Button, Form } from "antd"
import { useForm } from "antd/es/form/Form"

const checkLogin = (form: any) => {
    const payload = form.getFieldsValue()
    if (payload["password"] == "12345") {
        localStorage.setItem("username", payload["username"])
        window.location.href = "../"
    }
}

export default function Login() {
    const [form] = useForm()

    return (
        <div style={{ padding: 24 }}>
            <h1 style={{marginTop: 0, textAlign: "center"}}>LOGIN PAGE</h1>
            <Card style={{maxWidth: "40%", margin:"0 auto"}}>
                <Form form={form}>
                    <Form.Item
                        name="username"
                        label="Username"
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        name="password"
                        label="Password"
                    >
                        <Input />
                    </Form.Item>
                    <Button htmlType="button" onClick={() => checkLogin(form)}>Log In</Button>
                </Form>
            </Card>
        </div>
    )
}