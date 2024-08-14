import PySimpleGUI as sg
import json
import os
from pytube import YouTube

def apply_styles():
    sg.theme('DarkPurple')

def registration_layout():
    return [
        [sg.Text('Registre-se', font=('Arial', 20), text_color='white', background_color='#2e003e')],
        [sg.Text('Nome de usuário:', size=(15, 1), text_color='white', background_color='#2e003e'), sg.Input(key='username', size=(30, 1), pad=(10, 5), background_color='#3d3d3d', text_color='#000000')],
        [sg.Text('Senha:', size=(15, 1), text_color='white', background_color='#2e003e'), sg.Input(key='password', password_char='*', size=(30, 1), pad=(10, 5), background_color='#3d3d3d', text_color='#000000')],
        [sg.Button('Cadastrar', button_color=('white', '#6a0dad'))],
        [sg.Text('Já tenho login', text_color='white', background_color='#2e003e', enable_events=True, key='to_login')],
        [sg.Text('', key='message', text_color='red', background_color='#2e003e')]
    ]

def login_layout():
    return [
        [sg.Text('Login', font=('Arial', 20), text_color='white', background_color='#2e003e')],
        [sg.Text('Nome de usuário:', size=(15, 1), text_color='white', background_color='#2e003e'), sg.Input(key='username', size=(30, 1), pad=(10, 5), background_color='#3d3d3d', text_color='#000000')],
        [sg.Text('Senha:', size=(15, 1), text_color='white', background_color='#2e003e'), sg.Input(key='password', password_char='*', size=(30, 1), pad=(10, 5), background_color='#3d3d3d', text_color='#000000')],
        [sg.Button('Entrar', button_color=('white', '#6a0dad'))],
        [sg.Text('Voltar ao cadastro', text_color='white', background_color='#2e003e', enable_events=True, key='to_register')],
        [sg.Text('', key='message', text_color='red', background_color='#2e003e')]
    ]

def download_layout():
    return [
        [sg.Text('STREAMLINE', font=('Arial', 20), text_color='white', background_color='#2e003e')],
        [sg.Text('Cole o link do vídeo:', text_color='white', background_color='#2e003e'), sg.Input(key='url')],
        [sg.Text('Escolha a resolução:', text_color='white', background_color='#2e003e'), sg.Combo(['720p', '480p', '360p'], key='resolution')],
        [sg.Text('Escolha o diretório:', text_color='white', background_color='#2e003e'), sg.Input(key='folder'), sg.FolderBrowse()],
        [sg.Button('Baixar', button_color=('white', '#6a0dad'))],
        [sg.Text('', key='message', text_color='red', background_color='#2e003e')]
    ]

def save_user_data(username, password):
    data = {'username': username, 'password': password}
    with open('user_data.json', 'w') as f:
        json.dump(data, f)

def load_user_data():
    if os.path.exists('user_data.json'):
        with open('user_data.json', 'r') as f:
            return json.load(f)
    return None

def download_video(url, resolution, folder):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(res=resolution).first()
        if stream:
            stream.download(output_path=folder)
            return 'Vídeo baixado com sucesso!'
        else:
            return 'Resolução não disponível!'
    except Exception as e:
        return f'Erro: {e}'

def main():
    apply_styles()

    layout = registration_layout()
    window = sg.Window('STREAMLINE - Registro', layout, size=(400, 300))

    user_data = load_user_data()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == 'Cadastrar':
            username = values['username'].strip()
            password = values['password'].strip()
            save_user_data(username, password)
            window.close()
            window = sg.Window('STREAMLINE - Login', login_layout(), size=(400, 300))

        elif event == 'to_login':
            window.close()
            window = sg.Window('STREAMLINE - Login', login_layout(), size=(400, 300))

        elif event == 'Entrar':
            username = values['username'].strip()
            password = values['password'].strip()
            if user_data and user_data['username'] == username and user_data['password'] == password:
                window.close()
                window = sg.Window('STREAMLINE - Download', download_layout(), size=(400, 300))
            else:
                window['message'].update('Usuário ou senha incorretos!')

        elif event == 'to_register':
            window.close()
            window = sg.Window('STREAMLINE - Registro', registration_layout(), size=(400, 300))

        elif event == 'Baixar':
            url = values['url']
            resolution = values['resolution']
            folder = values['folder']
            print(f'Caminho do diretório: {folder}')
            message = download_video(url, resolution, folder)
            window['message'].update(message)

    window.close()

if __name__ == '__main__':
    main()
