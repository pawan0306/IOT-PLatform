import json


def validate_instance(stype):
    sensor_types = {}
    with open("sensor_repository.json", "r") as f:
        sensor_types = json.load(f)

    if stype in sensor_types:
        return True
    else:
        return False


if __name__ == "__main__":
    print(validate_instance('gas'))