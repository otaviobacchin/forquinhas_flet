import flet as ft
import random
import unicodedata

# Lista de palavras para o jogo
palavras = [
    "bananinha", "hype", "brahminha", "lapide", "loucas", "islandia", "wynwood",
    "porks", "edição comemorativa", "comemorativa", "trave", "larva", "brodway",
    "lindsay", "yaglandula", "da lhe", "dar lhe", "faz o l", "botina", "epoca errada",
    "quem estuda é burro", "burro", "trouxa", "rico", "galão", "agua", "pão",
    "mercadinho", "perfumes", "personagem", "eu odeio eu", "vou nanar", "minha toro",
    "toro", "estagiario", "sustentar o muniz na faculdade", "fortal", "financeia",
    "usa portugues quem precisa", "ilha", "farol", "dormiu de botina", "MM", "Ocean Blue",
    "Hamburgueria do X", "X Vinhos", "Oliver", "eu odeio eu", "o pai é bonito", "brahma litrão",
    "paisagismo", "visagismo", "roleta", "lhe da", "bleu de channel"
]

xingamentos = [
    "um corno", "um jumento", "fudido", "otário", "uma aberração", "um gordo morfético", 
    "uma baleia azul", "um fedido que não sabe nada de perfume", "um eau de channel", "uma bananinha bem passada",
    "amante do netão beef", "uma brahma litrão quente", "casado", "a nutricionista do yagao",
    "fretista do tio do ricieri", "babaca", "estudado", "graduado", "um dublê de rico", "um careca", "um calvo",
    "um pega ninguém", "horroroso"
]

audios_win = ['caramaisarrombado.mp3', 'comoconsegueviajar.mp3', 'cuidadavida.mp3', 'gabrielvaixavecar.mp3',
            'grupodemerdadocaraio.mp3', 'grupodepersonagens.mp3', 'inimigodaverdade.mp3', 'invejadocebola.mp3',
            'naotemumpapo.mp3', 'naotoacreditandodeuspai.mp3', 'nossakike.mp3', 'paradefalarmeunome.mp3',
            'pediupromunizvoltar.mp3', 'pqyagotenis.mp3', 'quedecadencia.mp3', 'sabadao10hdamanha.mp3',
            'socompronopda.mp3', 'teniscaro.mp3', 'tonolimite.mp3', 'xparedeacordarcedo.mp3']

audios_lose = ['euodeioeu.mp3', 'jumentostrouxas.mp3', 'loucasfalandodogab.mp3', 'tateno.mp3', 'xeumerro.mp3']




# Função para normalizar letras (remover acentos) e converter para maiúsculas
def normalizar_letra(letra):
    return unicodedata.normalize('NFD', letra).encode('ascii', 'ignore').decode('utf-8').upper()

# Função para iniciar o jogo
def iniciar_jogo():
    global palavra_secreta, letras_erradas, letras_corretas, tentativas_restantes
    palavra_secreta = random.choice(palavras).upper()
    letras_erradas = set()
    letras_corretas = set()
    tentativas_restantes = 6

# Função para atualizar o estado do jogo
def atualizar_estado():
    letras_ocultas = [
        letra if normalizar_letra(letra) in letras_corretas or letra == ' ' else '_'
        for letra in palavra_secreta
    ]
    estado_palavra = " ".join(letras_ocultas)
    return estado_palavra

