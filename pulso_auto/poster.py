import os
import sys
import json
import time
import requests
from dotenv import load_dotenv
from gerar_marca import gerar_card

load_dotenv()

TOKEN   = os.getenv("INSTAGRAM_TOKEN")
IG_ID   = os.getenv("INSTAGRAM_ID")
IMGUR_CLIENT = os.getenv("IMGUR_CLIENT_ID")

DIR = os.path.dirname(__file__)

def upload_imagem(caminho):
    with open(caminho, "rb") as f:
        r = requests.post(
            "https://api.imgur.com/3/image",
            headers={"Authorization": f"Client-ID {IMGUR_CLIENT}"},
            files={"image": f}
        )
    data = r.json()
    if not data.get("success"):
        raise Exception(f"Erro no upload da imagem: {data}")
    return data["data"]["link"]

def publicar_post(imagem_path, legenda):
    print(f"Fazendo upload: {imagem_path}")
    url_imagem = upload_imagem(imagem_path)
    print(f"URL: {url_imagem}")

    print("Criando container no Instagram...")
    r = requests.post(
        f"https://graph.facebook.com/v19.0/{IG_ID}/media",
        data={"image_url": url_imagem, "caption": legenda, "access_token": TOKEN}
    )
    result = r.json()
    if "id" not in result:
        raise Exception(f"Erro ao criar container: {result}")

    container_id = result["id"]
    print(f"Container: {container_id} — aguardando 5s...")
    time.sleep(5)

    print("Publicando...")
    r = requests.post(
        f"https://graph.facebook.com/v19.0/{IG_ID}/media_publish",
        data={"creation_id": container_id, "access_token": TOKEN}
    )
    result = r.json()
    if "id" not in result:
        raise Exception(f"Erro ao publicar: {result}")

    print(f"✅ Publicado! ID: {result['id']}")
    return result["id"]

def publicar_da_fila():
    fila_path = os.path.join(DIR, "posts.json")
    with open(fila_path) as f:
        posts = json.load(f)

    pendentes = [p for p in posts if not p.get("publicado")]
    if not pendentes:
        print("Nenhum post pendente na fila.")
        return

    post = pendentes[0]
    print(f"\n📋 Post: {post['titulo']}")

    # Gera card automaticamente com a frase do post
    frase = post.get("frase", post["titulo"])
    nome_arquivo = f"card_{posts.index(post)}.png"
    print(f"🎨 Gerando card: \"{frase}\"")
    imagem_path = gerar_card(frase, nome_arquivo)

    legenda = post["legenda"] + "\n\n" + post.get("hashtags", "")
    publicar_post(imagem_path, legenda)

    post["publicado"] = True
    with open(fila_path, "w") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    restantes = len([p for p in posts if not p.get("publicado")])
    print(f"✅ Fila atualizada — {restantes} post(s) restante(s)")

if __name__ == "__main__":
    publicar_da_fila()
