from pathlib import Path
from streamlit.testing.v1 import AppTest


def test_application_default_and_fea():
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1]/"app.py"), default_timeout=60)
    app.run()
    assert not app.exception
    assert app.title[0].value == "See stress through light."
    assert len(app.metric) == 4
    app.selectbox[0].select("Finite plate · FEA").run()
    assert not app.exception
    assert any("Finite plate" in message.value for message in app.info)
    next(button for button in app.button if button.label == "Run physics checks").click().run()
    assert not app.exception
    assert len(app.success) == 7
    next(button for button in app.button if button.label == "Run reconstruction").click().run()
    assert not app.exception
    assert any(metric.label == "RMSE on resolved pixels" for metric in app.metric)
