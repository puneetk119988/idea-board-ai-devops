import React, { useEffect, useState } from "react";

export default function App() {
  const [ideas, setIdeas] = useState([]);
  const [content, setContent] = useState("");
  const [status, setStatus] = useState("");

  async function safeJson(res) {
    try {
      return await res.json();
    } catch {
      return null;
    }
  }

  async function loadIdeas() {
    setStatus("");
    try {
      const res = await fetch("/api/ideas", { cache: "no-store" });

      if (!res.ok) {
        const text = await res.text().catch(() => "");
        console.error("GET /api/ideas failed", res.status, text);
        setIdeas([]);
        setStatus("Error loading ideas");
        return;
      }

      const data = await safeJson(res);
      if (Array.isArray(data)) {
        setIdeas(data);
      } else if (data && Array.isArray(data.items)) {
        setIdeas(data.items);
      } else {
        setIdeas([]);
      }
    } catch (e) {
      console.error("GET /api/ideas exception", e);
      setIdeas([]);
      setStatus("Error loading ideas");
    }
  }

  useEffect(() => {
    loadIdeas();
  }, []);

  async function addIdea() {
    const trimmed = content.trim();
    if (!trimmed) return;

    setStatus("Saving...");
    try {
      const res = await fetch("/api/ideas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: trimmed }),
      });

      if (!res.ok) {
        const text = await res.text().catch(() => "");
        console.error("POST /api/ideas failed", res.status, text);
        setStatus("Error");
        return;
      }

      setContent("");
      setStatus("Saved ✔");
      await loadIdeas();
    } catch (e) {
      console.error("POST /api/ideas exception", e);
      setStatus("Error");
    }
  }

  function formatDate(value) {
    if (!value) return "Unknown time";
    const d = new Date(value);
    return isNaN(d.getTime()) ? "Unknown time" : d.toLocaleString();
  }

  return (
    <div style={{ maxWidth: 800, margin: "50px auto", fontFamily: "Arial" }}>
      <h1>Idea Board</h1>

      <div style={{ display: "flex", gap: 10 }}>
        <input
          style={{ flex: 1, padding: 8 }}
          placeholder="Share a new idea..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
        <button onClick={addIdea}>Add</button>
      </div>

      <div style={{ marginTop: 10 }}>{status}</div>

      <h3 style={{ marginTop: 30 }}>Latest ideas</h3>

      {ideas.length === 0 ? (
        <div style={{ color: "#666" }}>No ideas yet.</div>
      ) : (
        <ul>
          {ideas.map((idea) => (
            <li key={idea.id}>
              <strong>{idea.content}</strong>{" "}
              <span style={{ color: "#666" }}>
                ({formatDate(idea.created_at)})
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}