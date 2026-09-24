# Ola Vet: Resumos Visuais de Veterinária

Ebook A4 de **100 páginas**: capa, **98 fichas visuais** e referências. Conteúdo em português, voltado ao estudo e à revisão rápida de pequenos animais (cães e gatos).

## Baixar

[PDF final (100 páginas)](output/pdf/atlas_visual_veterinaria_100_paginas.pdf)

## Módulos

| Páginas | Módulo |
| --- | --- |
| 2–10 | Fundamentos |
| 11–20 | Semiologia |
| 21–32 | Hematologia |
| 33–42 | Bioquímica e urina |
| 43–52 | Microbiologia |
| 53–62 | Parasitologia |
| 63–71 | Farmacologia aplicada |
| 72–81 | Sistemas clínicos |
| 82–91 | Urgências |
| 92–99 | Prevenção e saúde única |

O PDF traz marcadores de navegação por módulo, fonte de cada ficha no rodapé e links na página 100. O arquivo `content/topics.txt` contém o texto editável; `build.py` gera o PDF com ilustrações vetoriais originais.

## Regerar

Requer Python 3 e `reportlab` (fonte DejaVu Sans instalada no sistema).

```bash
python3 -m pip install reportlab
python3 build.py
```

## Uso responsável

O material é educativo. Não traz doses nem protocolos de prescrição. Interprete exames e intervenções segundo espécie, história, estado clínico, diretrizes atuais, legislação e avaliação do médico veterinário. Fontes principais: Manual Veterinário Merck, WSAVA, AAHA, ISCAID, CAPC e IRIS; links detalhados em [FONTES.md](FONTES.md).
