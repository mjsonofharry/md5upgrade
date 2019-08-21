def simplifyFloat(v_str):
    v_fl = float(v_str)
    v_int = int(v_fl)
    return v_int if float(v_int) == v_fl else v_fl