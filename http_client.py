import requests

class HttpClient:

    @staticmethod
    def Get(url_address, params):
        response = requests.get(url = url_address, params=params, verify = False)
        if response.status_code != 200:
            response.close()
            return None

        response.close()
        return response.content

    @staticmethod
    def Post(url_address, post_json):
        response = requests.post(url = url_address, data=post_json, verify = False)

        if response.status_code != 200:
            response.close()
            return None

        response.close()
        return response.content
