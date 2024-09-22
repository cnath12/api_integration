from db.database import DatabaseManager
from config import COSMOS_CONFIG
import uuid

def test_cosmos_connection():
    db_manager = DatabaseManager(**COSMOS_CONFIG)
    
    # Generate a unique ID for this test run
    test_id = f"test_user_{uuid.uuid4().hex[:8]}"
    
    # Test item creation
    test_item = {
        "id": test_id,
        "name": "Chirag",
        "email": "chirag@example.com",
        "job": "Developer"
    }
    
    try:
        # Create item
        created_item = db_manager.create_item(test_item)
        print(f"Created item: {created_item}")
        assert created_item['id'] == test_id, "Created item ID doesn't match"

        # Read item
        read_item = db_manager.read_item(test_item['id'], test_item['id'])
        print(f"Read item: {read_item}")
        assert read_item['id'] == test_id, "Read item ID doesn't match"

        # Update item
        test_item['job'] = "Senior Developer"
        updated_item = db_manager.update_item(test_item['id'], test_item)
        print(f"Updated item: {updated_item}")
        assert updated_item['job'] == "Senior Developer", "Job update failed"

        # Query items (with partition key)
        query = "SELECT * FROM c WHERE c.id = @id"
        parameters = [{"name": "@id", "value": test_id}]
        items = db_manager.query_items(query, parameters)
        print(f"Queried items: {items}")
        assert len(items) == 1 and items[0]['id'] == test_id, "Query with partition key failed"

        # Query items (cross-partition)
        query = "SELECT * FROM c WHERE c.name = @name"
        parameters = [{"name": "@name", "value": "Chirag"}]
        items = db_manager.query_items(query, parameters)
        print(f"Cross-partition queried items: {items}")
        assert len(items) >= 1 and any(item['id'] == test_id for item in items), "Cross-partition query failed"

        # Delete item
        db_manager.delete_item(test_item['id'], test_item['id'])
        print("Item deleted successfully")

        # Verify deletion
        query = "SELECT * FROM c WHERE c.id = @id"
        parameters = [{"name": "@id", "value": test_id}]
        items = db_manager.query_items(query, parameters)
        assert len(items) == 0, "Deletion verification failed"

        print("All operations completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup: Ensure the test item is deleted even if an error occurred
        try:
            db_manager.delete_item(test_id, test_id)
        except:
            pass

if __name__ == "__main__":
    test_cosmos_connection()