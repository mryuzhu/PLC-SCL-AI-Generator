import React from "react";

export type Mode = "safe" | "balanced" | "free";

export function ModeSelector({ value, onChange }: { value: Mode; onChange: (m: Mode) => void }) {
  return (
    <label>
      Mode:
      <select value={value} onChange={(e) => onChange(e.target.value as Mode)}>
        <option value="safe">Safe</option>
        <option value="balanced">Balanced</option>
        <option value="free">Free</option>
      </select>
    </label>
  );
}
