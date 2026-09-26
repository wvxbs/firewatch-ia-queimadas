# FireWatch IA — Parte 2

Projeto individual de Gabriel Ferreira (RA 10442043), turma 07N, Inteligência Artificial, Universidade Presbiteriana Mackenzie.

Este repositório contém o artigo parcial em PDF, os CSV oficiais do Programa Queimadas do INPE de janeiro e fevereiro de 2025, o script de análise exploratória e seus resultados. O objetivo do projeto completo é prever quais municípios estarão entre os 10% com maior concentração de focos na semana seguinte. **Nenhum modelo preditivo foi treinado nesta etapa.**

## Dados

Fonte: [Programa Queimadas do INPE](https://www.terrabrasilis.dpi.inpe.br/queimadas/portal/pages/secao_downloads/dados-abertos/index.html), série mensal Brasil, arquivos baixados em 25/09/2026:

- [janeiro de 2025](https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/mensal/Brasil/focos_mensal_br_202501.csv)
- [fevereiro de 2025](https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/mensal/Brasil/focos_mensal_br_202502.csv)

Os arquivos brutos ficam em `dados/brutos/` na pasta local do projeto e na raiz deste repositório público. Contêm detecções de diversos satélites; a agregação temporal usa apenas `AQUA_M-T` para evitar misturar sensores. `municipio_semana_observado.csv` inclui apenas municípios e semanas com detecção. Ele **não** pode ser usado diretamente para treinar a classificação, pois faltam os pares com zero foco.

## Reproduzir a análise

Requer Python 3 e pandas.

```sh
python3 analise_exploratoria.py
```

O script gera `dados/processados/resumo_eda.json` e `dados/processados/municipio_semana_observado.csv`; cópias desses resultados também estão na raiz para consulta direta. Os CSV de origem têm 104.240 registros; 4.956 pertencem ao satélite de referência, em 1.607 municípios observados e nove semanas de calendário. O código verifica IDs duplicados, datas inválidas, códigos de município ausentes e ausência de FRP.

## Limites e próximos passos

O recorte cobre somente janeiro e fevereiro de 2025 e não captura o ciclo sazonal completo. Ainda faltam os dados de 2019–2025, o painel completo de municípios com contagens zero, atributos históricos, treinamento, validação temporal, métricas de desempenho e explicações SHAP. Os números atuais são descritivos de detecções, não da área queimada nem do risco de cada município.

O artigo segue o template da SBC fornecido pela disciplina. A IA generativa OpenAI Codex auxiliou na redação, formatação e elaboração do script; a responsabilidade pelo conteúdo é do estudante.
