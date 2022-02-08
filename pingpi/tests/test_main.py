from fastapi.testclient import TestClient
from pathlib import Path
import json

from pingpi.main import app

HERE = Path(__file__).parent

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "FastAPI - Swagger UI" in response.text


def test_upload_file():
    file_name = 'pings.csv'
    csv_path = HERE / 'data' / file_name
    response = client.post(
        "/upload/",
        files={
            'file': (
                file_name,
                open(csv_path, 'rb'),
                'text/csv',
                {'Expires': '0'},
            )
        },
    )
    assert response.status_code == 200
    response_dict = response.json()
    assert response_dict.get("status") == "success"
    assert response_dict.get("original_filename") == file_name
    assert isinstance(response_dict.get("id"), str) is True


def test_get_data():
    file_name = 'pings.csv'
    csv_path = HERE / 'data' / file_name
    json_path = HERE / 'data' / 'pings.json'
    response = client.post(
        "/upload/",
        files={
            'file': (
                file_name,
                open(csv_path, 'rb'),
                'text/csv',
                {'Expires': '0'},
            )
        },
    )
    assert response.status_code == 200
    response_dict = response.json()
    file_id = response_dict.get("id")

    response = client.get(
        f"/data/{file_id}",
    )
    assert response.status_code == 200
    response_dict = response.json()

    assert isinstance(response_dict, list) is True
    assert response_dict == json.loads(json_path.read_text())
