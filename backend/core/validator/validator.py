import re

from backend.models.schemas import ValidationIssue, ValidationResult


class CodeValidator:
    REQUIRED_BLOCK_PATTERNS = [r"FUNCTION_BLOCK", r"DATA_BLOCK", r"TYPE"]

    def validate(self, scl_code: str, mode: str = "balanced") -> ValidationResult:
        warnings: list[ValidationIssue] = []
        errors: list[ValidationIssue] = []

        for pattern in self.REQUIRED_BLOCK_PATTERNS:
            if not re.search(pattern, scl_code, re.IGNORECASE):
                warnings.append(ValidationIssue(code="MISSING_BLOCK", message=f"Missing recommended block: {pattern}"))

        if re.search(r"ORGANIZATION_BLOCK", scl_code, re.IGNORECASE):
            if mode == "safe":
                errors.append(ValidationIssue(code="OB_FORBIDDEN", message="Safe mode forbids direct OB modification."))
            else:
                warnings.append(ValidationIssue(code="OB_TOUCH", message="OB generated; ensure this is an insertion snippet only."))

        if re.search(r"\bTEMP\b\s*:\s*INT\s*;", scl_code, re.IGNORECASE):
            warnings.append(ValidationIssue(code="GENERIC_NAME", message="Variable name TEMP is too generic."))

        if mode == "safe" and not re.search(r"FB_[A-Za-z0-9_]+", scl_code):
            errors.append(ValidationIssue(code="NAMING", message="Safe mode requires FB_ naming convention."))

        status = "pass"
        if errors:
            status = "error"
        elif warnings:
            status = "warning"

        return ValidationResult(status=status, warnings=warnings, errors=errors)
