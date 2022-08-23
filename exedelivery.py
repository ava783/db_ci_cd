import smbclient
import requests
import os
import sys

   
def nexus(node):
    headers = {
        'authority': '<HIDDEN>',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'cookie': 'NX-ANTI-CSRF-TOKEN=0.6610776800136398; ajs_user_id=%22b83769d6db734c06ea50af5c7b60bc98d68e1f45%22; ajs_anonymous_id=%22994f2e40-9b42-4819-b7e0-a510da1abf1e%22; _ga=GA1.1.1647449599.1644929411; _ga_9HBSWH8GRN=GS1.1.1654766593.12.1.1654767523.0; sso_1569167177589=_f36ccb2b-6448-46be-a0cc-f8529c623050; NXSESSIONID=d5706ec6-8c58-4f61-abe7-c49822950257',
        'nx-anti-csrf-token': '0.6610776800136398',
        'origin': 'https://<HIDDEN>',
        'referer': 'https://<HIDDEN>/',
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

    data = '{"action":"coreui_Browse","method":"read","data":[{"repositoryName":"krsua-raw","node":"'+str(node)+'"}],"type":"rpc","tid":11}'

    response = requests.post('https://<HIDDEN>/service/extdirect', headers=headers, data=data, verify=False).json()
    return response.get('result').get('data')

def download(id):
    f=requests.get('https://<HIDDEN>/repository/krsua-raw/'+str(id), verify=False, allow_redirects=True)
    return f.content

def upload(name, content):
    with smbclient.open_file(addres+str('\\')+name, mode='wb') as file:
        file.write(content)

def upgrade():
    st=[]
    stb=[]
    for x in nexus('<HIDDEN>'):
        st.append(x.get('id'))
        #print(x)
    for xx in nexus(st[-1]):
        stb.append(xx.get('id'))
    print("Будет установлен релиз: "+stb[-1])
    for i in nexus(stb[-1]):
        cont=download(i.get('id'))
        upload(i.get('text'), cont)
        print('Файл '+i.get('text')+' обновлен')

def downgrage_release():
    st=[]
    stb=[]
    for x in nexus('<HIDDEN>'):
        st.append(x.get('id'))
        #print(x)
    for xx in nexus(st[-2]):
        stb.append(xx.get('id'))
    print("Откат на предыдущий релиз: "+stb[-1])
    for i in nexus(stb[-1]):
        cont=download(i.get('id'))
        upload(i.get('text'), cont)
        print('Файл '+i.get('text')+' обновлен')

def downgrage_build():
    st=[]
    stb=[]
    for x in nexus('<HIDDEN>'):
        st.append(x.get('id'))
        #print(x)
    for xx in nexus(st[-1]):
        stb.append(xx.get('id'))
    print("Откат на предыдущий билд: "+stb[-2])
    for i in nexus(stb[-2]):
        cont=download(i.get('id'))
        upload(i.get('text'), cont)
        print('Файл '+i.get('text')+' обновлен')

def status():
    st=[]
    stb=[]
    stb2=[]
    for x in nexus('<HIDDEN>'):
        st.append(x.get('id'))
        #print(x)
    for xx in nexus(st[-1]):
        stb.append(xx.get('id'))
    print("Будет установлен релиз: "+stb[-1])
    try:
        print("Откат на предыдущий билд: "+stb[-2])
    except:
        print("Откат на предыдущий билд невозможен")
    for xx in nexus(st[-2]):
        stb2.append(xx.get('id'))
    print("Откат на предыдущий релиз: "+stb2[-1])

def main():
    smbclient.ClientConfig(username='deploy_client', password=os.getenv('SMB_PASS'))
    
def check_addres():
    try:
        addres=r'\\V00filenet02nod.<HIDDEN>\Public\prm'
        smbclient.listdir(addres)
    except ValueError:
        addres=r'\\V00filenet04nod.<HIDDEN>\Public\prm'
        smbclient.listdir(addres)
    print('Для подключения используется '+addres)
    return addres
    
if __name__ == '__main__':
    main()
    addres=check_addres()
    if sys.argv[1]=='update':
        upgrade()
    elif sys.argv[1]=='down_release':
        downgrage_release()
    elif sys.argv[1]=='down_build':
        downgrage_build()
    elif sys.argv[1]=='status':
        status()
    else:
        print("Неверно указан аргумент")