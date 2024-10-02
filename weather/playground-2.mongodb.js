// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// The current database to use.
use('test_db');

// Create a new document in the collection.
db.getCollection('test_collection').insertOne({
    request_id_1 : {
        cities : [
            {
                created_at: 2323232,
                city_id: 1,
                temperature: 1,
                humidity: 1
            }
        ]
        
    }
});
