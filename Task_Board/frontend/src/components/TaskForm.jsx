import { useEffect, useState } from "react";
import { api } from "../utils/api";

export default function TaskForm({ mode, route, session, setSession, navigate }) {
  const isUpdate = mode === "update";
  const [task, setTask] = useState({
    title: "",
    description: "",
    completed: false,
    priority: "Medium",
    due_date: "",
    user_id: route.userId,
  });
  const [error, setError] = useState("");

  useEffect(() => {
    if (!isUpdate) return;

    api(`/api/tasks/${route.taskId}`)
      .then((data) => setTask(data.task))
      .catch((err) => setError(err.message));
  }, [isUpdate, route.taskId]);

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
        <button className="back-btn" onClick={() => navigate(`/dash-${backId}`)}>
          ← Back
        </button>
        <h1>{isUpdate ? "Update task" : "Create task"}</h1>
        <p className="muted">{isUpdate ? "Adjust the details, priority, and status." : "Add something useful to your list."}</p>

        <form onSubmit={submit}>
          <div className="field">
            <label>Title</label>
            <input name="title" maxLength="20" value={task.title} onChange={updateField} required />
          </div>

          <div className="field">
            <label>Description</label>
            <textarea name="description" value={task.description} onChange={updateField} />
          </div>

          <div className="field-grid">
            <div className="field">
              <label>Priority</label>
              <select name="priority" value={task.priority || "Medium"} onChange={updateField} className="select-input">
                <option value="High">🔴 High</option>
                <option value="Medium">🟠 Medium</option>
                <option value="Low">🟢 Low</option>
              </select>
            </div>

            <div className="field">
              <label>Due Date</label>
              <input name="due_date" type="date" value={task.due_date || ""} onChange={updateField} className="date-input" />
            </div>
          </div>

          <label className="checkbox-row">
            <input name="completed" type="checkbox" checked={task.completed} onChange={updateField} />
            Mark as Completed
          </label>

          <button className="primary-btn" type="submit">
            {isUpdate ? "Save Changes" : "Create Task"}
          </button>
          <p className="error">{error}</p>
        </form>
      </section>
    </main>
  );
}
