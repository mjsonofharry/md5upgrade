def formatValue(v):
    v_fl = round(float(v), 10)
    v_int = int(v_fl)
    return str(v_int) if float(v_int) == v_fl else v_fl