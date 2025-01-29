def test_target_creation():
    from src.target import Target

    target = Target(100, 150, 30)
    assert target.x == 100
    assert target.y == 150
    assert target.size == 30

def test_target_click_detection():
    from src.target import Target

    target = Target(100, 150, 30)
    assert target.is_clicked(110, 160) == True
    assert target.is_clicked(200, 200) == False