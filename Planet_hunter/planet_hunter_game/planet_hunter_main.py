#Caçador de Planetas(Jogo da Nave)

import tkinter as tk     #permite usar a interface di tkinter
from PIL import Image, ImageTk # permite colocar imagens
import requests #Para dar fetch a Api da Nasa
import random as R # para usar a função random
import threading #para usar threads para evitar que o jogo trave
import os #permite ir buscar conteudos as pastas
import pygame # para a musica
import math

pygame.mixer.init() #Para poder dar o som

pontos_planeta = 1 # pontos de cada planeta
velocidade_base = 5 #velocidade base dos planetas
level_up_points = 10 #pontos para Subir o primeiro nivel
tminplaneta, tmaxplaneta = 20, 60 #tamanho maximo e minimo dos planetas
nave_largura, nave_altura = 50, 40 #largura e altura da nave
largura, altura = 800, 600 #largura e altura da tela
level = 1 #marcador de nivel
pontuacao = 0 #pontuação inicial
running = False #se o jogo esta a correr
em_boss = False #se esta em fase de boss
url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name+from+pscomppars+where+disc_year+>+2010&format=json"  #link da API
planetas = [] #array dos palnetas
cores_planetas = ["white", "yellow", "orange", "lightblue", "violet", "orange"] #fundo dos palnetas
formas_planeta = ["🌑", "🪐", "🪐", "🌀", "🌀", "✨", "✨", "✨"] #forma dos planetas
fundo_cores = ["orange", "darkblue", "midnightblue", "darkslategray", "navy", "purple"] #fundos do jogo
nome_planeta = "A Procurar..." #antiga mensagem de fallback
nomes_bosses = ["Titanus Prime", "Spectra", "Doppelvoid"] #nome dos boss
fundo_img = ["imagens_proj/menub.jpg",
             "imagens_proj/boss1.jpg",
             "imagens_proj/estrelas1.jpg",
             "imagens_proj/boss2.jpg",
             "imagens_proj/estrelas2.jpg",
             "imagens_proj/boss3.jpg",
             ] #array das imagens de fundo

musica_canal = None
boss_atual = -1 #para ir buscar o boss
boss_elementos = [] #array de elementos do boss

musica_principal_path = os.path.join("imagens_proj", "level_music.mp3") #musica principla do jogo
musicas_boss = [
    os.path.join("imagens_proj", "boss_music.mp3"),
    os.path.join("imagens_proj", "boss_music.mp3"),
    os.path.join("imagens_proj", "boss_music.mp3")
] #musica dos bosses

musica_vitoria_path = os.path.join("imagens_proj", "victory.mp3") #musica de vitoria
musica_pos = 0

fundo_nivel_objeto = None
fundo_nivel_id = None
bg_item_final = fundo_img[5]

fade_in_ativo = False
fade_volume = 0.0
fade_step = 0.02


def fade_in_musica():  # Função para aumentar gradualmente o volume da música
    global fade_in_ativo, fade_volume  # Chama as variaveis globais
    if fade_in_ativo and fade_volume < 1.0:  # Se o fade in está ativo e o volume atual é menor que o máximo (1.0)
        fade_volume = min(1.0, fade_volume + fade_step)  # Aumenta o volume gradualmente usando 'fade_step', sem ultrapassar 1.0
        pygame.mixer.music.set_volume(fade_volume)  # Define o novo volume da música no mixer do Pygame
        if fade_volume < 1.0:  # Se o volume ainda não atingiu o máximo
            ecranave.after(50, fade_in_musica)  # Chama esta função novamente após 50 milissegundos (utilizando metodo .after)
        else:
            fade_in_ativo = False  # Se o volume chegou a 1.0, desativa o fade in



