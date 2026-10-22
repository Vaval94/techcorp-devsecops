from aiops.evidence import bound_logs, correlate, first_error_time, mask

# Faux secrets construits par concaténation : aucune valeur ne figure en clair
# dans le dépôt (sinon Gitleaks bloquerait légitimement le pipeline).
FAKE_GH = "ghp_" + "Ab1" * 12
FAKE_AWS = "AKIA" + "ABCDEFGHIJKLMNOP"


def test_mask_secrets_and_identifiers():
    line = (f"ERROR token={FAKE_GH} key {FAKE_AWS} Authorization: Bearer abc.def.ghi "
            "user=jane.doe@techcorp.example db=postgres://app:S3cr3t@db:5432/orders")
    out = mask(line)
    for secret in (FAKE_GH, FAKE_AWS, "abc.def.ghi", "jane.doe@techcorp.example", "S3cr3t"):
        assert secret not in out


def test_logs_are_filtered_and_bounded():
    lines = [f"INFO request {i} ok" for i in range(500)] + [f"ERROR db_connection_timeout {i}" for i in range(100)]
    kept, stats = bound_logs(lines, max_lines=20, max_chars=50)
    assert len(kept) == 20
    assert all("ERROR" in l for l in kept)
    assert stats == {"lignes_lues": 600, "lignes_pertinentes": 100, "lignes_conservées": 20}


def test_long_lines_are_truncated():
    kept, _ = bound_logs(["ERROR " + "x" * 1000], max_chars=100)
    assert len(kept[0]) < 120 and kept[0].endswith("[tronqué]")


def test_correlation_is_not_causation():
    change = {"version": "2.4.7", "deployed_at": "2026-10-22T10:15:00Z"}
    first = first_error_time(["2026-10-22T10:17:02Z ERROR db_connection_timeout route=/orders"])
    c = correlate(change, first)
    assert c["délai_minutes"] == 2.0
    assert "PAS une preuve" in c["lecture"]
