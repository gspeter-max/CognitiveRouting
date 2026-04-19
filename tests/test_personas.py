from dataclasses import FrozenInstanceError

import pytest

from cognitive_routing.personas import Persona, load_personas


def test_load_personas_returns_three_stable_personas():
    personas = load_personas()

    assert len(personas) == 3
    assert personas[0].bot_id == "bot_a"
    assert personas[1].bot_id == "bot_b"
    assert personas[2].bot_id == "bot_c"
    assert isinstance(personas[0], Persona)
    assert personas[0].tags == ("tech", "ai", "crypto", "space")


def test_persona_is_immutable():
    persona = load_personas()[0]

    with pytest.raises(FrozenInstanceError):
        persona.bot_name = "Changed"
