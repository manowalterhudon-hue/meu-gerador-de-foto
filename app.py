import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import io

st.set_page_config(page_title="Gerador de Foto de Perfil - Maria Cristina", layout="centered")

def processar_e_mesclar(foto_usuario, imagem_moldura):
    """
    Torna o fundo branco da parte superior da moldura transparente 
    e coloca a foto do usuário perfeitamente atrás dela, sem cobrir o nome.
    """
    # 1. Converter moldura para RGBA (para aceitar transparência)
    moldura = imagem_moldura.convert("RGBA")
    largura, altura = moldura.size
    
    # 2. Transformar o fundo branco da parte de cima em transparente
    data = np.array(moldura)
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    
    # Identifica pixels brancos ou quase brancos
    pixels_brancos = (r > 240) & (g > 240) & (b > 240)
    
    # Aplicar a transparência APENAS na metade superior da imagem (onde fica a cabeça)
    # Isso garante que o fundo das letras brancas e detalhes de baixo não sumam
    limite_altura = int(altura * 0.58) 
    
    for y in range(limite_altura):
        for x in range(largura):
            if pixels_brancos[y, x]:
                data[y, x, 3] = 0  # Torna o pixel totalmente transparente
                
    moldura_vazada = Image.fromarray(data)
    
    # 3. Preparar a foto do usuário para preencher o fundo de forma harmônica
    foto_rgba = foto_usuario.convert("RGBA")
    
    # Corta e redimensiona a foto do usuário para encaixar no tamanho exato da moldura
    foto_ajustada = ImageOps.fit(foto_rgba, (largura, altura), Image.Resampling.LANCZOS)
    
    # 4. Juntar as duas: Foto no fundo + Moldura oficial por CIMA
    resultado = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    resultado.paste(foto_ajustada, (0, 0))
    
    # A moldura entra por cima, protegendo o nome "MARIA CRISTINA" de ser coberto
    return Image.alpha_composite(resultado, moldura_vazada)

# --- INTERFACE DO SITE ---
st.title("🎨 Gerador de Foto - Maria Cristina 2277")
st.write("Insira sua foto para gerar seu banner de apoio oficial automaticamente!")

try:
    # Abre a imagem que você enviou (certifique-se de salvar a image_vBb4nL.png como moldura.png)
    moldura_base = Image.open("moldura.png")
except FileNotFoundError:
    st.error("Erro: O arquivo 'moldura.png' não foi encontrado no seu GitHub. Verifique o nome do arquivo.")
    st.stop()

# Área de upload para o eleitor/usuário subir a foto dele
arquivo_upload = st.file_uploader("Escolha uma foto sua (JPG, PNG ou JPEG)", type=["jpg", "jpeg", "png"])

if arquivo_upload is not None:
    foto_usuario = Image.open(arquivo_upload)
    
    with st.spinner("Estilizando sua foto com a moldura oficial..."):
        imagem_final = processar_e_mesclar(foto_usuario, moldura_base)
        
    # Exibe o resultado harmônico na tela
    st.image(imagem_final, caption="Sua foto gerada com sucesso!", use_container_width=True)
    
    # Botão de download
    buffer = io.BytesIO()
    imagem_final.save(buffer, format="PNG")
    bytes_resultado = buffer.getvalue()
    
    st.download_button(
        label="📥 Baixar Minha Foto Pronta",
        data=bytes_resultado,
        file_name="apoio_maria_cristina_2277.png",
        mime="image/png"
    )
