"""Gabriel Ferreira | RA 10442043 | turma 07N.

Analise inicial dos focos do INPE em janeiro e fevereiro de 2025.
Historico: 2026-09-25, Gabriel Ferreira, criacao da analise e exportacao.
"""

from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "dados" / "brutos" if (ROOT / "dados" / "brutos").exists() else ROOT
OUT = ROOT / "dados" / "processados"


def main():
    paths = sorted(RAW.glob("focos_mensal_br_20250[12].csv"))
    if len(paths) != 2:
        raise FileNotFoundError("Baixe os CSV de janeiro e fevereiro de 2025 indicados no README.")
    data = pd.concat((pd.read_csv(path, low_memory=False) for path in paths), ignore_index=True)
    data["data_hora_gmt"] = pd.to_datetime(data["data_hora_gmt"], errors="coerce", utc=True)
    quality = {
        "registros_brutos": int(len(data)),
        "ids_duplicados": int(data["id"].duplicated().sum()),
        "datas_invalidas": int(data["data_hora_gmt"].isna().sum()),
        "municipios_id_ausentes": int(data["municipio_id"].isna().sum()),
        "frp_ausente": int(data["frp"].isna().sum()),
        "satelites": {str(k): int(v) for k, v in data["satelite"].value_counts().items()},
    }
    # O satelite de referencia evita misturar detectores com sensibilidades distintas.
    ref = data.loc[data["satelite"].eq("AQUA_M-T")].drop_duplicates("id").copy()
    ref["semana_inicio"] = (ref["data_hora_gmt"].dt.normalize()
                            - pd.to_timedelta(ref["data_hora_gmt"].dt.weekday, unit="D"))
    counts = (ref.groupby(["municipio_id", "municipio", "estado", "semana_inicio"],
                          dropna=False).size().rename("focos").reset_index())
    counts["semana_inicio"] = counts["semana_inicio"].dt.strftime("%Y-%m-%d")
    OUT.mkdir(parents=True, exist_ok=True)
    counts.to_csv(OUT / "municipio_semana_observado.csv", index=False)
    summary = {
        "fonte": "INPE Programa Queimadas, CSV mensal Brasil, janeiro-fevereiro de 2025",
        "qualidade": quality,
        "satelite_referencia": "AQUA_M-T",
        "deteccoes_referencia": int(len(ref)),
        "municipios_observados": int(ref["municipio_id"].nunique()),
        "semanas_observadas": int(counts["semana_inicio"].nunique()),
        "municipio_semanas_com_foco": int(len(counts)),
        "focos_por_mes": {str(k): int(v) for k, v in ref.groupby(ref["data_hora_gmt"].dt.strftime("%Y-%m")).size().items()},
        "focos_por_bioma": {str(k): int(v) for k, v in ref["bioma"].value_counts().items()},
        "top_10_municipios": [
            {"municipio": str(m), "estado": str(e), "focos": int(n)}
            for (m, e), n in ref.groupby(["municipio", "estado"]).size().nlargest(10).items()
        ],
    }
    (OUT / "resumo_eda.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
