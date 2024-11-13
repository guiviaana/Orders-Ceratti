import requests
import json

# Função para autenticar e obter o token JWT
def authenticate(session):
    url = "http://ceratti.4sales.com.br/api/Account/Authenticate"
    auth_data = {  # Alterado de 'payload' para 'auth_data'
        "tenancyName": "Ceratti",
        "usernameOrEmailAddress": "celonis",
        "password": "Celonis@2025"
    }
    headers = {"Content-Type": "application/json"}
    
    response = session.post(url, headers=headers, json=auth_data)
    response_data = response.json()
    
    if response.status_code == 200:
        print("Autenticação bem-sucedida.")
        token = response_data.get('result')
        print(f"Token obtido: {token}")
        return token
    else:
        print(f"Erro ao autenticar: {response_data}")
        return None

# Função para buscar orçamentos com reautenticação em caso de erro 401
def fetch_orders(session, token, json_data):
    url = "http://ceratti.4sales.com.br/api/services/app/order/GetOrderForReport"
    
    payload = {
        "initialDate": json_data["initialDate"],
        "endDate": json_data["endDate"],
        "maxResultCount": json_data["maxResultCount"]
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = session.post(url, headers=headers, json=payload)

    if response.status_code == 401:
        print("Token expirado ou inválido. Tentando reautenticar...")
        token = authenticate(session)
        
        if token:
            headers["Authorization"] = f"Bearer {token}"
            response = session.post(url, headers=headers, json=payload)
        else:
            print("Falha ao reautenticar.")
            return None

    if response.status_code == 200:
        print("Orçamentos obtidos com sucesso.")
        return response.json()
    else:
        print(f"Erro ao buscar orçamentos: {response.status_code}")
        print(f"Detalhes da resposta: {response.text}")
        return None

# Função para ler o arquivo JSON
def read_json_file(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# Função para salvar a resposta em um arquivo JSON
def save_response_to_file(response_data, filepath):
    with open(filepath, 'w') as file:
        json.dump(response_data, file, indent=4)

# Execução do script
# requests.Session mantem uma sessão persistente
with requests.Session() as session:
    token = authenticate(session)
    
    if token:
        json_data = read_json_file('E:\\Ceratti\\4Sales_Delta.json')
        orders = fetch_orders(session, token, json_data)

        if orders:
            save_response_to_file(orders, 'E:\\Ceratti\\4Sales_Get_Order.json')
            print("Resposta salva em '4Sales_Get_Order.json'.")
