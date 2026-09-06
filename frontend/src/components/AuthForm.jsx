import { useState } from "react";
import { api } from "../utils/api";

export default function AuthForm({ mode, navigate, setSession }) {
  const isRegister = mode === "register";
  const [form, setForm] = useState({ username: "", password: "", confirm: "" });
  const [error, setError] = useState("");

  function updateField(event) {
    setForm({ ...form, [event.target.name]: event.target.value });
  }

  async function submit(event) {
    event.preventDefault();
    setError("");

    try {
      const data = await api(isRegister ? "/api/register" : "/api/login", {
        method: "POST",
        body: JSON.stringify(form),
      });
      setSession(data);
      navigate(`/dash-${data.user.id}`);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <main className="app auth-layout">
      <section className="auth-card">
        <h1>{isRegister ? "Create account" : "Welcome back"}</h1>
        <p className="muted">{isRegister ? "Start a fresh task list." : "Log in to manage your tasks."}</p>

        <form onSubmit={submit}>
          <div className="field">
            <label>Username</label>
            <input name="username" maxLength="20" value={form.username} onChange={updateField} required />
          </div>

          <div className="field">
            <label>Password</label>
            <input name="password" type="password" value={form.password} onChange={updateField} required />
          </div>

          {isRegister && (
            <div className="field">
              <label>Confirm password</label>
              <input name="confirm" type="password" value={form.confirm} onChange={updateField} required />
            </div>
          )}

          <button className="primary-btn" type="submit">
            {isRegister ? "Register" : "Login"}
          </button>
          <p className="error">{error}</p>
        </form>

        <p className="switch-copy">
          {isRegister ? "Already have an account? " : "Don't have an account? "}
          <button className="link-btn" onClick={() => navigate(isRegister ? "/login" : "/register")}>
            {isRegister ? "Login" : "Register"}
          </button>
        </p>
      </section>
    </main>
  );
}
