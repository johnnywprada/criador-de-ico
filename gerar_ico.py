from PIL import Image

def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    """
    Centraliza a imagem em um canvas quadrado transparente.
    Isso impede distorção se a imagem original for retangular.
    """
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    # Cola a imagem original no centro
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

def create_professional_ico(input_path, output_path):
    try:
        img = Image.open(input_path)
        
        # Garante que estamos trabalhando com RGBA (transparência)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # Passo 1: Tornar a imagem quadrada para não distorcer
        img = make_square(img)

        # Passo 2: Definir tamanhos padrão do Windows
        # A ordem importa: do maior para o menor.
        # 256px é para views "Extra Large", 16px é para "Details/List view"
        icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        
        batch_images = []

        # Passo 3: Reamostragem de alta qualidade
        for size in icon_sizes:
            # LANCZOS é crítico aqui. O padrão (NEAREST) cria serrilhados horríveis.
            resized_img = img.resize(size, resample=Image.Resampling.LANCZOS)
            batch_images.append(resized_img)

        # Passo 4: Salvar
        # O formato ICO permite embutir várias imagens no mesmo arquivo.
        # 'append_images' adiciona as outras resoluções além da primeira.
        batch_images[0].save(
            output_path, 
            format='ICO', 
            sizes=icon_sizes, 
            append_images=batch_images[1:]
        )

        print(f"Sucesso: {output_path} gerado com {len(icon_sizes)} camadas de resolução.")

    except Exception as e:
        print(f"Erro ao processar: {e}")

# --- Execução ---
# Substitua pelo nome do seu arquivo gerado
input_file = "icone_em_HD.png" 
output_file = "warp.ico"

create_professional_ico(input_file, output_file)