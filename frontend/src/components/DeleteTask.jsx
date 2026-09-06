import { useEffect, useState } from "react";
import { api } from "../utils/api";

export default function DeleteTask({ route, setSession, navigate }) {
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
        <button className="back-btn" disabled={!backId} onClick={() => navigate(`/dash-${backId}`)}>
          Go Back
        </button>
        <h1>Delete task?</h1>
        <p className="muted">This will remove the task from your list.</p>

        {task && <div className="confirm-title">{task.title}</div>}
        <p className="error">{error}</p>

        <div className="confirm-actions">
          <button className="ghost-btn" disabled={!backId} onClick={() => navigate(`/dash-${backId}`)}>
            Cancel
          </button>
          <button className="danger-btn" onClick={removeTask}>
            Delete
          </button>
        </div>
      </section>
    </main>
  );
}
