from pytube import YouTube, helpers, Playlist
import subprocess


def codec_mp3(p, f):
	print("\033[34mCodificando para MP3\033[0;0m")
	subprocess.call([f"ffmpeg -i \'/home/brayan/Música/{p}/{f}.mp4\' -codec:a libmp3lame \'/home/brayan/Música/{p}/{f}.mp3\'"], shell=True)
	subprocess.call([f'rm \'/home/brayan/Música/{p}/{f}.mp4\'', '-Rf'], shell=True)


def audio(link):
	audio = YouTube(link)
	filename = (helpers.safe_filename(audio.title)).replace("  " or "   ", " - ")
	print('Baixando a música:', filename)
	audio = audio.streams.filter(only_audio=True)[0]
	pastas = subprocess.getoutput(["ls ~/Música/"]).split()
	pastas = ", ".join(pastas)
	path = input(f"Qual a pasta das músicas? \033[36m{pastas}\033[0;0m ")
	audio.download(output_path=f'~/Música/{path}', filename="\'"+filename+"\'")
	codec_mp3(path, filename)
	
	
def playlist(link):
	playlist = Playlist(link)
	while True:
		modo_playlist = input(f"Você deseja selecionar ou baixar todas as músicas? \033[36m[S][T]\033[0;0m ").upper()
		if modo_playlist == "S" or "T":
			break
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
		pastas = subprocess.getoutput(["ls ~/Música/"]).split()
		pastas = ", ".join(pastas)
		path = input(f"Qual a pasta das músicas? \033[36m{pastas}\033[0;0m ")
		audio.download(output_path=f'~/Música/{path}', filename="\'"+filename+"\'")
		codec_mp3(path, filename)
		
		
while True:
	tipo = input("Digite [V] para vídeo ou [P] para playlist: ").upper()
	if tipo == "V":
		audio(input("Digite a URL do link: "))
		break
	if tipo == "P":
		playlist(input("Digite a URL da playlist: "))
		break
	
