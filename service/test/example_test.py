from base import BaseTestCase


class TestItemRoutes(BaseTestCase):
    def test_create_item(self):
        """
        Testa o endpoint POST /items para criar um item.
        """
        payload = {
            "name": "Test Item",
            "description": "A test item for the API",
            "price": 10.99,
            "in_stock": True,
        }
        response = self.client.post("/items/", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], payload["name"])

    def test_get_item(self):
        """
        Testa o endpoint GET /items/{item_id} para buscar um item.
        """
        # Primeiro cria um item
        payload = {
            "name": "Test Item",
            "description": "A test item for the API",
            "price": 10.99,
            "in_stock": True,
        }
        post_response = self.client.post("/items/", json=payload)
        self.assertEqual(post_response.status_code, 201)
        item_id = post_response.json()["id"]

        # Busca o item criado
        get_response = self.client.get(f"/items/{item_id}")
        self.assertEqual(get_response.status_code, 200)
        data = get_response.json()
        self.assertEqual(data["id"], item_id)
        self.assertEqual(data["name"], payload["name"])

    def test_list_items(self):
        """
        Testa o endpoint GET /items para listar todos os itens.
        """
        # Insere dois itens
        self.client.post(
            "/items/",
            json={
                "name": "Item 1",
                "description": "Desc 1",
                "price": 5.0,
                "in_stock": True,
            },
        )
        self.client.post(
            "/items/",
            json={
                "name": "Item 2",
                "description": "Desc 2",
                "price": 15.0,
                "in_stock": False,
            },
        )

        # Lista os itens
        response = self.client.get("/items/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(len(data), 2)

    def test_update_item(self):
        """
        Testa o endpoint PUT /items/{item_id} para atualizar um item.
        """
        # Primeiro cria um item
        payload = {
            "name": "Original Item",
            "description": "Original Description",
            "price": 20.0,
            "in_stock": True,
        }
        post_response = self.client.post("/items/", json=payload)
        self.assertEqual(post_response.status_code, 201)
        item_id = post_response.json()["id"]

        # Atualiza o item
        update_payload = {
            "name": "Updated Item",
            "description": "Updated Description",
            "price": 25.0,
            "in_stock": False,
        }
        put_response = self.client.put(f"/items/{item_id}", json=update_payload)
        self.assertEqual(put_response.status_code, 200)
        data = put_response.json()
        self.assertEqual(data["name"], update_payload["name"])
        self.assertEqual(data["price"], update_payload["price"])

    def test_delete_item(self):
        """
        Testa o endpoint DELETE /items/{item_id} para excluir um item.
        """
        # Primeiro cria um item
        payload = {
            "name": "Item to Delete",
            "description": "Will be deleted",
            "price": 30.0,
            "in_stock": True,
        }
        post_response = self.client.post("/items/", json=payload)
        self.assertEqual(post_response.status_code, 201)
        item_id = post_response.json()["id"]

        # Deleta o item
        delete_response = self.client.delete(f"/items/{item_id}")
        self.assertEqual(delete_response.status_code, 204)

        # Tenta buscar o item deletado
        get_response = self.client.get(f"/items/{item_id}")
        self.assertEqual(get_response.status_code, 404)
