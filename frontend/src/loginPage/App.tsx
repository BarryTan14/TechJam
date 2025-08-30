import { Card, Input, Button, Form, message } from "antd"
import { useForm } from "antd/es/form/Form"

const checkLogin = async (form: any) => {
    const payload = form.getFieldsValue()
    
    try {
        // Call the user login API
        const response = await fetch('http://localhost:5000/api/users/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: payload.username,
                password: payload.password
            })
        })

        if (response.ok) {
            const userData = await response.json()
            // Store username in localStorage (keeping existing behavior)
            localStorage.setItem("username", userData.username)
            // Continue with existing redirect behavior
            window.location.href = "../"
        } else {
            // Handle login failure
            message.error('Invalid username or password')
        }
    } catch (error) {
        console.error('Login error:', error)
        message.error('Login failed. Please try again.')
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