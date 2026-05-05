def test_system_flow():
    # Example: Testing if file writing + reading works together
    test_data = "System check"
    with open("temp.txt", "w") as f:
        f.write(test_data)

    with open("temp.txt", "r") as f:
        assert f.read() == test_data

    import os
    os.remove("temp.txt")