import os
import sys
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("INSTAGRAM_TOKEN")
IG_ID = os.getenv("INSTAGRAM_ID")
IMGUR_CLIENT = os.getenv("IMGUR_CLIENT_ID")

def upload_imagem(caminho):
    with open(caminho, "rb") as f:
        r = requests.post(
            "https://api.imgur.com/3/image",
            headers={"Authorization": f"Client-ID {IMGUR_CLIENT}"},
            files={"image": f}
        )
    data = r.json()
    if not data.get("success"):
        raise Exception(f"Erro ao fazer upload da imagem: {data}")
    return data["data"]["link"]

def publicar_post(imagem_path, legenda):
    print(f"Fazendo upload da imagem: {imagem_path}")
    url_imagem = upload_imagem(imagem_path)
    print(f"Imagem disponível em: {url_imagem}")

    print("Criando container no Instagram...")
    r = requests.post(
        f"https://graph.facebook.com/v19.0/{IG_ID}/media",
        data={
            "image_url": url_imagem,
            "caption": legenda,
            "access_token": TOKEN
        }
    )
    result = r.json()
    if "id" not in result:
        raise Exception(f"Erro ao criar container: {result}")

    container_id = result["id"]
    print(f"Container criado: {container_id}")
    time.sleep(5)

    print("Publicando post...")
    r = requests.post(
        f"https://graph.facebook.com/v19.0/{IG_ID}/media_publish",
        data={
            "creation_id": container_id,
            "access_token": TOKEN
        }
    )
    result = r.json()
    if "id" not in result:
        raise Exception(f"Erro ao publicar: {result}")

    print(f"✅ Post publicado com sucesso! ID: {result['id']}")
    return result["id"]

def publicar_da_fila():
    fila_path = os.path.join(os.path.dirname(__file__), "posts.json")
    with open(fila_path) as f:
        posts = json.load(f)

    pendentes = [p for p in posts if not p.get("publicado")]
    if not pendentes:
        print("Nenhum post pendente na fila.")
        return

    post = pendentes[0]
    print(f"\nPublicando: {post['titulo']}")

    imagem = os.path.join(os.path.dirname(__file__), "imagens", post["imagem"])
    if not os.path.exists(imagem):
        print(f"❌ Imagem não encontrada: {imagem}")
        print("Coloque a imagem na pasta imagens/ e tente novamente.")
        return

    legenda = post["legenda"] + "\n\n" + post.get("hashtags", "")
    publicar_post(imagem, legenda)

    post["publicado"] = True
    with open(fila_path, "w") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f"Fila atualizada — próximo post: {pendentes[1]['titulo'] if len(pendentes) > 1 else 'nenhum'}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        publicar_post(sys.argv[1], sys.argv[2])
    else:
        publicar_da_fila()
