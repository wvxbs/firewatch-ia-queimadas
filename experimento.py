"""FireWatch IA | Gabriel Ferreira | RA 10442043 | turma 07N.

Experimento retrospectivo com dados de janeiro e fevereiro de 2025.
Histórico: 2026-11-20, Gabriel Ferreira, versão para revisão da Parte 3.
"""

import csv
import json
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, precision_recall_fscore_support
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "dados/brutos" if (ROOT / "dados/brutos").exists() else ROOT
WEEKS = [date(2025, 1, 6) + timedelta(weeks=i) for i in range(7)]


def load_data():
    counts = Counter()
    names = {}
    ids = set()
    for path in sorted(RAW.glob("focos_mensal_br_20250[12].csv")):
        with path.open(newline="", encoding="utf-8") as stream:
            for row in csv.DictReader(stream):
                municipality = row["municipio_id"]
                ids.add(municipality)
                names[municipality] = (row["municipio"], row["estado"])
                if row["satelite"] == "AQUA_M-T":
                    day = date.fromisoformat(row["data_hora_gmt"][:10])
                    week = day - timedelta(days=day.weekday())
                    counts[week, municipality] += 1
    if len(ids) < 1000 or len(counts) < 1000:
        raise ValueError("Dados de origem ausentes ou incompletos")
    return counts, names, sorted(ids)


def examples(counts, ids):
    batches = []
    for current, target in zip(WEEKS[:-1], WEEKS[1:]):
        previous = current - timedelta(weeks=1)
        features = np.array([
            [counts[current, municipality], counts[previous, municipality]]
            for municipality in ids
        ], dtype=float)
        actual = np.array([counts[target, municipality] for municipality in ids])
        nonzero = actual[actual > 0]
        # Empates no corte entram todos; nenhuma semana rotula municípios com zero.
        threshold = int(np.quantile(nonzero, .9, method="higher"))
        labels = (actual >= threshold).astype(int)
        assert threshold > 0 and 0 < labels.sum() < len(labels)
        batches.append((target, features, labels, threshold))
    return batches


def score(y, prediction):
    predicted = (prediction >= .5).astype(int)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y, predicted, average="binary", zero_division=0
    )
    top50 = np.argsort(-prediction, kind="stable")[:50]
    return {
        "average_precision": round(float(average_precision_score(y, prediction)), 4),
        "precisao_0_5": round(float(precision), 4),
        "revocacao_0_5": round(float(recall), 4),
        "f1_0_5": round(float(f1), 4),
        "revocacao_top50": round(float(y[top50].sum() / y.sum()), 4),
    }


def main():
    counts, names, ids = load_data()
    batches = examples(counts, ids)
    rows = []
    last_predictions = None
    for test_index in range(3, len(batches)):
        week, x_test, y_test, threshold = batches[test_index]
        x_train = np.concatenate([batch[1] for batch in batches[:test_index]])
        y_train = np.concatenate([batch[2] for batch in batches[:test_index]])
        models = {
            "logistica": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, class_weight="balanced")),
            "floresta": RandomForestClassifier(n_estimators=100, min_samples_leaf=20, class_weight="balanced", random_state=42),
        }
        predictions = {"persistencia": x_test[:, 0]}
        for name, model in models.items():
            model.fit(x_train, y_train)
            predictions[name] = model.predict_proba(x_test)[:, 1]
        for name, values in predictions.items():
            rows.append({"semana_alvo": week.isoformat(), "modelo": name,
                         "limiar_focos_classe_positiva": threshold,
                         "positivos": int(y_test.sum()), **score(y_test, values)})
        if test_index == len(batches) - 1:
            last_predictions = (week, y_test, predictions)

    output = ROOT / "resultados"
    output.mkdir(exist_ok=True)
    with (output / "metricas.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    week, actual, predictions = last_predictions
    with (output / "ranking_retrospectivo.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["semana_alvo", "municipio_id", "municipio", "estado", "classe_real",
                         "probabilidade_floresta", "pontuacao_persistencia"])
        for index in np.argsort(-predictions["floresta"], kind="stable")[:50]:
            municipality = ids[index]
            writer.writerow([week, municipality, *names[municipality], int(actual[index]),
                             round(float(predictions["floresta"][index]), 5),
                             int(predictions["persistencia"][index])])
    summary = {
        "universo_municipios_observados_em_qualquer_satelite": len(ids),
        "semanas_completas": [week.isoformat() for week in WEEKS],
        "protocolo": "validação temporal expansiva; treino nas semanas anteriores e teste em uma semana posterior",
        "definicao_positivo": "decil superior das contagens positivas por semana; empates incluídos",
        "metrica_principal": "average precision (resumo da curva precisão-revocação)",
        "resultados": rows,
    }
    (output / "resumo.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
