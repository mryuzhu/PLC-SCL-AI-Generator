import { useState } from "react";

import { Mode, ModeSelector } from "../components/ModeSelector";
import { SclViewer } from "../editor/SclViewer";
import { generateScl } from "../api/client";

export default function HomePage() {
  const [prompt, setPrompt] = useState("创建一个电机控制 FB，输入 Start/Stop/Fault");
  const [mode, setMode] = useState<Mode>("balanced");
  const [code, setCode] = useState("// Generated SCL will appear here");
  const [validation, setValidation] = useState("-");

  const onGenerate = async () => {
    const result = await generateScl(prompt, mode);
    setCode(result.scl_code);
    setValidation(result.validation.status);
  };

  return (
    <main style={{ maxWidth: 960, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>PLC SCL AI Generator</h1>
      <p>Natural language to Siemens TIA Portal style SCL code.</p>
      <textarea rows={8} style={{ width: "100%" }} value={prompt} onChange={(e) => setPrompt(e.target.value)} />
      <div style={{ display: "flex", gap: 12, alignItems: "center", margin: "1rem 0" }}>
        <ModeSelector value={mode} onChange={setMode} />
        <button onClick={onGenerate}>Generate</button>
        <span>Validation: {validation}</span>
      </div>
      <SclViewer code={code} />
    </main>
  );
}
