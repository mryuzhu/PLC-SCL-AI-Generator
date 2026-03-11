import React from "react";

export function SclViewer({ code }: { code: string }) {
  return <pre style={{ whiteSpace: "pre-wrap", background: "#0f172a", color: "#e2e8f0", padding: 12 }}>{code}</pre>;
}
