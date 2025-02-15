import unittest
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
import models

client = TestClient(app)

# Helper to manage the session
def get_test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        models.Base.metadata.create_all(bind=SessionLocal().bind)

    @classmethod
    def tearDownClass(cls):
        models.Base.metadata.drop_all(bind=SessionLocal().bind)

    def setUp(self):
        self.db = next(get_test_db())
        self.db.begin()  # Start a new transaction

    def tearDown(self):
        self.db.rollback()  # Rollback transaction to discard changes

    def test_create_empresa(self):
        empresa_data = {
            "nome": "Empresa A",
            "cnpj": "12.345.678/0001-99",
            "endereco": "Rua A, 123",
            "email": "empresaa@exemplo.com",
            "telefone": "1234567890"
        }
        response = client.post("/empresas/", json=empresa_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nome"], empresa_data["nome"])
        self.assertEqual(response.json()["cnpj"], empresa_data["cnpj"])

    def test_get_empresas(self):
        response = client.get("/empresas/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_empresa_by_id(self):
        empresa_data = {
            "nome": "Empresa B",
            "cnpj": "98.765.432/0001-10",
            "endereco": "Rua B, 456",
            "email": "empresab@exemplo.com",
            "telefone": "0987654321"
        }
        create_response = client.post("/empresas/", json=empresa_data)
        empresa_id = create_response.json()["id"]
        
        response = client.get(f"/empresas/{empresa_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], empresa_id)

    def test_create_obrigacao(self):
        obrigacao_data = {
            "nome": "Declaração A",
            "periodicidade": "mensal",
            "empresa_id": 1
        }
        response = client.post("/obrigacoes/", json=obrigacao_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nome"], obrigacao_data["nome"])

    def test_get_obrigacoes(self):
        response = client.get("/obrigacoes/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_obrigacao_by_id(self):
        obrigacao_data = {
            "nome": "Declaração B",
            "periodicidade": "anual",
            "empresa_id": 1
        }
        create_response = client.post("/obrigacoes/", json=obrigacao_data)
        obrigacao_id = create_response.json()["id"]
        
        response = client.get(f"/obrigacoes/{obrigacao_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], obrigacao_id)

    def test_edit_obrigacao(self):
        obrigacao_data = {
            "nome": "Declaração C",
            "periodicidade": "trimestral",
            "empresa_id": 1
        }
        create_response = client.post("/obrigacoes/", json=obrigacao_data)
        obrigacao_id = create_response.json()["id"]
        
        updated_data = {
            "nome": "Declaração Atualizada",
            "periodicidade": "anual",
            "empresa_id": 1
        }
        response = client.put(f"/obrigacoes/{obrigacao_id}", json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nome"], "Declaração Atualizada")

    def test_delete_obrigacao(self):
        obrigacao_data = {
            "nome": "Declaração D",
            "periodicidade": "mensal",
            "empresa_id": 1
        }
        create_response = client.post("/obrigacoes/", json=obrigacao_data)
        obrigacao_id = create_response.json()["id"]
        
        response = client.delete(f"/obrigacoes/{obrigacao_id}")
        self.assertEqual(response.status_code, 200)

    def test_edit_empresa(self):
        empresa_data = {
            "nome": "Empresa C",
            "cnpj": "12.345.678/0001-98",
            "endereco": "Rua C, 789",
            "email": "empresac@exemplo.com",
            "telefone": "1230987654"
        }
        create_response = client.post("/empresas/", json=empresa_data)
        empresa_id = create_response.json()["id"]
        
        updated_data = {
            "nome": "Empresa Atualizada",
            "cnpj": "12.345.678/0001-98",
            "endereco": "Rua D, 1010",
            "email": "empresad@exemplo.com",
            "telefone": "9876543210"
        }
        response = client.put(f"/empresas/{empresa_id}", json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nome"], "Empresa Atualizada")

    def test_delete_empresa(self):
        empresa_data = {
            "nome": "Empresa E",
            "cnpj": "12.345.678/0001-88",
            "endereco": "Rua E, 1111",
            "email": "empresae@exemplo.com",
            "telefone": "5555555555"
        }
        create_response = client.post("/empresas/", json=empresa_data)
        empresa_id = create_response.json()["id"]
        
        response = client.delete(f"/empresas/{empresa_id}")
        self.assertEqual(response.status_code, 200)
