import { useMemo, useState } from "react";
import ThemeToggle from "./ThemeToggle";
import ProgressBar from "./ProgressBar";
import { api } from "../utils/api";

export default function Dashboard({ session, setSession, navigate, logout }) {
  const [query, setQuery] = useState("");
  const [filterTab, setFilterTab] = useState("all"); // 'all', 'pending', 'completed', 'high'
  const [sortBy, setSortBy] = useState("newest"); // 'newest', 'priority', 'title'

  if (!session) {
    return <main className="app empty-state">Please log in again.</main>;
  }

  const tasks = session.tasks || [];
  const totalCount = tasks.length;
  const completedCount = tasks.filter((t) => t.completed).length;
  const pendingCount = totalCount - completedCount;
  const highPriorityCount = tasks.filter((t) => (t.priority || "").toLowerCase() === "high").length;

  async function handleToggle(taskId) {
    try {
      const data = await api(`/api/tasks/${taskId}/toggle`, { method: "POST" });
      setSession(data);
    } catch (err) {
      console.error(err);
    }
  }

  const filteredTasks = useMemo(() => {
    let result = tasks.filter((task) =>
      task.title.toLowerCase().includes(query.toLowerCase()) ||
      (task.description || "").toLowerCase().includes(query.toLowerCase())
    );

    if (filterTab === "pending") {
      result = result.filter((t) => !t.completed);
    } else if (filterTab === "completed") {
      result = result.filter((t) => t.completed);
    } else if (filterTab === "high") {
      result = result.filter((t) => (t.priority || "").toLowerCase() === "high");
    }

    const priorityWeight = { High: 3, Medium: 2, Low: 1 };

    result.sort((a, b) => {
      if (sortBy === "priority") {
        const weightA = priorityWeight[a.priority] || 2;
        const weightB = priorityWeight[b.priority] || 2;
        return weightB - weightA;
      }
      if (sortBy === "title") {
        return a.title.localeCompare(b.title);
      }
      // Default: newest first by id
      return b.id - a.id;
    });

    return result;
  }, [tasks, query, filterTab, sortBy]);

  function getDueDateBadge(dueDate) {
    if (!dueDate) return null;
    const today = new Date().toISOString().split("T")[0];
    if (dueDate < today) {
      return <span className="due-tag overdue">Overdue ({dueDate})</span>;
    }
    if (dueDate === today) {
      return <span className="due-tag today">Due Today</span>;
    }
    return <span className="due-tag upcoming">Due {dueDate}</span>;
  }

  return (
    <main className="app">
      <section className="task-shell">
        <header className="topbar">
          <div className="topbar-actions">
            <ThemeToggle />
            <button className="logout-btn" onClick={logout}>
              Logout
            </button>
          </div>
          <h1>Hello {session.user.username},</h1>
          <p>
            You have <i>{pendingCount}</i> incomplete tasks
          </p>
        </header>

        {/* Analytics & Progress Section */}
        <div className="analytics-section">
          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-label">Total Tasks</span>
              <span className="stat-value">{totalCount}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Pending</span>
              <span className="stat-value pending">{pendingCount}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Completed</span>
              <span className="stat-value done">{completedCount}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">High Priority</span>
              <span className="stat-value high">{highPriorityCount}</span>
            </div>
          </div>

          <ProgressBar total={totalCount} completed={completedCount} />
        </div>

        {/* Toolbar & Filter Controls */}
        <div className="toolbar">
          <div className="search-box">
            <input
              className="search-input"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search by title or description..."
            />
          </div>

          <div className="toolbar-controls">
            <div className="sort-box">
              <label>Sort:</label>
              <select className="select-sort" value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
                <option value="newest">Newest First</option>
                <option value="priority">Priority</option>
                <option value="title">Title (A-Z)</option>
              </select>
            </div>

            <button
              className="icon-btn"
              title="Add new task"
              aria-label="Add new task"
              onClick={() => navigate(`/createtask-${session.user.id}`)}
            >
              +
            </button>
          </div>
        </div>

        {/* Filter Tabs */}
        <div className="filter-tabs">
          <button className={`tab-btn ${filterTab === "all" ? "active" : ""}`} onClick={() => setFilterTab("all")}>
            All ({totalCount})
          </button>
          <button className={`tab-btn ${filterTab === "pending" ? "active" : ""}`} onClick={() => setFilterTab("pending")}>
            Pending ({pendingCount})
          </button>
          <button className={`tab-btn ${filterTab === "completed" ? "active" : ""}`} onClick={() => setFilterTab("completed")}>
            Completed ({completedCount})
          </button>
          <button className={`tab-btn ${filterTab === "high" ? "active" : ""}`} onClick={() => setFilterTab("high")}>
            High Priority ({highPriorityCount})
          </button>
        </div>

        {/* Task List */}
        <div className="task-list">
          {filteredTasks.length === 0 ? (
            <div className="empty-state">No tasks found matching filters.</div>
          ) : (
            filteredTasks.map((task) => (
              <div className={`task-row ${task.completed ? "is-done" : ""}`} key={task.id}>
                <button
                  className={`status-toggle-btn ${task.completed ? "done" : ""}`}
                  onClick={() => handleToggle(task.id)}
                  title={task.completed ? "Mark as pending" : "Mark as completed"}
                >
                  {task.completed ? "✓" : ""}
                </button>

                <div className="task-content">
                  <div className="task-header-row">
                    <button
                      className={`task-title ${task.completed ? "done" : ""}`}
                      onClick={() => navigate(`/update-${task.id}`)}
                    >
                      {task.title}
                    </button>

                    <span className={`priority-badge ${(task.priority || "Medium").toLowerCase()}`}>
                      {task.priority || "Medium"}
                    </span>

                    {getDueDateBadge(task.due_date)}
                  </div>

                  {task.description && (
                    <p className="task-desc-preview">{task.description}</p>
                  )}
                </div>

                <div className="task-actions">
                  <button
                    className="edit-btn"
                    title="Edit task"
                    onClick={() => navigate(`/update-${task.id}`)}
                  >
                    ✏️
                  </button>
                  <button
                    className="delete-btn"
                    title="Delete task"
                    aria-label={`Delete ${task.title}`}
                    onClick={() => navigate(`/delpage-${task.id}`)}
                  >
                    ×
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </section>
    </main>
  );
}
