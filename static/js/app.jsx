const { useEffect, useMemo, useState } = React;

function csrfToken() {
    const input = document.querySelector("input[name='csrfmiddlewaretoken']");
    return input ? input.value : "";
}

async function api(path, options = {}) {
    const response = await fetch(path, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken(),
            ...(options.headers || {}),
        },
    });
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Something went wrong");
    }

    return data;
}

function routeFromPath() {
    const path = window.location.pathname;

    if (path === "/" || path === "/login") return { name: "login" };
    if (path === "/register") return { name: "register" };

    const dashboard = path.match(/^\/dash-(\d+)$/);
    if (dashboard) return { name: "dashboard", userId: Number(dashboard[1]) };

    const create = path.match(/^\/createtask-(\d+)$/);
    if (create) return { name: "create", userId: Number(create[1]) };

    const update = path.match(/^\/update-(\d+)$/);
    if (update) return { name: "update", taskId: Number(update[1]) };

    const remove = path.match(/^\/delpage-(\d+)$/);
    if (remove) return { name: "delete", taskId: Number(remove[1]) };

    return { name: "login" };
}

function App() {
    const [route, setRoute] = useState(routeFromPath);
    const [session, setSession] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const onPop = () => setRoute(routeFromPath());
        window.addEventListener("popstate", onPop);
        return () => window.removeEventListener("popstate", onPop);
    }, []);

    useEffect(() => {
        if (!route.userId || session?.user?.id === route.userId) return;

        setLoading(true);
        api(`/api/users/${route.userId}/tasks`)
            .then(setSession)
            .catch(() => navigate("/login"))
            .finally(() => setLoading(false));
    }, [route.userId]);

    function navigate(path) {
        window.history.pushState({}, "", path);
        setRoute(routeFromPath());
    }

    function logout() {
        setSession(null);
        navigate("/login");
    }

    if (loading) {
        return <main className="app empty-state">Loading...</main>;
    }

    if (route.name === "register") {
        return <AuthForm mode="register" navigate={navigate} setSession={setSession} />;
    }

    if (route.name === "dashboard") {
        return <Dashboard session={session} setSession={setSession} navigate={navigate} logout={logout} />;
    }

    if (route.name === "create") {
        return <TaskForm mode="create" route={route} session={session} setSession={setSession} navigate={navigate} />;
    }

    if (route.name === "update") {
        return <TaskForm mode="update" route={route} session={session} setSession={setSession} navigate={navigate} />;
    }

    if (route.name === "delete") {
        return <DeleteTask route={route} setSession={setSession} navigate={navigate} />;
    }

    return <AuthForm mode="login" navigate={navigate} setSession={setSession} />;
}

