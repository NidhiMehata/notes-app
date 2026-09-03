import { useState } from "react";
import "./Login.css";
import { login } from "./api/auth";

type LoginProps = {
  onLogin: () => void;
};

function Login({ onLogin }: LoginProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleLogin() {
    try {
      setLoginError("");

      if (!email.trim()) {
        setLoginError("Email is required.");
        return;
      }

      if (!password) {
        setLoginError("Password is required.");
        return;
      }

      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (!emailPattern.test(email)) {
        setLoginError("Please enter a valid email address.");
        return;
      }

      setIsLoading(true);

      const data = await login(email, password);

      localStorage.setItem("access_token", data.access_token);
      onLogin();
    } catch (error) {
      if (error instanceof Error) {
        setLoginError(error.message);
      } else {
        setLoginError("Something went wrong. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <h1>Notes App</h1>

        <form
          noValidate
          onSubmit={(event) => {
            event.preventDefault();
            handleLogin();
          }}
        >
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
            />
          </div>

          {loginError && <p className="login-error">{loginError}</p>}

          <button className="login-button" type="submit" disabled={isLoading}>
            {isLoading ? "Logging in..." : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
