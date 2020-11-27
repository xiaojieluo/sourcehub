code_data = {
    0: {'error_code': 0, 'message': "normal"}
}

def error_code(code: int) -> int:
    if code in code_data:
        return code_data[code]['error_code']
    else:
        raise Exception("not found error_code")