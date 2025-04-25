#!/bin/bash

echo "🔧 Instalando o Estimador Codex CLI..."

DESTINO=$HOME/.local/bin
SCRIPT_ORIGEM="estimador_codex_v3.py"
SCRIPT_DESTINO="$DESTINO/estimador"

# 1. Cria ~/.local/bin se não existir
mkdir -p "$DESTINO"

# 2. Copia o script para ~/.local/bin com nome de comando
cp "$SCRIPT_ORIGEM" "$SCRIPT_DESTINO"
chmod +x "$SCRIPT_DESTINO"

# 3. Garante que ~/.local/bin esteja no PATH no .zshrc
if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$HOME/.zshrc"; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
  echo "✅ PATH atualizado no ~/.zshrc"
fi

# 4. Instala dependências usando o mesmo Python usado pelo script
PYTHON_BIN=$(which python3)
echo "🐍 Instalando dependências no Python: $PYTHON_BIN"
$PYTHON_BIN -m pip install --user tiktoken inquirer tabulate

# 5. Recarrega PATH atual
export PATH="$HOME/.local/bin:$PATH"

echo "✅ Instalação concluída!"
echo "Você pode usar agora com o comando: estimador"
