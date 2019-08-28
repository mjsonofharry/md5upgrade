from dataclasses import dataclass
import abc

@dataclass(frozen=True)
class Vector:
    x: float
    y: float
    z: float = None
    w: float = None

def formatValue(v):
    v_fl = round(float(v), 10)
    v_int = int(v_fl)
    return str(v_int) if float(v_int) == v_fl else v_fl
