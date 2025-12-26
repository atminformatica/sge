import requests

class Notify:
    def __init__(self):
        #self.__base_url = f'https://webhook.site'
         self.__base_url = f'http://localhost:8001'

    def send_order_event(self, data):
        response = requests.post(
            # url=f'{self.__base_url}/39106885-3d2d-4f03-889e-521667bc36eb',
            url=f'{self.__base_url}/api/v1/webhooks/order/',
            json=data,
        )
       

