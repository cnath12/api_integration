from azure.cosmos import CosmosClient, PartitionKey

class DatabaseManager:
    def __init__(self, endpoint, key, database_name, container_name):
        self.client = CosmosClient(endpoint, key)
        self.database = self.client.get_database_client(database_name)
        self.container = self.database.get_container_client(container_name)

    def create_item(self, item):
        return self.container.create_item(body=item)

    def read_item(self, item_id, partition_key):
        return self.container.read_item(item=item_id, partition_key=partition_key)

    def update_item(self, item_id, updated_item):
        return self.container.upsert_item(body=updated_item)

    def delete_item(self, item_id, partition_key):
        return self.container.delete_item(item=item_id, partition_key=partition_key)

    def query_items(self, query, parameters=None):
        return list(self.container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))