def atualizar_fundo():
    global fundo_nivel_objeto, fundo_nivel_id  # chama as variaveis globais

    if level <= len(fundo_img):  # Garante que há uma imagem de fundo correspondente ao nível atual
        canvas_width = canvas.winfo_width()  # Obtém a largura atual
        canvas_height = canvas.winfo_height()  # Obtém a altura atual

        if canvas_width < 10 or canvas_height < 10:  # Se as dimensões forem muito pequenas
            ecranave.after(50, atualizar_fundo)  # Reagenda a função para tentar novamente após 50ms
            return  # Encerra a execução atual

        img_path = fundo_img[level - 1]  # Caminho da imagem do nível atual
        imagem = Image.open(img_path)  # Abre a imagem
        imagem = imagem.resize((canvas_width, canvas_height))  # Redimensiona a imagem para caber no canvas
        fundo_nivel_objeto = ImageTk.PhotoImage(imagem)  # Converte a imagem para o formato que o Tkinter pode exibir

        if fundo_nivel_id is None:  # Se ainda não foi criado um fundo
            fundo_nivel_id = canvas.create_image(0, 0, anchor="nw", image=fundo_nivel_objeto)  # Cria a imagem no canto superior esquerdo
        else:
            canvas.itemconfig(fundo_nivel_id, image=fundo_nivel_objeto)  # Atualiza a imagem existente

        # Garante que os elementos importantes fiquem sobre o fundo
        if 'nave' in globals():
            canvas.tag_raise(nave)
        if 'nave_emoji' in globals():
            canvas.tag_raise(nave_emoji)
        if 'score_text' in globals():
            canvas.tag_raise(score_text)
        if 'level_text' in globals():
            canvas.tag_raise(level_text)



def nome_planeta_fetch():
    global nome_planeta, level  # Usa as variáveis globais
    try:
        data = requests.get(url).json()  # Faz requisição HTTP e obtém os dados em JSON
        if isinstance(data, list) and len(data) > level:  # Garante que o índice existe
            nome_planeta = data[level].get('pl_name', "Desconhecido")  # Obtém o nome do planeta no nível atual
        else:
            nome_planeta = "Desconhecido"  # Fallback se não houver planeta correspondente
    except:
        nome_planeta = "Desconhecido"  # Em caso de erro na requisição

    if 'canvas' in globals() and 'level_text' in globals():  # Garante que os elementos existem
        canvas.itemconfig(level_text, text=f"Nivel {level}: {nome_planeta}")  # Atualiza o texto exibido no canvas



