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
        ("*y *M", "[*y *m *d *H *M]")
    ]
    for config, result in tests:
        print("config", config)
        assert str(Calendar.from_config(config)) == result


def test_normal():
    dt = datetime(2018, 7, 13, 11, 58, 5)
    assert Calendar(month=EVERY(), day=15).next_event(dt) == datetime(2018, 7, 16)
    assert Calendar(year=EVERY(2), week=EVERY(2), day=1).next_event(dt) == datetime(2018, 7, 24)
    assert Calendar().next_event(dt) == datetime(2018, 7, 13, 11, 58, 6)


def test_calendar():
    dt = datetime.now()
    dt = dt.replace(hour=15)
    print(dt)
    cal = Calendar.from_config("weekly")
    print(cal)
    print(cal.next_event(dt))
