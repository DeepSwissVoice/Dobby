from datetime import datetime

from dobby.models.calendar import Calendar, EVERY


def test_config():
    tests = [
        ("yearly", "[*y]"),
        ("monthly", "[*y *m]"),
        ("weekly", "[*y *w]"),
        ("daily", "[*y *m *d]"),
        ("hourly", "[*y *m *d *H]"),
        ("minutely", "[*y *m *d *H *M]"),
        ("secondly", "[*y *m *d *H *M *S]")
    ]
    for config, result in tests:
        print("config", config)
        assert str(Calendar.from_config(config)) == result


def test_repr():
    tests = [
        ("[*y @3m]", "[*y @3m]"),
        ("*y *M", "[*y *m *d *H *M]"),
        ("  5M]", "[*y *m *d *H 5M]")
    ]
    for config, result in tests:
        print("config", config)
        assert str(Calendar.from_config(config)) == result


def test_normal():
    dt = datetime(2018, 7, 13, 11, 58, 5)
    assert Calendar(month=EVERY(), day=15).next_event(dt) == datetime(2018, 7, 16)
    assert Calendar(year=EVERY(2), week=EVERY(2), day=1).next_event(dt) == datetime(2018, 7, 24)
    assert Calendar().next_event(dt) == datetime(2018, 7, 13, 11, 58, 6)
    assert Calendar(month=7).next_event(dt) == datetime(2018, 8, 1)
    assert Calendar(month=5, day=7).next_event(dt) == datetime(2019, 6, 8)
    assert Calendar(day=EVERY(12)).next_event(dt) == datetime(2018, 7, 25)

    dt = datetime(2018, 7, 25, 12, 56)
    assert Calendar.from_config("weekly").next_event(dt) == datetime(2018, 7, 30)
    assert Calendar.from_config("monthly").next_event(dt) == datetime(2018, 8, 1)


def test_calendar():
    dt = datetime.now()
    dt = dt.replace(hour=15)
    print(dt)
    cal = Calendar.from_config("weekly")
    print(cal)
    print(cal.next_event(dt))
