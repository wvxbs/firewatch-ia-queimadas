# FireWatch IA — experimento retrospectivo

Projeto de Gabriel Ferreira (RA 10442043), turma 07N, Inteligência Artificial, Universidade Presbiteriana Mackenzie.

Este repositório documenta um experimento de priorização semanal de municípios a partir de detecções de focos ativos do [Programa Queimadas do INPE](https://www.terrabrasilis.dpi.inpe.br/queimadas/portal/pages/secao_downloads/dados-abertos/index.html). O recorte disponível cobre janeiro e fevereiro de 2025. Trata-se de **avaliação retrospectiva**, sem uso operacional.

## Arquivos

- `experimento.py`: preparação do painel, treinamento e avaliação temporal.
- CSV na raiz: arquivos mensais originais de [janeiro](https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/mensal/Brasil/focos_mensal_br_202501.csv) e [fevereiro](https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/mensal/Brasil/focos_mensal_br_202502.csv) de 2025.
- `analise_exploratoria.py`, `artigo_parcial_firewatch_07N.pdf`, `municipio_semana_observado.csv` e `resumo_eda.json`: entrega da Parte 2.
- `resultados/metricas.csv`: AP, precisão, revocação, F1 e revocação entre os 50 primeiros por semana e modelo.
- `resultados/ranking_retrospectivo.csv`: demonstração histórica para a semana de 17/02/2025.
- `resultados/resumo.json`: protocolo e resultados em formato estruturado.
- `artigo_parte3_aguardando_video.pdf`: artigo da Parte 3; substituir pelo PDF com o link do vídeo antes da entrega final.

## Reproduzir

Requer Python 3.10+.

```sh
python3 -m pip install -r requirements.txt
python3 experimento.py
```

O script recria os arquivos em `resultados/`. Ele usa somente `AQUA_M-T` para contar focos; o painel inclui 4.332 municípios encontrados em qualquer satélite nos dois CSV. A classe positiva provisória é o decil superior entre municípios com pelo menos uma detecção na semana alvo, incluindo empates.

## Resultado e limites

Em três semanas de teste temporal, a AP média foi 0,0654 para persistência, 0,0798 para regressão logística e 0,0755 para floresta aleatória. O recorte curto, o universo municipal incompleto e o desempenho baixo impedem conclusões sobre utilidade real. A proposta inicial de 2019–2025, XGBoost, SHAP e protótipo não foi concluída neste experimento.

Dados de focos não equivalem a área queimada, gravidade ou causa de incêndios. Qualquer aplicação prática exigiria histórico maior, análise regional e revisão humana.
