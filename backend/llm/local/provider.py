from backend.llm.base import BaseProvider


class LocalModelProvider(BaseProvider):
    def generate_code(self, prompt: str) -> str:
        _ = prompt
        return """TYPE UDT_MotorState :
STRUCT
    Running : Bool;
    Faulted : Bool;
END_STRUCT;
END_TYPE

FUNCTION_BLOCK FB_MotorControl
VAR_INPUT
    Start : Bool;
    Stop : Bool;
    Fault : Bool;
END_VAR
VAR_OUTPUT
    MotorOn : Bool;
END_VAR
VAR
    State : UDT_MotorState;
END_VAR
BEGIN
    IF (Start AND NOT Fault) THEN
        MotorOn := TRUE;
    END_IF;

    IF (Stop OR Fault) THEN
        MotorOn := FALSE;
    END_IF;

    State.Running := MotorOn;
    State.Faulted := Fault;
END_FUNCTION_BLOCK

DATA_BLOCK DB_Motor_Instance
    MotorCtrl : FB_MotorControl;
END_DATA_BLOCK"""
