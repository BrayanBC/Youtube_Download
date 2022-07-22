''' Programa construído em um linux '''

from pytube import YouTube, Playlist
import subprocess, os 
from safe_filename import mod

#função para codificar so áudios de mp4 para mp3
def codec_mp3(p, f):
    print(f"{B}Codificando para MP3{W}")
    if p == "":
        subprocess.call([f"ffmpeg -i {f} -codec:a libmp3lame {f}.mp3"], shell=True)
        subprocess.call([f'rm {f}'], shell=True)
    else:
        os.chdir(p)
        subprocess.call([f'ls'], shell=True)
        subprocess.call([f"ffmpeg -i {f} -codec:a libmp3lame {f}.mp3"], shell=True)
        subprocess.call([f'rm {f}'], shell=True)

#função para baixar somente um vídeo
def video(link):
    video = YouTube(link)
    filename = mod(video.title)
    while True:
        seletor = input(f"Você deseja baixar o video {R}{filename}{W}? {C}[S][N]{W} ").upper()
        if seletor == "N":
            break
        if seletor == "S":
            pastas = subprocess.getoutput(["ls"]).split() 
            pastas = ", ".join(pastas)
            print(f"Qual a pasta dos vídeos? {C}{pastas}{W}")
            path = input("")
            video = video.streams.get_highest_resolution()
            video.download(output_path=path)
            print('Baixando o vídeo:', filename)
            break


#função para baixar somente uma música
def audio(link):
    audio = YouTube(link)
    filename = mod(audio.title)
    while True:
        seletor = input(f"Você deseja baixar a música {R}{filename}{W}? {C}[S][N]{W} ").upper()
        if seletor == "N":
            break
        if seletor == "S":
            audio = audio.streams.filter(only_audio=True)[0]
            pastas = subprocess.getoutput(["ls"]).split()
            pastas = ", ".join(pastas)
            path = input(f"Qual a pasta das músicas? {C}{pastas}{W} ")
            audio.download(output_path=path, filename=filename)
            print('Baixando a música:', filename)
            codec_mp3(path, filename)
            break


#função para baixar vários vídeos de uma playlist
def playlist_video(link):
    playlist = Playlist(link)
    nVideos = len(playlist.video_urls)
    print(f"A playlist tem {nVideos} videos!")
    while True:
        modo_playlist = input(f"Você deseja selecionar ou baixar todos os vídeos? {C}[S][T]{W} ").upper()
        if modo_playlist == "S" or "T":
            break
    pastas = subprocess.getoutput(["ls"]).split()
    pastas = ", ".join(pastas)
    path = input(f"Qual a pasta dos vídeos? {C}{pastas}{W} ")
    for url in playlist:
        video = YouTube(url)
        filename = mod(video.title)
        if modo_playlist == "S":
            while True:
                selecao = input(f"Você deseja baixar o vídeo {G}{filename}{W}? {C}[S][N]{W} ").upper()
                if selecao == "S" or "N":
                    break
            if selecao == "N":
                continue
        if modo_playlist == "T":
            print(f"{G}Ok, irei baixar todos os vídeos!{W}")
        print(f'Baixando o vídeo {C}{filename}{W} ...')
        video = video.streams.get_highest_resolution()
        video.download(output_path=path)


#função para baixar várias músicas de alguma playlist	
def playlist_audio(link):
    playlist = Playlist(link)
    n = len(playlist.video_urls)
    print(f"A playlist tem {n} músicas!")
    while True:
        modo_playlist = input(f"Você deseja selecionar ou baixar todas as músicas? \033[36m[S][T]{W} ").upper()
        if modo_playlist == "S" or "T":
            break
    pastas = subprocess.getoutput(["ls"]).split()
    pastas = ", ".join(pastas)
    path = input(f"Qual a pasta das músicas? {C}{pastas}{W} ")
    for url in playlist:
        audio = YouTube(url)
        filename = mod(audio.title)
        if modo_playlist == "S":
            while True:
                selecao = input(f"Você deseja baixar a música {R}{filename}{W}? {C}[S][N]{W} ").upper()
                if selecao == "S" or "N":
                    break
            if selecao == "N":
                continue
            if modo_playlist == "T":
                print(f"{G}Ok, irei baixar todas as músicas!{W}")
        audio = audio.streams.filter(only_audio=True)[0]
        audio.download(output_path=path, filename = filename)
        print('Baixando a música:', filename)
        print(path)
        print(type(path))
        codec_mp3(path, filename)



#cores
BK = "\033[30m"; R = "\033[31m"; G = "\033[32m"; Y = "\033[33m"; B = "\033[34m"; L = "\033[35m"; C = "\033[36m"; W = "\033[0;0m"

#chamada das funções, script nominal
while True:
    modo_arquivo = input(f"Você deseja instalar músicas {C}[M]{W} ou vídeos {C}[V]{W}? ").upper()
    if modo_arquivo == "M":
        while True:
            tipo = input(f"Digite {C}[A]{W} para somente um audio ou {C}[P]{W} para playlist: ").upper()
            if tipo == "A":
                print("Digite a URL da música:")
                try:
                    audio(input(">>> "))
                    break
                except:
                    print(f"{R}Talvez você tenha digitado errado {W}")
            if tipo == "P":	
                try:
                    print(f'Digite a URL da playlist: \n Examples \n {ExampleM.read()}')
                    ExampleM.close()
                except:
                    print('Digite outra URL: ')
                finally:
                    playlist_audio(input(">>> "))
                    break
    if modo_arquivo == "V":
        while True:
            tipo = input(f"Digite {C}[V]{W} para somente um vídeo ou {C}[P]{W} para playlist: ").upper()
            if tipo == "V":
                print("Digite a URL do video:")
                video(input(">>> "))
                break
            if tipo == "P":
                print('Digite a URL da playlist:')
                playlist_video(input(">>> "))
                break
