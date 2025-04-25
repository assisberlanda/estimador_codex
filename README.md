# 🧮 Estimador de Custos OpenAI Codex CLI + Interface Web

Este projeto permite estimar o custo de uso da API da OpenAI (Codex/GPT) de forma interativa no terminal ou visualmente via navegador com uma interface local.

---

## ✅ Funcionalidades

### Interface no Terminal (CLI)
- ✅ Estimativas com base nos modelos da OpenAI (`gpt-3.5-turbo`, `gpt-4o`, `gpt-4o-mini`, `gpt-4`)
- ✅ Leitura de arquivos individuais ou pastas inteiras
- ✅ Cálculo de tokens de entrada/saída e custo estimado
- ✅ Reutilização do mesmo prompt e arquivos com múltiplos modelos
- ✅ Exportação automática em `.csv` com resultados completos

### Interface Web
- 🌐 Relatório visual em HTML com:
  - Instrução usada
  - Lista de arquivos analisados
  - Tabela interativa com custos por modelo
- 🚀 Executável localmente com Python puro (`http.server`)
- 📁 Exporta os dados em `relatorio.json` que a página HTML consome

---

## 🚀 Instalação Rápida (CLI global)

1. Baixe os arquivos `estimador_codex_v3.py` e `instalar_estimador.sh`
2. Rode no terminal:

```bash
bash instalar_estimador.sh
```

3. Depois, use de qualquer lugar com:

```bash
estimador
```

---

## 🌐 Como Rodar a Interface Web

1. Baixe os arquivos da interface:
   - `relatorio_codex.html`
   - `relatorio.json` (será gerado pelo script futuramente)
   - `rodar_interface_local.py`

2. Rode o servidor local:

```bash
python3 rodar_interface_local.py
```

3. Acesse no navegador:

```
http://localhost:8000/relatorio_codex.html
```

---

## 📦 Requisitos

- Python 3.7+
- Pacotes: `tiktoken`, `inquirer`, `tabulate` (instalados automaticamente)

---

## 📁 Estrutura de saída esperada

- `estimativa_codex.csv`: relatório simples de terminal
- `relatorio.json`: exportado para visualização web
- `relatorio_codex.html`: interface visual
- `rodar_interface_local.py`: servidor local para HTML

---

Feito com 💻 por Assis Berlanda – compartilhe, adapte e colabore!
# estimar_codex
