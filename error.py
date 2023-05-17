def error(e):
    print(e.status_code)
    print(e.request_id)
    print(e.error_code)
    print(e.error_msg)