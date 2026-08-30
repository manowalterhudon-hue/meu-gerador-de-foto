import streamlit as st
from PIL import Image, ImageOps, ImageDraw
import io

st.set_page_config(page_title="Gerador de Foto - Maria Cristina", layout="centered")

def gerar_foto_circulo_interno(foto_usuario, imagem_moldura):
    """
    Recorta a foto do usuário em formato circular e a encaixa milimetricamente
    dentro do círculo verde da moldura oficial.
    """
    # 1. Carregar a moldura original em alta qualidade
    moldura = imagem_moldura.convert("RGBA")
    largura_m, altura_m = moldura.size
    
    # 2. Definir o tamanho e a posição exata do círculo verde na imagem (Base 1024x1024)
    # Ajustado de forma milimétrica para cobrir o céu azul e a nuvem interna
    largura_alvo = int(largura_m * 0.72)  # ~737 pixels de diâmetro
    altura_alvo = int(altura_m * 0.72)
    
    # Posição centralizada para encaixar dentro da borda verde
    pos_x = int(largura_m * 0.14)         # Deslocamento horizontal (143 pixels)
    pos_y = int(altura_m * 0.11)         # Deslocamento vertical (112 pixels)

    # 3. Redimensionar e cortar a foto do usuário para o tamanho do quadrado do círculo
    foto_ajustada = ImageOps.fit(foto_usuario.convert("RGBA"), (largura_alvo, altura_alvo), Image.Resampling.LANCZOS)
    
    # 4. Criar uma máscara circular perfeita
    mascara_circulo = Image.new("L", (largura_alvo, altura_alvo), 0)
    desenho = ImageDraw.Draw(mascara_circulo)
    desenho.ellipse((0, 0, largura_alvo, altura_alvo), fill=255)
    
    # 5. Criar uma tela de fundo transparente idêntica ao tamanho da moldura
    fundo_final = Image.new("RGBA", (largura_m, altura_m), (0, 0, 0, 0))
    
    # 6. Colar a foto circular do usuário na posição exata do miolo verde
    fundo_final.paste(foto_ajustada, (pos_x, pos_y), mascara_circulo)
    
    # 7. Sobrepor a moldura oficial com os textos por CIMA de tudo
    # Como as letras e faixas estão na frente, o acabamento fica perfeito
    return Image.alpha_composite(fundo_final, moldura)

# --- INTERFACE DO SITE ---
st.title("🎨 Gerador de Foto Oficial - Maria Cristina 2277")
st.write("Suba sua foto e veja a mágica acontecer dentro do círculo oficial de campanha!")

try:
    # Abre a imagem atualizada que você acabou de me enviar
    # Certifique-se de salvar esta nova imagem como 'moldura.png' no GitHub
    moldura_base = Image.open("moldura.png")
except FileNotFoundError:
    st.error("Erro: O arquivo 'moldura.png' não foi encontrado no seu GitHub. Verifique o nome do arquivo.")
    st.stop()

# Área para o usuário subir a foto dele
arquivo_upload = st.file_uploader("Escolha uma foto sua (JPG, PNG ou JPEG)", type=["jpg", "jpeg", "png"])

if arquivo_upload is not None:
    foto_usuario = Image.open(arquivo_upload)
    
    with st.spinner("Moldando sua foto dentro do círculo oficial..."):
        imagem_final = gerar_foto_circulo_interno(foto_usuario, moldura_base)
        
    # Exibe o resultado impecável na tela do site
    st.image(imagem_final, caption="Sua foto de perfil oficial está pronta!", use_container_width=True)
    
    # Botão de download seguro
    buffer = io.BytesIO()
    imagem_final.save(buffer, format="PNG")
    bytes_resultado = buffer.getvalue()
    
    st.download_button(
        label="📥 Baixar Minha Foto de Apoio",
        data=bytes_resultado,
        file_name="perfil_maria_cristina_2277.png",
        mime="image/png"
    )
