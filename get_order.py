import requests
import json

# Função para autenticar e obter o token JWT
def authenticate():
    url = "http://ceratti.4sales.com.br/api/Account/Authenticate"
    payload = {
        "tenancyName": "Ceratti",
        "usernameOrEmailAddress": "celonis",
        "password": "Celonis@2025"
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()
    
    if response.status_code == 200:
        print("Autenticação bem-sucedida.")
        return response_data['result']  # Retorna o token JWT
    else:
        print(f"Erro ao autenticar: {response_data}")
        return None

# Função para buscar orçamentos
def fetch_orders(token, json_data):
    url = "http://ceratti.4sales.com.br/api/services/app/order/GetOrderForReport"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Estrutura do payload com os parâmetros necessários
    payload = {
        #"orderId": None,  # Pode ser None se não for necessário
        "initialDate": json_data["initialDate"],
        "endDate": json_data["endDate"],
        "maxResultCount": json_data["maxResultCount"],
        #"skipCount": 0,  # Para obter a primeira página
        #"sorting": "creationTime"  # Ajuste se necessário
    }

    # Fazendo a requisição POST com os dados do JSON
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Orçamentos obtidos com sucesso.")
        return response.json()  # Retorna os dados dos orçamentos
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
        json.dump(response_data, file, indent=4)  # Salva com formatação

# Execução do script
token = authenticate()
if token:
    json_data = read_json_file('E:\\Ceratti\\4Sales_Delta.json')  # Caminho do arquivo JSON
    orders = fetch_orders(token, json_data)

    if orders:  # Verifica se os pedidos foram obtidos
        # Salva a resposta da API em '4Sales_Get_Order.json'
        save_response_to_file(orders, 'E:\\Ceratti\\4Sales_Get_Order.json')
        print("Resposta salva em '4Sales_Get_Order.json'.")