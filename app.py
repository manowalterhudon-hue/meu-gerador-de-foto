import streamlit as st
from PIL import Image, ImageOps, ImageDraw
import io

st.set_page_config(page_title="Gerador de Foto com Moldura", layout="centered")

def limpar_miolo_moldura(moldura_original):
    """
    Cria um furo transparente perfeito exatamente onde está o céu azul e a nuvem,
    preservando as bordas coloridas e o número 2277 intactos.
    """
    # Garante que a imagem está no formato correto com canal de transparência (Alpha)
    moldura = moldura_original.convert("RGBA")
    largura, altura = moldura.size
    
    # Coordenadas exatas do círculo do céu calculadas para esta imagem de 1024x1024
    # Centro do círculo (X, Y) e o Raio interno
    centro_x = int(largura * 0.50)   # 512
    centro_y = int(altura * 0.45)    # 460
    raio = int(largura * 0.358)      # ~367 pixels de raio
    
    # Cria uma máscara preta e desenha um círculo branco onde queremos apagar
    mascara_furo = Image.new("L", (largura, altura), 0)
    desenho = ImageDraw.Draw(mascara_furo)
    desenho.ellipse(
        (centro_x - raio, centro_y - raio, centro_x + raio, centro_y + raio), 
        fill=255
    )
    
    # Aplica a transparência no miolo da moldura usando a máscara
    pixels_moldura = moldura.load()
    pixels_mascara = mascara_furo.load()
    
    for y in range(altura):
        for x in range(largura):
            # Se o pixel está dentro do círculo branco da máscara, tornamos ele transparente
            if pixels_mascara[x, y] == 255:
                # Mantém as cores originais, mas define a opacidade (Alpha) para 0 (transparente)
                r, g, b, _ = pixels_moldura[x, y]
                pixels_moldura[x, y] = (r, g, b, 0)
                
    return moldura

def gerar_foto_final(foto_usuario, moldura_limpa):
    """Ajusta a foto do usuário e coloca por trás da moldura já vazada."""
    largura_m, altura_m = moldura_limpa.size
    
    # Redimensiona a foto do usuário para cobrir toda a área da imagem de fundo
    foto_ajustada = ImageOps.fit(foto_usuario.convert("RGBA"), (largura_m, altura_m), Image.Resampling.LANCZOS)
    
    # Coloca a foto do usuário no fundo e joga a moldura vazada por cima
    fundo = Image.new("RGBA", (largura_m, altura_m), (0, 0, 0, 0))
    fundo.paste(foto_ajustada, (0, 0))
    
    # O número 2277 e as bordas vão cobrir as partes necessárias da foto do usuário automaticamente
    return Image.alpha_composite(fundo, moldura_limpa)

# --- INTERFACE ---
st.title("🎨 Gerador de Foto de Perfil - 2277")
st.write("Suba sua foto para aplicar a moldura oficial automaticamente!")

try:
    moldura_base = Image.open("moldura.png")
    # Limpa o céu azul interno deixando-o transparente
    moldura_processada = limpar_miolo_moldura(moldura_base)
except FileNotFoundError:
    st.error("Erro: O arquivo 'moldura.png' não foi encontrado na raiz do projeto.")
    st.stop()

arquivo_upload = st.file_uploader("Escolha uma foto sua (JPG, PNG ou JPEG)", type=["jpg", "jpeg", "png"])

if arquivo_upload is not None:
    foto_usuario = Image.open(arquivo_upload)
    
    with st.spinner("Cortando e encaixando sua foto perfeitamente..."):
        imagem_final = gerar_foto_final(foto_usuario, moldura_processada)
        
    st.image(imagem_final, caption="Sua foto gerada com sucesso!", use_container_width=True)
    
    buffer = io.BytesIO()
    imagem_final.save(buffer, format="PNG")
    bytes_resultado = buffer.getvalue()
    
    st.download_button(
        label="📥 Baixar Foto Pronta",
        data=bytes_resultado,
        file_name="perfil_campanha_2277.png",
        mime="image/png"
    )
