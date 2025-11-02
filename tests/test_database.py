
import unittest
import sqlite3
from datetime import datetime, timezone
import os

# We need to adjust the path to import from the parent directory
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        """Set up a temporary, in-memory database for each test."""
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row # Use dictionary-like rows
        # Monkey-patch the get_db_connection to use our in-memory db
        database.get_db_connection = lambda: self.conn
        database.create_database()

    def tearDown(self):
        """Close the database connection after each test."""
        self.conn.close()

    def test_create_database(self):
        """Test if tables are created successfully."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hosts'")
        self.assertIsNotNone(cursor.fetchone(), "'hosts' table should be created.")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='models'")
        self.assertIsNotNone(cursor.fetchone(), "'models' table should be created.")

    def test_add_or_update_host(self):
        """Test adding a new host and updating an existing one."""
        # 1. Add a new host
        ip = "127.0.0.1"
        performance = "High-Performance"
        host_id = database.add_or_update_host(ip, performance)
        self.assertIsNotNone(host_id, "Should return a host ID for a new host.")

        # Verify the host was added
        host = database.get_host_by_ip(ip)
        self.assertEqual(host['ip_address'], ip)
        self.assertEqual(host['performance'], performance)
        self.assertEqual(host['is_alive'], 1)

        # 2. Update the same host
        new_performance = "Mid-Range"
        updated_host_id = database.add_or_update_host(ip, new_performance, is_alive=0)
        self.assertEqual(host_id, updated_host_id, "Should return the same host ID when updating.")

        # Verify the host was updated
        updated_host = database.get_host_by_ip(ip)
        self.assertEqual(updated_host['performance'], new_performance)
        self.assertEqual(updated_host['is_alive'], 0)

    def test_add_models(self):
        """Test adding models for a host."""
        host_id = database.add_or_update_host("192.168.1.1", "Test-Performance")
        
        models_to_add = [
            {'name': 'llama3:latest', 'modified_at': datetime.now(timezone.utc).isoformat(), 'parameter_size': '8B', 'quantization_level': 'Q4_0'},
            {'name': 'codellama:latest', 'modified_at': datetime.now(timezone.utc).isoformat(), 'parameter_size': '7B', 'quantization_level': 'Q5_K_M'}
        ]
        
        database.add_models(host_id, models_to_add)

        # Verify models were added
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM models WHERE host_id = ?", (host_id,))
        added_models = cursor.fetchall()
        self.assertEqual(len(added_models), 2)
        self.assertEqual(added_models[0]['name'], 'llama3:latest')

    def test_mark_host_as_dead(self):
        """Test marking a host as not alive."""
        host_id = database.add_or_update_host("10.0.0.1", "Test-Performance")
        database.mark_host_as_dead(host_id)
        
        host = database.get_host_by_ip("10.0.0.1")
        self.assertEqual(host['is_alive'], 0)

    def test_clear_models_for_host(self):
        """Test clearing all models for a specific host."""
        host_id = database.add_or_update_host("10.0.0.2", "Test-Performance")
        models_to_add = [
            {'name': 'test-model:latest', 'modified_at': 'N/A', 'parameter_size': '1B', 'quantization_level': 'Q8'}
        ]
        database.add_models(host_id, models_to_add)

        # Verify model exists
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM models WHERE host_id = ?", (host_id,))
        self.assertEqual(cursor.fetchone()[0], 1)

        # Clear models and verify
        database.clear_models_for_host(host_id)
        cursor.execute("SELECT COUNT(*) FROM models WHERE host_id = ?", (host_id,))
        self.assertEqual(cursor.fetchone()[0], 0)

if __name__ == '__main__':
    unittest.main()
