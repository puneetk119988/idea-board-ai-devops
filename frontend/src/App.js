import React, { useEffect, useState } from "react";

const apiBase = "/api"; // nginx proxies /api -> backend

export default function App() {
  const [ideas, setIdeas] = useState([]);
  const [content, setContent] = useState("");
  const [status, setStatus] = useState("");

  const load = async () => {
    const r = await fetch(`${apiBase}/ideas`);
    const data = await r.json();
    setIdeas(data);
  };

  useEffect(() => { load(); }, []);

  const submit = async () => {
    setStatus("");
    if (!content.trim()) return setStatus("Please write an idea first.");
    const r = await fetch(`${apiBase}/ideas`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content })
    });
    if (!r.ok) return setStatus("Failed to save. Try again.");
    setContent("");
    await load();
    setStatus("Saved ✅");
  };

  return (
    <div style={{ maxWidth: 760, margin: "40px auto", fontFamily: "system-ui" }}>
      <h1>Idea Board</h1>

      <div style={{ display: "flex", gap: 8 }}>
        <input
          style={{ flex: 1, padding: 10, fontSize: 16 }}
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Share a new idea…"
        />
        <button style={{ padding: "10px 16px", fontSize: 16 }} onClick={submit}>
          Add
        </button>
      </div>

      {status && <p>{status}</p>}

      <h3 style={{ marginTop: 28 }}>Latest ideas</h3>
      <ul>
        {ideas.map((i) => (
          <li key={i.id}>
            {i.content} <small style={{ opacity: 0.65 }}>({new Date(i.created_at).toLocaleString()})</small>
          </li>
        ))}
      </ul>
    </div>
  );
}
