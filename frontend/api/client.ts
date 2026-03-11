export async function generateScl(prompt: string, mode: "safe" | "balanced" | "free") {
  const resp = await fetch("http://localhost:8000/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt, mode, model: "local" }),
  });
  if (!resp.ok) {
    throw new Error(`API failed: ${resp.status}`);
  }
  return resp.json();
}
