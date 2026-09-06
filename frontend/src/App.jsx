import { useEffect, useState } from "react";
import AuthForm from "./components/AuthForm";
import Dashboard from "./components/Dashboard";
import TaskForm from "./components/TaskForm";
import DeleteTask from "./components/DeleteTask";
import { api } from "./utils/api";

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

export default function App() {
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
  }, [route.userId, session?.user?.id]);

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
    return (
      <TaskForm
        mode="create"
        route={route}
        session={session}
        setSession={setSession}
        navigate={navigate}
      />
    );
  }

  if (route.name === "update") {
    return (
      <TaskForm
        mode="update"
        route={route}
        session={session}
        setSession={setSession}
        navigate={navigate}
      />
    );
  }

  if (route.name === "delete") {
    return <DeleteTask route={route} setSession={setSession} navigate={navigate} />;
  }

  return <AuthForm mode="login" navigate={navigate} setSession={setSession} />;
}
