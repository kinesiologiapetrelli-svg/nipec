#!/usr/bin/env bash
# Rigenera i PDF dei documenti NIPEC a partire dalle fonti in Markdown/HTML.
#
#   bash tools/build-pdf.sh
#
# Fonte unica: CLAUDE.md per il principio, docs/*.md per il resto.
# I PDF in docs/ sono prodotti — non si modificano a mano, si rigenerano.

set -euo pipefail
cd "$(dirname "$0")/.."

CHROME=$(command -v chromium || command -v chromium-browser || command -v google-chrome \
  || echo /opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell)

render() { # $1 = html di partenza, $2 = pdf di arrivo
  "$CHROME" --no-sandbox --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$PWD/$2" "file://$PWD/$1" 2>/dev/null
  echo "  $2"
}

echo "Principio di Analisi Petrus"
render docs/build/principio.html docs/petrus/PrincipioAnalisiPetrus.pdf

echo "Biblioteca cognitiva"
python3 tools/md2html.py docs/petrus/BibliotecaCognitiva.md \
  docs/build/biblioteca.html "Biblioteca cognitiva NIPEC" >/dev/null
render docs/build/biblioteca.html docs/petrus/BibliotecaCognitiva.pdf

echo "Biblioteca completa (indice + regole + cinque lenti)"
{
  cat docs/petrus/BibliotecaCognitiva.md
  for f in docs/petrus/lenti/RegoleDiRagionamento.md docs/petrus/lenti/MappaConcetti.md \
           docs/petrus/lenti/SchedaOperativa.md \
           docs/petrus/lenti/Munger.md \
           docs/petrus/lenti/Buffett.md docs/petrus/lenti/Kiyosaki.md \
           docs/petrus/lenti/Fuller.md docs/petrus/lenti/Gardner.md; do
    printf '\n\n---\n\n'
    cat "$f"
  done
} > docs/build/biblioteca-completa.md
python3 tools/md2html.py docs/build/biblioteca-completa.md \
  docs/build/biblioteca-completa.html "Biblioteca cognitiva NIPEC — completa" >/dev/null
render docs/build/biblioteca-completa.html docs/petrus/BibliotecaCognitiva-completa.pdf

echo "Contratti"
for c in Contratto-1-Vendita-Afrodite Contratto-2-Noleggio-Afrodite; do
  python3 tools/md2html.py "docs/nipec/contratti/$c.md" \
    "docs/build/$c.html" "$c" >/dev/null
  render "docs/build/$c.html" "docs/nipec/contratti/$c.pdf"
done

echo "Fatto."
