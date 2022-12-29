import requests


class SalesforceAPI:
    def __init__(self, account_name, client_id, client_secret, client_token):
        self.host = "https://monetusbr.my.salesforce.com"
        self.token = self.make_access_token(account_name, client_id, client_secret, client_token)

    @staticmethod
    def make_access_token(account_name, client_id, client_secret, client_token):
        payload=f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
        headers = {
        'Authorization': f'Bearer {client_token}',
        'Content-Type': 'application/x-www-form-urlencoded',
        }
        url = f"https://{account_name}.my.salesforce.com/services/oauth2/token"

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()["access_token"]


    def make_query(self, query):
        
        url = f"{self.host}/services/data/v56.0/query?q={query}"
        headers = {
        'Authorization': f'Bearer {self.token}'
        }

        all_data = []
        counter = 1
        while True:
            resp = requests.request("GET", url, headers=headers).json()
            all_data.extend(resp["records"]) 
            print(f"Extracting {counter} page: {len(resp['records'])} records")

            if resp["done"] == False:
                url = f"{self.host}{resp['nextRecordsUrl']}"
            else:
                break
            counter += 1

        return all_data

