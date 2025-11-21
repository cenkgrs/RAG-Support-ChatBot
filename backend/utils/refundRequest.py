import re

def returnOrderApi(data):
    print(data)

    isValid = isValidEmail(data['customerEmail'])

    if not isValid:
        return {"status": False, "message": "E-Posta bilgisini tekrar iletebilir misiniz ?"}

    print("api isteği gidiyor")
    return {"message": "Oldu bitti maşallah", "code": "571311263", "status": True}

def isValidEmail(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None