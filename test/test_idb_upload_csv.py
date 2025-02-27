import pytest
from src.idb_upload_csv import app  # Change the filename if necessary

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_upload_csv(client):
    # Test uploading a valid CSV file
    with open('/test_sales_data.csv', 'rb') as f:  # Create a sample CSV file for testing
        response = client.post('/upload/', data={'file': f})
    assert response.status_code == 200
    assert b'File uploaded successfully' in response.data

def test_get_sales(client):
    # Test retrieving sales data
    response = client.get('/sales/?page=1&page_size=5')
    assert response.status_code == 200
    assert 'total_sales' in response.json 