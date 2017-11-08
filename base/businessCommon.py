from base import common
from base import configHttp
import readConfig as readConfig
import json
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
# login
def login():
    """
    login
    :return: token
    """
    # set url
    url = common.get_url_from_xml('LTClogin')
    localConfigHttp.set_url(url)

    # set header
    header = {"Content-type": "application/json"}
    localConfigHttp.set_headers(header)

    # set param
    param = {
	"CommandCode": "MobileUserLogin",
	"Marker": "ytc",
	"TransferData": "{\"password\":\"Uc8IqZ9nxg2E9dCLd34PcA\\u003d\\u003d\",\"phoneNo\":\"13249824552\"}"
}
    data = json.dumps(param)
    localConfigHttp.set_data(data)

    # login
    response = localConfigHttp.post().json()
    token = common.get_value_from_return_json(response, 'ResultInfo', "tokenNo")
    return token

# logout
def logout(token):
    """
    logout
    :param token: login token
    :return:
    """
    # set url
    url = common.get_url_from_xml('LTClogin')
    localConfigHttp.set_url(url)

    # set header
    header = {"Content-type": "application/json"}
    localConfigHttp.set_headers(header)

    #set data
    # set param
    param = {"CommandCode":"MobileUserLogout","Marker":token,"TransferData":"17"}
    data = json.dumps(param)
    localConfigHttp.set_data(data)
    # logout
    localConfigHttp.post()

if __name__=='__main__':
    print (login())
