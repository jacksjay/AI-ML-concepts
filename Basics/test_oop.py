# Import the Document class from the 2_oop.py file we made earlier
from oop import Document

def test_document_summary():
    # 1. Setup: Create test data
    doc = Document("Test Doc", "One two three four five six seven.")
    
    # 2. Action: Run the method we want to test
    summary = doc.get_summary()
    
    # 3. Assert: Check if the result matches our expectations
    # We expect the first 5 words + "..."
    assert summary == "One two three four five..."
    
    # Pytest will pass if the assert is True, and fail if it's False