function AuthForm({ mode, navigate, setSession }) {
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

                    <button className="primary-btn" type="submit">{isRegister ? "Register" : "Login"}</button>
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

function Dashboard({ session, setSession, navigate, logout }) {
    const [query, setQuery] = useState("");

    if (!session) {
        return <main className="app empty-state">Please log in again.</main>;
    }

    const filteredTasks = useMemo(() => {
        return session.tasks.filter((task) => task.title.toLowerCase().includes(query.toLowerCase()));
    }, [session.tasks, query]);

    return (
        <main className="app">
            <section className="task-shell">
                <header className="topbar">
                    <div className="topbar-actions">
                        <button className="logout-btn" onClick={logout}>Logout</button>
                    </div>
                    <h1>Hello {session.user.username},</h1>
                    <p>You have <i>{session.count}</i> incomplete tasks</p>
                </header>

                <div className="toolbar">
                    <input
                        className="search-input"
                        value={query}
                        onChange={(event) => setQuery(event.target.value)}
                        placeholder="Search task..."
                    />
                    <button className="ghost-btn" type="button">Search</button>
                    <button
                        className="icon-btn"
                        title="Add task"
                        aria-label="Add task"
                        onClick={() => navigate(`/createtask-${session.user.id}`)}
                    >
                        +
                    </button>
                </div>

                <div className="task-list">
                    {filteredTasks.length === 0 ? (
                        <div className="empty-state">No tasks found.</div>
                    ) : (
                        filteredTasks.map((task) => (
                            <div className="task-row" key={task.id}>
                                <span className={`status-dot ${task.completed ? "done" : ""}`} />
                                <button
                                    className={`task-title ${task.completed ? "done" : ""}`}
                                    onClick={() => navigate(`/update-${task.id}`)}
                                >
                                    {task.title}
                                </button>
                                <button
                                    className="delete-btn"
                                    title="Delete task"
                                    aria-label={`Delete ${task.title}`}
                                    onClick={() => navigate(`/delpage-${task.id}`)}
                                >
                                    x
                                </button>
                            </div>
                        ))
                    )}
                </div>
            </section>
        </main>
    );
}

function TaskForm({ mode, route, session, setSession, navigate }) {
    const isUpdate = mode === "update";
    const [task, setTask] = useState({ title: "", description: "", completed: false, user_id: route.userId });
    const [error, setError] = useState("");

    useEffect(() => {
        if (!isUpdate) return;

        api(`/api/tasks/${route.taskId}`)
            .then((data) => setTask(data.task))
            .catch((err) => setError(err.message));
    }, [route.taskId]);

    function updateField(event) {
        const { name, value, checked, type } = event.target;
        setTask({ ...task, [name]: type === "checkbox" ? checked : value });
    }

    async function submit(event) {
        event.preventDefault();
        setError("");

        const userId = isUpdate ? task.user_id : route.userId;
        const path = isUpdate ? `/api/tasks/${route.taskId}/update` : `/api/tasks/${route.userId}/create`;

        try {
            const data = await api(path, {
                method: "POST",
                body: JSON.stringify(task),
            });
            setSession(data);
            navigate(`/dash-${userId}`);
        } catch (err) {
            setError(err.message);
        }
    }

    const backId = task.user_id || route.userId || session?.user?.id;

    return (
        <main className="app">
            <section className="form-shell">
                <button className="back-btn" onClick={() => navigate(`/dash-${backId}`)}>Back</button>
                <h1>{isUpdate ? "Update task" : "Create task"}</h1>
                <p className="muted">{isUpdate ? "Adjust the details and status." : "Add something useful to your list."}</p>

                <form onSubmit={submit}>
                    <div className="field">
                        <label>Title</label>
                        <input name="title" maxLength="20" value={task.title} onChange={updateField} />
                    </div>

                    <div className="field">
                        <label>Description</label>
                        <textarea name="description" value={task.description} onChange={updateField} />
                    </div>

                    <label className="checkbox-row">
                        <input name="completed" type="checkbox" checked={task.completed} onChange={updateField} />
                        Complete
                    </label>

                    <button className="primary-btn" type="submit">Submit</button>
                    <p className="error">{error}</p>
                </form>
            </section>
        </main>
    );
}

function DeleteTask({ route, setSession, navigate }) {
    const [task, setTask] = useState(null);
    const [error, setError] = useState("");

    useEffect(() => {
        api(`/api/tasks/${route.taskId}`)
            .then((data) => setTask(data.task))
            .catch((err) => setError(err.message));
    }, [route.taskId]);

    async function removeTask() {
        if (!task) return;

        try {
            const data = await api(`/api/tasks/${task.id}/delete`, { method: "POST" });
            setSession(data);
            navigate(`/dash-${task.user_id}`);
        } catch (err) {
            setError(err.message);
        }
    }

    const backId = task?.user_id || "";

    return (
        <main className="app">
            <section className="confirm-shell">
                <button className="back-btn" disabled={!backId} onClick={() => navigate(`/dash-${backId}`)}>Go Back</button>
                <h1>Delete task?</h1>
                <p className="muted">This will remove the task from your list.</p>

                {task && <div className="confirm-title">{task.title}</div>}
                <p className="error">{error}</p>

                <div className="confirm-actions">
                    <button className="ghost-btn" disabled={!backId} onClick={() => navigate(`/dash-${backId}`)}>Cancel</button>
                    <button className="danger-btn" onClick={removeTask}>Delete</button>
                </div>
            </section>
        </main>
    );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
