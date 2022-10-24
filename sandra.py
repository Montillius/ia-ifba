import os
# Importando módulos
from tkinter import *
import json
import bs4
import requests
import sounddevice as sd
import speech_recognition as sr
import wavio as wv
from bs4 import BeautifulSoup
from gtts import gTTS
from playsound import playsound


#abre json
with open("dados_pessoais.json") as jsonFile:
    dados = json.load(jsonFile)
nome = dados['name']
idade = dados['age']
local = dados['local']


# Função de fala
def fala(text):
    global file1
    for i in range(0, 3):
        tts = gTTS(text, lang='pt')
        file1 = str("testandoaudio" + str(i) + ".mp3")
        tts.save(file1)
    playsound(file1, True)
    os.remove(file1)


def ia():
    # Importando arquivos de voz
    filename = "minhavoz.wav"
    falaia = "falaia.mp3"

    # Declarar globalmente a variável
    global says

    # Função de gravar áudio para reconhecimento.
    def grava():
        freq = 48000  # frequência
        duration = 7  # Duração de cada gravação
        recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
        print('Estou te ouvindo, pode falar!')
        sd.wait()
        wv.write("minhavoz.wav", recording, freq, sampwidth=2)
        print('Certo! Processando...')

    # Função de pegar informações sobre ativos
    def get_crypto_price(coin):
        url = "https://www.google.com/search?q=" + coin + "+hoje"
        HTML = requests.get(url)
        soup = bs4.BeautifulSoup(HTML.text, 'html.parser')
        text = soup.find("div", attrs={'class': 'BNeawe iBp4i AP7Wnd'}).find("div", attrs={
            'class': 'BNeawe iBp4i AP7Wnd'}).text
        print(f'O preço de {coin} é de {text}')
        fala(f'O preço de {coin} é de {text}')

    def get_action_winer():
        response = requests.get('https://economia.uol.com.br/cotacoes/bolsas/')
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='data-table')
        trs = table.find_all('tr')
        classificacoes = []
        for tr in trs:
            ativo = tr.find_all('td')
            classificacao = {
                ativo[0].find('a').text
            }
            classificacoes.append(classificacao)
        sigla = classificacoes[0]
        url = f"https://www.google.com/search?q={sigla}"
        HTML = requests.get(url)
        soup = BeautifulSoup(HTML.text, 'html.parser')
        result = soup.find('div',class_='BNeawe deIvCb AP7Wnd').text
        print(f'O ativo que mais valorizou no Brasil hoje, segundo a bovespa foi {result}')
        fala(f'O ativo que mais valorizou no Brasil hoje, segundo a bovespa foi {result}')

    def get_action_loser():
        response = requests.get('https://economia.uol.com.br/cotacoes/bolsas/')
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find_all('table', class_='data-table')[1]
        trs = table.find_all('tr')
        classificacoes = []
        for tr in trs:
            ativo = tr.find_all('td')
            classificacao = {
                ativo[0].find('a').text
            }
            classificacoes.append(classificacao)
        sigla = classificacoes[0]
        url = f"https://www.google.com/search?q={sigla}"
        HTML = requests.get(url)
        soup = BeautifulSoup(HTML.text, 'html.parser')
        result = soup.find('div', class_='BNeawe deIvCb AP7Wnd').text
        print(f'O ativo que mais desvalorizou no Brasil hoje, segundo a bovespa foi {result}')
        fala(f'O ativo que mais desvalorizou no Brasil hoje, segundo a bovespa foi {result}')

    while True:
        grava()

        # Iniciando o reconhecimento de fala
        r = sr.Recognizer()

        try:
            with sr.AudioFile(filename) as source:
                # "Escutando" o arquivo
                audio_data = r.record(source)
                # Convertendo de audio para texto
                says = r.recognize_google(audio_data, language='pt-BR')
                # Escrevendo o que foi dito.
                print('Você falou: ' + says.lower())
                texto = says.lower()

                # Desligar
                f = open('palavras_encerramento.txt', 'r')
                fec = f.read()
                if texto in fec:
                    fala('Ok! Desligando')
                    playsound('desligando.wav')
                    window.destroy()
                    break

                # Valor criptomoedas
                elif 'sandra valor hoje do' in texto:
                    coin = texto.replace('sandra valor hoje do', '')
                    get_crypto_price(coin)
                # Ativo que mais valorizou
                elif 'sandra qual ativo mais valorizou hoje' in texto:
                    get_action_winer()

                # Ativo que mais desvalorizou
                elif 'sandra qual ativo mais desvalorizou hoje' in texto:
                    get_action_loser()

                # funcoes que executam com texto do json
                elif 'bom dia' in texto:
                    fala(f'Bom dia {nome}"')

                elif 'qual a minha idade' in texto:
                    fala(f'Você tem {idade} anos')

                elif 'onde eu moro' in texto:
                    fala(f'Você mora em {local}')

        # Se ocorrer algum erro, retornará:
        except Exception as e:
            print('Este comando não é válido!')
            fala('Este comando não é válido!')


window = Tk()
window.title('Sandra - Assistente Virtual')
photo = PhotoImage(file=r"/home/otiliano/Documentos/assistentevirtual/icon_robot.png")
photo_image = photo.subsample(3, 3)
Button(window, text='Clique em mim!', image=photo_image, compound=LEFT, command=ia).pack(side=TOP)

mainloop()
