
#!/Library/Frameworks/Python.framework/Versions/3.13/bin/python3
import os
import sys
import csv
import json
import time
import tiktoken
import webbrowser
import shutil
import threading
import http.server
import socketserver
import urllib.request
from datetime import datetime

try:
    import inquirer
    from tabulate import tabulate
except ImportError:
    print("📦 Instalando dependências...")
    os.system("pip install inquirer tabulate")
    import inquirer
    from tabulate import tabulate

PREÇOS = {
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    "gpt-4o-mini": {"input": 0.0025, "output": 0.0075},
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-4": {"input": 0.01, "output": 0.03},
}

EXTENSOES_VALIDAS = [".py", ".js", ".ts", ".html", ".css", ".json", ".java", ".txt"]

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def mostrar_boas_vindas():
    clear_terminal()
    borda = "=" * 60
    print(f"\n{borda}")
    print("🚀 BEM-VINDO AO ESTIMADOR CODEX CLI".center(60))
    print(borda)
    print("💡 Estima o custo de uso da API da OpenAI com base nos tokens")
    print("📁 Analisa arquivos ou pastas inteiras com extensões de código")
    print("🌐 Gera relatório em CSV + interface web visual (HTML/JSON)")
    print(f"{borda}\n")

def contar_tokens(texto: str, modelo: str = "gpt-3.5-turbo"):
    try:
        encoding = tiktoken.encoding_for_model(modelo)
    except:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(texto))

def estimar_custo(modelo, input_tokens, output_tokens):
    preco = PREÇOS.get(modelo)
    if not preco:
        raise ValueError(f"Modelo '{modelo}' não suportado.")
    custo = (input_tokens / 1000) * preco["input"] + (output_tokens / 1000) * preco["output"]
    return round(custo, 4)

def ler_arquivos_recursivamente(caminho):
    conteudo_total = ""
    arquivos_lidos = []
    if os.path.isfile(caminho):
        if os.path.splitext(caminho)[1] in EXTENSOES_VALIDAS:
            with open(caminho, "r", encoding="utf-8") as f:
                conteudo_total += f"\n# Arquivo: {caminho}\n" + f.read()
                arquivos_lidos.append(caminho)
    else:
        for root, _, files in os.walk(caminho):
            for file in files:
                if os.path.splitext(file)[1] in EXTENSOES_VALIDAS:
                    caminho_arquivo = os.path.join(root, file)
                    with open(caminho_arquivo, "r", encoding="utf-8", errors="ignore") as f:
                        conteudo_total += f"\n# Arquivo: {caminho_arquivo}\n" + f.read()
                        arquivos_lidos.append(caminho_arquivo)
    return conteudo_total, arquivos_lidos

def salvar_csv(prompt, arquivos, resultados, pasta_destino):
    nome_arquivo = os.path.join(pasta_destino, "estimativa_codex.csv")
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Prompt", prompt])
        writer.writerow([])
        writer.writerow(["Arquivos analisados:"])
        for arquivo in arquivos:
            writer.writerow([arquivo])
        writer.writerow([])
        writer.writerow(["Modelo", "Tokens Entrada", "Tokens Saída (estimado)", "Custo (USD)"])
        for r in resultados:
            writer.writerow([r["modelo"], r["tokens_entrada"], r["tokens_saida"], r["custo"]])
    print(f"📄 Estimativa salva em: {nome_arquivo}")

def salvar_json(prompt, arquivos, resultados, pasta_destino):
    dados = {
        "prompt": prompt,
        "arquivos": arquivos,
        "resultados": resultados
    }
    nome_arquivo = os.path.join(pasta_destino, "relatorio.json")
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    print(f"🌐 Relatório web salvo como: {nome_arquivo}")

def copiar_relatorio_html(destino):
    destino_html = os.path.join(destino, "relatorio_codex.html")
    if not os.path.exists(destino_html):
        conteudo_html = """<!DOCTYPE html><html><head><meta charset='utf-8'><title>Relatório</title></head><body><h1>Relatório Codex</h1><div id='relatorio'></div><script>fetch('relatorio.json').then(r=>r.json()).then(d=>{document.getElementById('relatorio').innerText=JSON.stringify(d,null,2);})</script></body></html>"""
        with open(destino_html, "w", encoding="utf-8") as f:
            f.write(conteudo_html)
        print("📁 Arquivo relatorio_codex.html criado na pasta atual.")

def iniciar_servidor_local(pasta_destino):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            return

    def servidor():
        os.chdir(pasta_destino)
        with socketserver.TCPServer(("", 8000), Handler) as httpd:
            httpd.serve_forever()

    thread = threading.Thread(target=servidor, daemon=True)
    thread.start()

    for _ in range(10):
        try:
            with urllib.request.urlopen("http://localhost:8000", timeout=1):
                print("🌐 Servidor local iniciado em http://localhost:8000")
                return
        except:
            time.sleep(0.5)
    print("⚠️ Não foi possível iniciar o servidor local.")

def main():
    mostrar_boas_vindas()
    try:
        print("1️⃣ O que você deseja que o Codex faça com seu código?")
        prompt_usuario = input("> ").strip()
        if not prompt_usuario:
            print("⚠️ Nenhuma instrução fornecida. Encerrando.")
            return

        caminho = inquirer.text("2️⃣ Caminho do arquivo ou pasta (pressione Enter para usar a pasta atual):")
        if not caminho.strip():
            caminho = os.getcwd()
            print(f"📂 Nenhum caminho informado. Usando a pasta atual: {caminho}")

        print("\n📦 Lendo arquivos...")
        codigo, arquivos_lidos = ler_arquivos_recursivamente(caminho)
        if not codigo.strip():
            print("❌ Nenhum arquivo válido encontrado.")
            return

        entrada_completa = f"Instruções: {prompt_usuario}\n\n{codigo}"
        input_tokens = contar_tokens(entrada_completa)

        resultados = []
        for modelo in PREÇOS:
            output_tokens_estimado = 800
            custo = estimar_custo(modelo, input_tokens, output_tokens_estimado)
            resultado = {
                "modelo": modelo,
                "tokens_entrada": input_tokens,
                "tokens_saida": output_tokens_estimado,
                "custo": round(custo, 4)
            }
            resultados.append(resultado)
            print("\n📊 Estimativa:")
            print(tabulate([[resultado["modelo"], resultado["tokens_entrada"], resultado["tokens_saida"], f"${resultado['custo']:.4f}"]],
                           headers=["Modelo", "Tokens Entrada", "Tokens Saída", "Custo (USD)"], tablefmt="grid"))

        if resultados:
            salvar_csv(prompt_usuario, arquivos_lidos, resultados, os.getcwd())
            salvar_json(prompt_usuario, arquivos_lidos, resultados, os.getcwd())
            copiar_relatorio_html(os.getcwd())
            abrir = inquirer.confirm("🌍 Deseja abrir o relatório visual no navegador?", default=True)
            if abrir:
                iniciar_servidor_local(os.getcwd())
                if os.path.exists("relatorio.json"):
                    webbrowser.open("http://localhost:8000/relatorio_codex.html")
                    input("🔁 Pressione Enter para encerrar...")
                else:
                    print("⚠️ relatorio.json não encontrado. A página pode abrir vazia.")

        print("👋 Análise encerrada. Obrigado por usar o Estimador Codex!")

    except KeyboardInterrupt:
        print("\n🛑 Interrompido pelo usuário. Até a próxima!")

if __name__ == "__main__":
    main()