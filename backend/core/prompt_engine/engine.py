from dataclasses import dataclass


MODE_HINTS = {
    "safe": "Follow strict Siemens naming conventions, do not modify OB blocks, include manual review checklist.",
    "balanced": "Generate practical SCL with standard naming and basic guard conditions.",
    "free": "Generate complete code quickly, include risk notes for skipped checks.",
}


@dataclass
class PromptContext:
    requirement: str
    mode: str
    template: str | None = None


class PromptEngine:
    def build(self, ctx: PromptContext) -> str:
        mode_hint = MODE_HINTS.get(ctx.mode, MODE_HINTS["balanced"])
        template_part = f"Template:\n{ctx.template}\n" if ctx.template else ""
        return (
            "You are a Siemens TIA Portal SCL code generator. "
            "Output FC/FB/DB/UDT blocks when required and optionally OB insertion snippets.\n"
            f"Mode: {ctx.mode}. {mode_hint}\n"
            f"{template_part}"
            "User requirement:\n"
            f"{ctx.requirement}\n"
            "Return only SCL code and lightweight comments."
        )
