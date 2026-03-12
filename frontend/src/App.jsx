import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "https://task-manager-app-production-6417.up.railway.app";
function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");

  // 🔄 Load all tasks when the page loads
  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await axios.get(`${API_URL}/tasks`);
      setTasks(response.data);
      setError("");
    } catch (err) {
      setError("❌ Cannot connect to backend. Is it running?");
    }
  };

  // ➕ Add a new task
  const addTask = async () => {
    if (!title.trim()) return;
    try {
      await axios.post(`${API_URL}/tasks`, { title, description });
      setTitle("");
      setDescription("");
      fetchTasks(); // refresh the list
    } catch (err) {
      setError("❌ Failed to add task.");
    }
  };

  // ✅ Toggle task complete/incomplete
  const toggleTask = async (task) => {
    try {
      await axios.patch(`${API_URL}/tasks/${task.id}`, {
        completed: !task.completed,
      });
      fetchTasks();
    } catch (err) {
      setError("❌ Failed to update task.");
    }
  };

  // 🗑️ Delete a task
  const deleteTask = async (id) => {
    try {
      await axios.delete(`${API_URL}/tasks/${id}`);
      fetchTasks();
    } catch (err) {
      setError("❌ Failed to delete task.");
    }
  };

  // ⌨️ Allow pressing Enter to submit
  const handleKeyDown = (e) => {
    if (e.key === "Enter") addTask();
  };

  return (
    <div className="app">
      <h1>📝 Task Manager</h1>

      {error && <div className="error">{error}</div>}

      {/* Input Section */}
      <div className="input-section">
        <input
          type="text"
          placeholder="Task title (required)"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <textarea
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button onClick={addTask}>+ Add Task</button>
      </div>

      {/* Task List */}
      <div className="task-list">
        {tasks.length === 0 ? (
          <div className="empty">No tasks yet. Add one above! ☝️</div>
        ) : (
          tasks.map((task) => (
            <div
              key={task.id}
              className={`task-card ${task.completed ? "completed" : ""}`}
            >
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => toggleTask(task)}
              />
              <div className="task-info">
                <h3>{task.title}</h3>
                {task.description && <p>{task.description}</p>}
              </div>
              <button
                className="delete-btn"
                onClick={() => deleteTask(task.id)}
              >
                🗑️
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
