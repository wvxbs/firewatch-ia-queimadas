# FireWatch IA — experimento retrospectivo

Projeto de Gabriel Ferreira (RA 10442043), turma 07N, Inteligência Artificial, Universidade Presbiteriana Mackenzie.

Este repositório estuda a priorização semanal de municípios com dados públicos de focos ativos do [Programa Queimadas do INPE](https://www.terrabrasilis.dpi.inpe.br/queimadas/portal/pages/secao_downloads/dados-abertos/index.html). O recorte cobre **janeiro e fevereiro de 2024 e 2025**. É uma avaliação retrospectiva, sem uso operacional.

## Arquivos

- `experimento.py`: constrói o painel, treina os modelos e avalia o teste temporal.
- `focos_mensal_br_202401.csv`, `202402.csv`, `202501.csv`, `202502.csv`: CSV mensais originais do INPE, na raiz do repositório.
- `resultados/metricas.csv`: AP, precisão, revocação, F1 e revocação entre os 50 primeiros por semana e método.
- `resultados/ranking_retrospectivo.csv`: ranking histórico para a semana de 17/02/2025; não é previsão atual.
- `resultados/resumo.json`: protocolo e resultados estruturados.
- `artigo_parte3_aguardando_video.pdf`: artigo da Parte 3. O endereço do vídeo será inserido depois da gravação.
- `analise_exploratoria.py`, `artigo_parcial_firewatch_07N.pdf`, `municipio_semana_observado.csv` e `resumo_eda.json`: entrega anterior, Parte 2.

## Reproduzir

Requer Python 3.10+.

    python3 -m pip install -r requirements.txt
    python3 experimento.py

O script recria `resultados/`. As contagens semanais usam somente o satélite **AQUA_M-T**. O painel contém 4.872 códigos municipais observados por qualquer satélite nos quatro CSV, incluindo zeros para semanas sem detecção AQUA_M-T. Isso não corresponde a um cadastro nacional completo. A classe positiva provisória é o decil superior entre municípios com pelo menos uma detecção na semana alvo, incluindo empates.

## Protocolo e resultados

Treino: seis semanas alvo de **2024**. Teste: cinco semanas alvo de **2025**, sem dados de 2025 no ajuste. Entradas: contagens da semana corrente e da anterior. Métodos: persistência, regressão logística e floresta aleatória. Os hiperparâmetros foram fixados antes da comparação, sem busca ou calibração.

| Método | AP média | F1 médio no corte 0,5 | Revocação média nos 50 primeiros |
|---|---:|---:|---:|
| Persistência | 0,1093 | 0,1129 | 0,2176 |
| Regressão logística | 0,1244 | 0,1630 | 0,2237 |
| Floresta aleatória | **0,1272** | 0,1132 | 0,2237 |

A AP da floresta superou a persistência nas cinco semanas de teste, mas o desempenho absoluto é baixo e varia muito por semana. Os dois meses de cada ano, o universo municipal incompleto e a seleção retrospectiva de códigos impedem conclusões de utilidade real. A proposta original de 2019–2025, XGBoost, SHAP e protótipo não foi concluída aqui.

Focos de satélite não medem área queimada, gravidade nem causa de incêndios. Qualquer aplicação prática exigiria mais anos e estações, avaliação regional e revisão humana.