def move_nave(dy):  # Move a nave verticalmente com deslocamento 'dy'
    x1, y1, x2, y2 = canvas.coords(nave)  # Obtém as coordenadas da nave
    novoy1 = max(0, y1 + dy)  # Garante que o topo da nave não ultrapasse o topo do canvas
    novoy2 = min(altura, y2 + dy)  # Garante que a base da nave não ultrapasse o fundo
    canvas.coords(nave, x1, novoy1, x2, novoy2)  # Atualiza as coordenadas da nave
    canvas.coords(nave_emoji, x1 + nave_largura // 2, novoy1 + nave_altura // 2)  # Atualiza a posição do emoji



def aparecer_planeta():
    if not running or em_boss:  # Se o jogo não estiver a rodar ou estiver em modo boss, não faz nada
        return
    tamanhop = R.randint(tminplaneta, tmaxplaneta)  # Tamanho aleatório do planeta
    alturap = R.randint(tamanhop, altura - tamanhop)  # Altura aleatória onde o planeta aparece
    cor_planeta = cores_planetas[(level - 1) % len(cores_planetas)]  # Cor do planeta baseado no nível
    forma = formas_planeta[(level - 1) % len(formas_planeta)]  # Forma do planeta baseado no nível
    # Cria o planeta como um texto no canvas
    planet = {
        'id': canvas.create_text(largura + tamanhop, alturap, text=forma,
                                 font=("Arial", tamanhop, "bold"), fill=cor_planeta),
        't': tamanhop,  # Tamanho do planeta
        'velocidade': velocidade_base + level - 1  # Velocidade baseada no nível
    }
    planetas.append(planet)  # Adiciona o planeta à lista global
    canvas.itemconfig(nave_emoji, fill=cor_planeta)  # Muda a cor do emoji da nave para combinar com o planeta
    # Ajusta o aparecimento dos planetas baseado no nivel
    ecranave.after(max(500, 2000 - level * 100), aparecer_planeta)



def subir_nivel():
    global level, em_boss  # Usa variáveis globais
    if em_boss:  # Se está em batalha com o boss, não avança de nível
        return
    level += 1  # Avança para o próximo nível
    atualizar_fundo()  # Atualiza a imagem de fundo
    threading.Thread(target=nome_planeta_fetch).start()  # Procura o nome do novo planeta em uma thread separada
    canvas.itemconfig(level_text, text=f"Nivel {level}: A carregar novo destino...")  # Atualiza o texto no canvas
    if level % 2 == 0 and level <= 6:  # Se o nível for par e até o 6, inicia uma batalha com o boss
        em_boss = True
        threading.Thread(target=iniciar_boss).start()
    else:
        ecranave.after(1000, aparecer_planeta)  # Caso contrário, faz surgir o próximo planeta normalmente



def Verifica_colisao(planet):
    nave_coords = canvas.coords(nave)  # Obtém as coordenadas da nave
    planeta_coords = canvas.coords(planet['id'])  # Obtém as coordenadas do planeta
    if not planeta_coords:  # Se não há coordenadas (objeto removido), não há colisão
        return False
    cx, cy = planeta_coords  # Coordenadas do centro do planeta
    raio = planet.get('t', 30) / 2  # Raio do planeta (usando tamanho, com valor padrão 30)
    x1, y1, x2, y2 = nave_coords  # Coordenadas da nave
    px = max(x1, min(cx, x2))  # Coordenada X mais próxima do planeta dentro da nave
    py = max(y1, min(cy, y2))  # Coordenada Y mais próxima do planeta dentro da nave
    distancia_sq = (cx - px) ** 2 + (cy - py) ** 2  # Distância ao quadrado entre centro do planeta e ponto mais próximo da nave
    return distancia_sq < raio ** 2  # Retorna True se houver colisão (distância menor que raio)



def atualiza_jogo():
    if not running:  # Se o jogo não estiver a correr, sai da função
        return
    if em_boss:  # Se estiver numa fase de boss, atualiza o boss
        atualizar_boss()
    else:
        for planet in list(planetas):  # Itera sobre a lista de planetas
            canvas.move(planet['id'], -planet['velocidade'], 0)  # Move o planeta da direita para a esquerda
            coords = canvas.coords(planet['id'])  # Obtém as novas coordenadas
            if not coords:  # Se não houver coordenadas (pode ter sido apagado), ignora
                continue
            x, y = coords  # Extrai a posição
            if x < -planet['t']:  # Se o planeta saiu completamente do ecrã
                canvas.delete(planet['id'])  # Apaga do canvas
                planetas.remove(planet)  # Remove da lista
            elif Verifica_colisao(planet):  # Se houve colisão com a nave
                capturar_planeta(planet)  # Executa captura
    ecranave.after(30, atualiza_jogo)  # Prepara a próxima atualização do jogo após 30 ms



def capturar_planeta(planet):
    global pontuacao
    if planet in planetas:
        canvas.delete(planet['id'])  # Remove visualmente do canvas
        planetas.remove(planet)  # Remove da lista
        pontuacao += pontos_planeta  # Aumenta a pontuação
        canvas.itemconfig(score_text, text=f"Pontuação: {pontuacao}")  # Atualiza o texto da pontuação

        novo_level = pontuacao // level_up_points + 1  # Calcula se já pode subir de nível
        if novo_level > level:
            subir_nivel()  # Se sim, sobe de nível

boss_timer = 0
boss_tentativas = 0
boss_direcao = -4
boss_ultima_pos = None


def iniciar_boss():
    global boss_atual, musica_pos
    musica_pos = pygame.mixer.music.get_pos()  # Guarda a posição atual da música
    pygame.mixer.music.stop()  # Para a música
    boss_atual = level // 2 - 1  # Define qual é o boss com base no nível
    pygame.mixer.music.load(musicas_boss[boss_atual])  # Carrega a música do boss
    pygame.mixer.music.play(-1)  # Reproduz em loop
    pygame.mixer.music.set_volume(1.0)  # Volume no máximo
    for p in planetas:
        canvas.delete(p['id'])  # Remove todos os planetas do canvas
    planetas.clear()
    boss_elementos.clear()
    canvas.itemconfig(level_text, text=f"Nivel {level}: {nome_planeta} (BOSS)")  # Atualiza o texto do nível
    # Mostra o aviso no centro do ecrã
    canvas.create_text(largura // 2, altura // 2 - 50, text="BOSS FASE", font=("Arial", 24, "bold"), fill="red", tag="boss_text")
    canvas.create_text(largura // 2, altura // 2, text=f"{nomes_bosses[boss_atual]}", font=("Arial", 30, "bold"), fill="white", tag="boss_text")
    ecranave.after(2000, lambda: canvas.delete("boss_text"))  # Remove o texto após 2 segundos
    ecranave.after(2500, mostrar_boss)  # Mostra o boss após 2,5 segundos



def mostrar_boss():
    global boss_elementos, boss_timer, boss_tentativas, boss_direcao, boss_ultima_pos
    boss_elementos.clear()
    if boss_atual == 0:
        y = R.randint(100, 500)  # Posição vertical aleatória
        boss_direcao = -boss_direcao  # Inverte a direção vertical
        boss_id = canvas.create_text(largura, y, text="\u2604", font=("Arial", 100), fill="red", tag="boss")
        boss_elementos.append({'id': boss_id, 'dx': -5, 'dy': boss_direcao, 't': 100})
    elif boss_atual == 1:
        while True:
            y = R.randint(100, 500)
            if y != boss_ultima_pos:  # Evita repetir a posição anterior
                boss_ultima_pos = y
                break
        boss_id = canvas.create_text(largura, y, text="\U0001F6F8", font=("Arial", 60), fill="green", tag="boss")
        boss_elementos.append({'id': boss_id, 'dx': -7, 'dy': 0, 't': 60, 'fade': 0, 'step': 0, 'faded_once': False})
    elif boss_atual == 2:
        x = largura
        alturas = R.sample(range(100, altura - 100, 100), 4)  # Quatro posições verticais diferentes
        real_index = R.randint(0, 3)  # Índice do boss verdadeiro
        for i, ay in enumerate(alturas):
            color = "gray"
            b = canvas.create_text(x, ay, text="\ud83d\udc7e", font=("Arial", 50), fill=color, tag="boss")
            boss_elementos.append({'id': b, 'real': i == real_index, 'dx': -6, 'dy': 0, 't': 50})



def atualizar_boss():
    global em_boss, boss_timer
    boss_timer += 1  # Incrementa o tempo de boss

    if not boss_elementos:
        return

    if boss_atual in (0, 1):  # Boss 0 ou 1
        b = boss_elementos[0]
        if boss_atual == 0:
            canvas.move(b['id'], b['dx'], b['dy'])  # Move o boss
            x, y = canvas.coords(b['id'])
            if y <= 50 or y >= altura - 50:  # Faz o boss bater nas margens
                b['dy'] *= -1
        elif boss_atual == 1:
            b['step'] += 1
            if b['step'] % 30 == 0 and not b['faded_once']:  # Vai alternado a visibilidade
                b['fade'] += 1
                if b['fade'] == 1:
                    canvas.itemconfig(b['id'], state='hidden')
                else:
                    canvas.itemconfig(b['id'], state='normal')
                    b['faded_once'] = True
            canvas.move(b['id'], b['dx'], 0)

        x, y = canvas.coords(b['id'])
        if x < -100:  # Se sair do ecrã, reinicia o boss
            canvas.delete(b['id'])
            boss_elementos.clear()
            mostrar_boss()

        if Verifica_colisao(b):  # Se colidir com a nave
            canvas.delete(b['id'])
            boss_elementos.clear()
            em_boss = False
            retomar_musica_principal_com_fade()
            subir_nivel()

    elif boss_atual == 2:
        todos_fora = True
        for b in boss_elementos:
            canvas.move(b['id'], b['dx'], b['dy'])
            x, _ = canvas.coords(b['id'])
            if x > -100:
                todos_fora = False  # Se algum ainda estiver visível

        if todos_fora:  # Se todos saíram do ecrã
            for b in boss_elementos:
                canvas.delete(b['id'])
            boss_elementos.clear()
            mostrar_boss()
            return

        for b in boss_elementos:
            if Verifica_colisao(b):
                if b.get('real', False):  # Acertou no verdadeiro
                    for bb in boss_elementos:
                        canvas.delete(bb['id'])
                    boss_elementos.clear()
                    em_boss = False
                    iniciar_vitoria()
                else:  # Capturou num falso, repete boss
                    for bb in boss_elementos:
                        canvas.delete(bb['id'])
                    boss_elementos.clear()
                    mostrar_boss()
                break



# Retoma a música principal com um efeito de fade-in a partir da posição onde parou
def retomar_musica_principal_com_fade():
    global musica_pos, fade_in_ativo, fade_volume
    pygame.mixer.music.stop()
    pygame.mixer.music.load(musica_principal_path)
    fade_volume = 0.0
    fade_in_ativo = True
    pygame.mixer.music.set_volume(fade_volume)
    if musica_pos > 0:
        try:
            # Tenta reproduzir a música a partir do momento onde parou
            pygame.mixer.music.play(-1, start=musica_pos / 1000.0)
        except:
            pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.play(-1)
    fade_in_musica()



# Inicia a fase de vitória após derrotar o último boss
def iniciar_vitoria():
    pygame.mixer.music.stop()
    try:
        if os.path.exists(musica_vitoria_path):
            pygame.mixer.music.load(musica_vitoria_path)
            pygame.mixer.music.play(0)
            pygame.mixer.music.set_volume(1.0)
    except:
        pass
    parabens()



# Mostra animação de vitória e nave a sair do ecrã
def parabens():
    global running, fundo_nivel_objeto, fundo_nivel_id
    running = False
    canvas.delete("all")
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    img_path = fundo_img[5]  # Imagem de fundo do Boss 3
    imagem = Image.open(img_path)
    imagem = imagem.resize((canvas_width, canvas_height))
    fundo_nivel_objeto = ImageTk.PhotoImage(imagem)
    fundo_nivel_id = canvas.create_image(0, 0, anchor="nw", image=fundo_nivel_objeto)
    nave_saida = canvas.create_text(50, altura // 2, text="🚀", font=("Arial", 40), fill="white")
    # Anima a nave a mover-se para fora do ecrã
    def animar_saida(x):
        if x < largura + 50:
            canvas.coords(nave_saida, x, altura // 2)
            canvas.after(20, lambda: animar_saida(x + 10))
        else:
            mostrar_tela_final()
    animar_saida(50)



# Mostra o ecrã final de parabéns com opções de menu e sair
def mostrar_tela_final():
    global bg_photo1, bg_item_final
    canvas.delete("all")
    canvas.config(bg="black")
    bg_image1 = Image.open(os.path.join("imagens_proj", "menub.jpg")).resize((800, 600))
    bg_photo1 = ImageTk.PhotoImage(bg_image1)
    bg_item_final = canvas.create_image(0, 0, image=bg_photo1, anchor="nw")
    canvas.create_text(largura // 2, altura // 2 - 100,
                       text="Parabéns, concluíste o jogo!",
                       font=("Arial", 24, "bold"), fill="yellow")
    # Botão para sair do jogo
    botao_sair = tk.Button(canvas, text="Sair do Jogo", font=("Arial", 18, "bold"),
                           bg="red", fg="white", command=sair_do_jogo)
    canvas.create_window(largura // 2, altura // 2 + 40, window=botao_sair)



# Sai do jogo
def sair_do_jogo():
    pygame.mixer.quit()
    ecranave.quit()
    ecranave.destroy()



# Volta ao menu principal após terminar o jogo
def voltar_para_menu_final():
    pygame.mixer.music.stop()
    canvas.destroy()
    menu_frame.pack(fill="both", expand=True)



# Inicia o jogo propriamente dito: reinicia variáveis, carrega música, prepara o canvas
def iniciar_jogo():
    global running, pontuacao, level, em_boss, fade_in_ativo, fade_volume
    pontuacao=0
    level = 1
    em_boss = False
    fade_in_ativo = False
    fade_volume = 1.0
    pygame.mixer.music.load(musica_principal_path)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1.0)
    menu_frame.pack_forget()
    regras_frame.pack_forget()
    criar_canvas_jogo()
    nome_planeta_fetch()
    running = True
    aparecer_planeta()
    atualiza_jogo()



# Mostra o ecrã com as regras do jogo
def mostrar_regras():
    menu_frame.pack_forget()
    regras_frame.pack(fill="both", expand=True)


# Volta ao menu principal a partir do ecrã de regras
def voltar_ao_menu():
    regras_frame.pack_forget()
    menu_frame.pack(fill="both", expand=True)



# Cria o canvas principal do jogo, nave, textos e liga os controlos
def criar_canvas_jogo():
    global canvas, nave, nave_emoji, score_text, level_text
    canvas = tk.Canvas(ecranave, width=largura, height=altura, bg="black", highlightthickness=0, bd=0)
    canvas.pack()
    ecranave.after(100, atualizar_fundo)
    # Desenha a nave
    nave = canvas.create_rectangle(50, altura // 2 - nave_altura // 2,
                                   50 + nave_largura, altura // 2 + nave_altura // 2,
                                   fill="", outline="")
    nave_emoji = canvas.create_text(50 + nave_largura // 2, altura // 2,
                                    text="🚀", font=("Arial", 30))
    # Mostra a pontuação
    score_text = canvas.create_text(10, 10, anchor="nw",
                                    text=f"Pontuação: {pontuacao}", font=("Arial", 16), fill="white")
    # Mostra o nível atual
    level_text = canvas.create_text(10, 40, anchor="nw",
                                    text=f"Nivel {level}: {nome_planeta}", font=("Arial", 16), fill="white",
                                    tag="level_info")
    # Liga as teclas de controlo da nave
    ecranave.bind('<Up>', lambda e: move_nave(-20))
    ecranave.bind('<Down>', lambda e: move_nave(20))



ecranave = tk.Tk()
ecranave.title("Ca\u00e7ador de Planetas")
ecranave.geometry("800x600")

ecranave.protocol("WM_DELETE_WINDOW", sair_do_jogo)

menu_frame = tk.Frame(ecranave)
menu_frame.pack(fill="both", expand=True)

bg_image = Image.open(os.path.join("imagens_proj", "menub.jpg")).resize((800, 600))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(menu_frame, image=bg_photo)
bg_label.image = bg_photo
bg_label.place(relwidth=1, relheight=1)

menu_canvas = tk.Canvas(menu_frame, width=800, height=600, highlightthickness=0)
menu_canvas.pack(fill="both", expand=True)

menu_canvas.create_image(0, 0, image=bg_photo, anchor="nw")

img_foguete = Image.open(os.path.join("imagens_proj", "foguete.png")).resize((200, 200))
img_foguete_tk = ImageTk.PhotoImage(img_foguete)

menu_canvas.create_image(400, 200, image=img_foguete_tk)

menu_canvas.create_text(400, 320, text="Caçador de Planetas",
                        font=("Arial", 30, "bold"), fill="white")

menu_canvas.create_text(400, 360, text="Caça planetas e enfrenta os bosses!",
                        font=("Arial", 16), fill="white")

btn_jogar = tk.Button(menu_frame, text="Jogar", font=("Arial", 20, "bold"),
                      bg="orange", fg="black", command=iniciar_jogo)
menu_canvas.create_window(400, 420, window=btn_jogar, width=200, height=60)

btn_regras = tk.Button(menu_frame, text="Regras", font=("Arial", 20, "bold"),
                       bg="orange", fg="black", command=mostrar_regras)
menu_canvas.create_window(400, 500, window=btn_regras, width=200, height=60)

menu_canvas.bg_photo = bg_photo
menu_canvas.img_foguete_tk = img_foguete_tk

regras_frame = tk.Frame(ecranave, width=800, height=600)
regras_frame.pack_propagate(False)

bg_image1 = Image.open(os.path.join("imagens_proj", "menub.jpg")).resize((800, 600))
bg_photo1 = ImageTk.PhotoImage(bg_image1)

canvas = tk.Canvas(regras_frame, width=800, height=600, highlightthickness=0)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, image=bg_photo1, anchor="nw")

texto_regras = (
    "• Use as setas para cima e para baixo para mover a nave.\n"
    "• Capture planetas para ganhar pontos.\n"
    "• Para o Primeiro nivel precisa de 10 Pontos e para os restantes 20 Pontos.\n"
    "• Ao fim de cada nivel existe um Boss que guarda a entrada para uma nova galaxia.\n"
    "• Boa sorte!!!!"
)

canvas.create_text(
    400, 200,
    text=texto_regras,
    fill="white",
    font=("Arial", 16),
    justify="left",
    width=600
)

canvas.bg_photo1 = bg_photo1

btn_voltar = tk.Button(
    regras_frame,
    text="Voltar ao Menu",
    font=("Arial", 20, "bold"),
    bg="orange",
    fg="black",
    command=voltar_ao_menu
)
btn_voltar.place(relx=0.5, rely=0.7, anchor="center", width=250, height=50)

regras_frame.bg_photo1 = bg_photo1

ecranave.mainloop()