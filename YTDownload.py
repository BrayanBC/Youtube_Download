''' Programa construído em um linux ubuntu'''

from pytube import YouTube, helpers, Playlist
import subprocess, requests, os, re

usuario = subprocess.getoutput(["whoami"])
os.chdir(f'/home/{usuario}/Música')

try:
	ExampleM = open("/home/brayan/Documentos/Cursos/python/Youtube_Download/Playlist.txt", "r")
	ExampleV = open("/home/brayan/Documentos/Cursos/python/Youtube_Download/Videos.txt", "r")
except:
	print(f"Bem Vindo {usuario}")

#cores
BK = "\033[30m"; R = "\033[31m"; G = "\033[32m"; Y = "\033[33m"; B = "\033[34m"; L = "\033[35m"; C = "\033[36m"; W = "\033[0;0m"


#função para codificar so áudios de mp4 para mp3
def codec_mp3(p, f):
	print(f"{B}Codificando para MP3{W}")
	subprocess.call([f"ffmpeg -i \'{p}/{f}.mp4\' -codec:a libmp3lame \'{p}/{f}.mp3\'"], shell=True)
	subprocess.call([f'rm \'{p}/{f}.mp4\'', '-Rf'], shell=True)
			
				
#função para baixar somente um vídeo
def video(link):
	video = YouTube(link)
	filename = (helpers.safe_filename(video.title)).replace("  " or "   ", " - ")
	while True:
		seletor = input(f"Você deseja baixar o video {R}{filename}{W}? {C}[S][N]{W} ").upper()
		if seletor == "N":
			break
		if seletor == "S":
			pastas = subprocess.getoutput(["ls"]).split()
			pastas = ", ".join(pastas)
			path = input(f"Qual a pasta dos vídeos? {C}{pastas}{W} ")
			video = video.streams.get_highest_resolution()
			video.download(output_path=path)
			print('Baixando o vídeo:', filename)
			break


#função para baixar somente uma música
def audio(link):
	audio = YouTube(link)
	filename = (helpers.safe_filename(audio.title)).replace("  " or "   ", " - ")
	while True:
		seletor = input(f"Você deseja baixar a música {R}{filename}{W}? {C}[S][N]{W} ").upper()
		if seletor == "N":
			break
		if seletor == "S":
			audio = audio.streams.filter(only_audio=True)[0]
			pastas = subprocess.getoutput(["ls"]).split()
			pastas = ", ".join(pastas)
			path = input(f"Qual a pasta das músicas? {C}{pastas}{W} ")
			audio.download(output_path=path, filename="\'"+filename+"\'")
			print('Baixando a música:', filename)
			codec_mp3(path, filename)
			break
	

#se a playlist tivver mais de 100 url	
def erro_playlist(url, modo_arquivo):
	link = requests.get(url)
	url = re.findall(r'(\/watch\?v\=.{56})', link.text)
	for i in url:
		try:
			if modo_arquivo == "M":
				audio(f"www.youtube.com{i}")
			if modo_arquivo == "V":
				video(f"www.youtube.com{i}")
		except:
			print(f"{R}Talvez você tenha digitado errado {W}")
	
	
#função para baixar vários vídeos de uma playlist
def playlist_video(link):
	playlist = Playlist(link)
	n = len(playlist.video_urls)
	print(f"A playlist tem {n} videos!")
	if n > 99:
		erro_playlist(link, 'V')
	while True:
		modo_playlist = input(f"Você deseja selecionar ou baixar todos os vídeos? {C}[S][T]{W} ").upper()
		if modo_playlist == "S" or "T":
			break
	pastas = subprocess.getoutput(["ls"]).split()
	pastas = ", ".join(pastas)
	path = input(f"Qual a pasta dos vídeos? {C}{pastas}{W} ")
	for url in playlist:
		video = YouTube(url)
		filename = video.title
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
	if n > 99:
		erro_playlist(link, 'M')
	while True:
		modo_playlist = input(f"Você deseja selecionar ou baixar todas as músicas? \033[36m[S][T]{W} ").upper()
		if modo_playlist == "S" or "T":
			break
	pastas = subprocess.getoutput(["ls"]).split()
	pastas = ", ".join(pastas)
	path = input(f"Qual a pasta das músicas? {C}{pastas}{W} ")
	for url in playlist:
		audio = YouTube(url)
		filename = (helpers.safe_filename(audio.title)).replace("  " or "   ", " - ")
		if modo_playlist == "S":
			while True:
				selecao = input(f"Você deseja baixar a música {G}{filename}{W}? {C}[S][N]{W} ").upper()
				if selecao == "S" or "N":
					break
			if selecao == "N":
				continue
			if modo_playlist == "T":
				print(f"{G}Ok, irei baixar todas as músicas!{W}")
		print(f'Baixando a música {C}{filename}{W} ...')
		audio = audio.streams.filter(only_audio=True)[0]
		audio.download(output_path=path, filename="\'"+filename+"\'")
		codec_mp3(path, filename)


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
				print(f'Digite a URL da playlist: \n Examples \n {ExampleM.read()}')
				playlist_audio(input(">>> "))
				break
	if modo_arquivo == "V":
		while True:
			tipo = input(f"Digite {C}[V]{W} para somente um vídeo ou {C}[P]{W} para playlist: ").upper()
			if tipo == "V":
				print("Digite a URL do video:")
				try:
					video(input(">>>"))
					break
				except:
					print(f"{R}Talvez você tenha digitado errado {W}")
			if tipo == "P":
				try:
					print(f'Digite a URL da playlist: \n Examples \n {ExampleV.read()}')
					playlist_video(input(">>> "))
					break
				except: 
					print(f"{R}Talvez você tenha digitado errado {W}")
