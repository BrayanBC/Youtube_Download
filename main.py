from pytube import YouTube, helpers, Playlist
import subprocess


def codec_mp3(p, f):
	print("\033[34mCodificando para MP3\033[0;0m")
	subprocess.call([f"ffmpeg -i \'{p}/{f}.mp4\' -codec:a libmp3lame \'{p}/{f}.mp3\'"], shell=True)
	subprocess.call([f'rm \'{p}/{f}.mp4\'', '-Rf'], shell=True)


def audio(link):
	audio = YouTube(link)
	filename = (helpers.safe_filename(audio.title)).replace("  " or "   ", " - ")
	print('Baixando a música:', filename)
	audio = audio.streams.filter(only_audio=True)[0]
	pastas = subprocess.getoutput(["ls"]).split()
	pastas = ", ".join(pastas)
	path = input(f"Qual a pasta das músicas? \033[36m{pastas}\033[0;0m ")
	audio.download(output_path=path, filename="\'"+filename+"\'")
	codec_mp3(path, filename)
	
	
def playlist_audio(link):
	playlist = Playlist(link)
	while True:
		modo_playlist = input(f"Você deseja selecionar ou baixar todas as músicas? \033[36m[S][T]\033[0;0m ").upper()
		if modo_playlist == "S" or "T":
			break
	pastas = subprocess.getoutput(["ls"]).split()
	pastas = ", ".join(pastas)
	path = input(f"Qual a pasta das músicas? \033[36m{pastas}\033[0;0m ")
	for url in playlist:
		audio = YouTube(url)
		filename = (helpers.safe_filename(audio.title)).replace("  " or "   ", " - ")
		if modo_playlist == "S":
			while True:
				selecao = input(f"Você deseja baixar a música \033[32m{filename}\033[0;0m? \033[36m[S][N]\033[0;0m ").upper()
				if modo_playlist == "S" or "N":
					break
			if selecao == "N":
				continue
			if modo_playlist == "T":
				print("\033[32mOk, irei baixar todas as músicas!\033[0;0m")

		print(f'Baixando a música \033[36m{filename}\033[0;0m ...')
		audio = audio.streams.filter(only_audio=True)[0]
		audio.download(output_path=path, filename="\'"+filename+"\'")
		codec_mp3(path, filename)
	

def video(link):
	video = YouTube(link)
	filename = video.title
	print('Baixando o vídeo:', filename)
	pastas = subprocess.getoutput(["ls"]).split()
	pastas = ", ".join(pastas)
	path = input(f"Qual a pasta dos vídeos? \033[36m{pastas}\033[0;0m ")
	video = video.streams.get_highest_resolution()
	video.download(output_path=path)
	

def playlist_video(link):
	playlist = Playlist(link)
	while True:
		modo_playlist = input(f"Você deseja selecionar ou baixar todos os vídeos? \033[36m[S][T]\033[0;0m ").upper()
		if modo_playlist == "S" or "T":
			break
	pastas = subprocess.getoutput(["ls"]).split()
	pastas = ", ".join(pastas)
	path = input(f"Qual a pasta dos vídeos? \033[36m{pastas}\033[0;0m ")
	for url in playlist:
		video = YouTube(url)
		filename = video.title
		if modo_playlist == "S":
			while True:
				selecao = input(f"Você deseja baixar o vídeo \033[32m{filename}\033[0;0m? \033[36m[S][N]\033[0;0m ").upper()
			if modo_playlist == "S" or "N":
				break
			if selecao == "N":
				continue
		if modo_playlist == "T":
			print("\033[32mOk, irei baixar todas as músicas!\033[0;0m")
		print(f'Baixando o vídeo \033[36m{filename}\033[0;0m ...')
		video = video.streams.get_highest_resolution()
		video.download(output_path=path)


while True:
	modo_arquivo = input("Você deseja instalar músicas \033[36m[M]\033[0;0m ou vídeos \033[36m[V]\033[0;0m? ").upper()
	if modo_arquivo == "M":
		while True:
			tipo = input("Digite \033[36m[A]\033[0;0m para somente um audio ou \033[36m[P]\033[0;0m para playlist: ").upper()
			if tipo == "A":
				audio(input("Digite a URL do link: "))
				break
			if tipo == "P":
				playlist_audio(input("Digite a URL da playlist: "))
				break
		break
	if modo_arquivo == "V":
		while True:
			tipo = input("Digite \033[36m[V]\033[0;0m para somente um vídeo ou \033[36m[P]\033[0;0m para playlist: ").upper()
			if tipo == "V":
				video(input("Digite a URL do link: "))
				break
			if tipo == "P":
				playlist_video(input("Digite a URL da playlist: "))
				break
