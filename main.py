import requests
import sys
import os

def api(reponame, node):
    cookies = {
        'NX-ANTI-CSRF-TOKEN': '0.6610776800136398',
        'ajs_user_id': '%22b83769d6db734c06ea50af5c7b60bc98d68e1f45%22',
        'ajs_anonymous_id': '%22994f2e40-9b42-4819-b7e0-a510da1abf1e%22',
        '_ga': 'GA1.1.1647449599.1644929411',
        '_ga_9HBSWH8GRN': 'GS1.1.1654766593.12.1.1654767523.0',
        'sso_1569167177589': '_3d6b9116-493a-41ab-b6ec-f7871afc8442',
        'NXSESSIONID': 'a6f29a15-8d9d-4997-b35b-a34fffe92595',
    }

    headers = {
        'authority': 'repo.<HIDDEN>.ru',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'nx-anti-csrf-token': '0.6610776800136398',
        'origin': 'https://repo.<HIDDEN>.ru',
        'referer': 'https://repo.<HIDDEN>.ru/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'x-nexus-ui': 'true',
        'x-requested-with': 'XMLHttpRequest',
    }

    json_data = {
        'action': 'coreui_Browse',
        'method': 'read',
        'data': [
            {
                'repositoryName': reponame,
                'node': node,
            },
        ],
        'type': 'rpc',
        'tid': 7,
    }
    
    response = requests.post('https://repo.<HIDDEN>.ru/service/extdirect', cookies=cookies, headers=headers, json=json_data, verify=False).json()
    return response

def download(name, node):
    f=requests.get('https://repo.<HIDDEN>.ru/repository/krsua-raw/'+node+'/'+name, verify=False, allow_redirects=True)
    with open(name, 'wb') as file:
        file.write(f.content)

if __name__ == '__main__':
    spis=[]
    response=api('krsua-raw', sys.argv[1])
    data=response.get('result').get('data')
    for i in data:
        spis.append(i.get('text'))
    if sys.argv[2] == 'status':
        print('Список релизов в репозитории:', end=' ')
        for fi in spis:
            print(fi.split('.zip')[0], end=', ')
        print(' ')
        print('Последняя версия релиза, которая будет установлена: '+max(spis).split('.zip')[0])
    elif sys.argv[2] == 'load':
        print('downloaded '+max(spis), sys.argv[1])
        download(max(spis), sys.argv[1])
        os.system('unzip '+max(spis))
