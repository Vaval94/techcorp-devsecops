from aiops.detector import detect_anomaly, evaluate, make_report


# --- Tests fournis par le sujet (conservés)
def test_threshold():
    assert not detect_anomaly(2)
    assert detect_anomaly(3)


def test_approval_required():
    assert make_report(4, [], 'pending')['human_approval_required'] is True


# --- Détection enrichie
def test_incident_detected_and_explained():
    """10 HTTP 500 sur 10 requêtes, baseline calme : anomalie critique."""
    v = evaluate(errors_now=10, total_now=10, baseline=[0, 0, 0, 0, 0, 0])
    assert v["anomalie"] is True
    assert v["severite"] == "critique"
    assert v["regles"] == {"seuil_absolu": True, "taux_erreur": True, "z_score": True}
    assert len(v["raisons"]) == 3


def test_low_volume_is_not_an_anomaly():
    """2 erreurs : sous le seuil, même avec 100 % d'erreurs."""
    v = evaluate(errors_now=2, total_now=2, baseline=[0] * 6)
    assert v["anomalie"] is False


def test_threshold_alone_is_not_enough_with_high_traffic():
    """3 erreurs sur 10 000 requêtes et niveau habituel : le seuil seul déclencherait à tort."""
    assert detect_anomaly(3) is True
    v = evaluate(errors_now=3, total_now=10_000, baseline=[3, 2, 4, 3, 3, 2])
    assert v["anomalie"] is False


def test_zscore_detects_unusual_spike():
    """Taux faible mais hausse brutale par rapport à la baseline glissante."""
    v = evaluate(errors_now=40, total_now=2_000, baseline=[2, 3, 2, 4, 3, 2, 3])
    assert v["regles"]["taux_erreur"] is False
    assert v["regles"]["z_score"] is True
    assert v["anomalie"] is True
    assert v["z_score"] > 3


def test_missing_baseline_falls_back_on_rate():
    v = evaluate(errors_now=5, total_now=6, baseline=[0, 0])
    assert v["z_score"] is None
    assert v["anomalie"] is True


def test_no_traffic_no_division_error():
    v = evaluate(errors_now=0, total_now=0, baseline=[])
    assert v["anomalie"] is False and v["error_rate_pct"] == 0.0