def main(page: ft.Page):
    global audio_vitoria, audio_derrota, audio_mutado

    audio_mutado = False

    page.title = "Forquinhas"
    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    iniciar_jogo()
    
    imagem_titulo = ft.Image(src="./imagens/loucasbg2.png", width=200, height=200, fit="contain")
    titulo = ft.Text(value="F O R Q U I N H A S", style="headlineLarge", text_align=ft.TextAlign.CENTER, size=50)
    espaco_titulo = ft.Container(height=30)
    palavra_label = ft.Text(value=atualizar_estado(), width=800, text_align=ft.TextAlign.CENTER, style='titleLarge')
    espaco_palavra_letra = ft.Container(height=30)  # Espaço entre a palavra e a caixa de texto
    letra_input = ft.TextField(label="Letra", width=100, on_submit=lambda e: verificar_tentativa(None))
    mensagem = ft.Text()
    chances_label = ft.Text(value=f"Tentativas restantes: {tentativas_restantes}")
    letras_erradas_label = ft.Text(value=f"Letras erradas: {', '.join(letras_erradas)}")
    btn_jogar_novamente = ft.ElevatedButton(text="Jogar Novamente", on_click=lambda e: reiniciar_jogo(), visible=False)
    
    audio_inicio = ft.Audio(src="./audios/paiebonitoempqp.mp3", autoplay=True)
    audio_vitoria = ft.Audio(src=f"./audios/win/{random.choice(audios_win)}", autoplay=False)
    audio_derrota = ft.Audio(src=f"./audios/lose/{random.choice(audios_lose)}", autoplay=False)

    def tocar_audio_inicio():
        if not audio_mutado:
            audio_inicio.play()
    
    def tocar_audio_vitoria():
        if not audio_mutado:
            audio_vitoria.play()
    
    def tocar_audio_derrota():
        if not audio_mutado:
            audio_derrota.play()

    def alternar_mute():
        global audio_mutado
        audio_mutado = not audio_mutado
        audio_inicio.muted = audio_mutado
        audio_vitoria.muted = audio_mutado
        audio_derrota.muted = audio_mutado
        mute_btn.icon = "volume_up" if not audio_mutado else "volume_off"
        page.update()

    def verificar_tentativa(e):
        letra = letra_input.value.upper()
        if letra and letra.isalpha() and len(letra) == 1:
            if letra in letras_erradas or letra in letras_corretas:
                mensagem.value = "Você já chutou essa letra, T R O U X A!"
            else:
                resultado = tentativa(letra)
                palavra_label.value = atualizar_estado()
                letra_input.value = ""
                chances_label.value = f"Tentativas restantes: {tentativas_restantes}"
                letras_erradas_label.value = f"Letras erradas: {', '.join(letras_erradas)}"
                if resultado:
                    mensagem.value = resultado
                if "impressionado" in resultado or "BURRO" in resultado:
                    letra_input.disabled = True
                    btn_jogar_novamente.visible = True
            letra_input.focus()
        else:
            mensagem.value = "É só pra usar LETRA, seu B U R R O! kkkkkk"
        page.update()

    def reiniciar_jogo():
        global audio_vitoria, audio_derrota
        iniciar_jogo()
        palavra_label.value = atualizar_estado()
        letra_input.disabled = False
        letra_input.value = ""
        mensagem.value = ""
        chances_label.value = f"Tentativas restantes: {tentativas_restantes}"
        letras_erradas_label.value = f"Letras erradas: {', '.join(letras_erradas)}"
        btn_jogar_novamente.visible = False
        
        # Atualiza os áudios aleatórios para a nova sessão
        page.controls.remove(audio_vitoria)
        page.controls.remove(audio_derrota)
        
        audio_vitoria = ft.Audio(src=f"./audios/win/{random.choice(audios_win)}", autoplay=False)
        audio_derrota = ft.Audio(src=f"./audios/lose/{random.choice(audios_lose)}", autoplay=False)
        
        page.add(audio_vitoria)
        page.add(audio_derrota)
        
        page.update()
    
    def tentativa(letra):
        global tentativas_restantes
        letra_normalizada = normalizar_letra(letra)
        mensagem_erro = ""

        if letra_normalizada in letras_corretas or letra in letras_erradas:
            return "Você já chutou essa letra, T R O U X A!"
        if letra_normalizada in normalizar_letra(palavra_secreta):
            letras_corretas.add(letra_normalizada)
        else:
            letras_erradas.add(letra)
            tentativas_restantes -= 1
            mensagem_erro = f"Errou! Você é {random.choice(xingamentos)} mesmo."
        
        letras_palavra_secreta = set(normalizar_letra(letra) for letra in palavra_secreta if letra != ' ')
        if letras_palavra_secreta <= letras_corretas:
            tocar_audio_vitoria()
            return f"Nossa, parabens em, to impressionado com a sua inteligencia... Q inveja que eu to de vc.\na palavra era: {palavra_secreta}"
        elif tentativas_restantes <= 0:
            tocar_audio_derrota()
            return f'Vc deve ter estudado muito mesmo porque vc é BURRO KKKKKKKKKKK\n\nA palavra certa era "{palavra_secreta}", nem pelo hype vc consegue se manter, aiaiai...'
        else:
            return mensagem_erro

    # Adiciona o botão de ícone
    mute_btn = ft.IconButton(icon="volume_up", on_click=lambda e: alternar_mute())

    page.add(
        imagem_titulo,
        titulo,
        espaco_titulo,
        palavra_label,
        espaco_palavra_letra,  # Adiciona o espaço entre a palavra e a caixa de texto
        ft.Column(
            controls=[
                letra_input,
                ft.ElevatedButton(text="Chutar", on_click=verificar_tentativa),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        mensagem,
        chances_label,
        letras_erradas_label,
        btn_jogar_novamente,
        mute_btn,
        audio_inicio,
        audio_vitoria,
        audio_derrota
    )
    
    tocar_audio_inicio()

# Executa a aplicação
ft.app(target=main)