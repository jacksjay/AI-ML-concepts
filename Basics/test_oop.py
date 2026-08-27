# Import the Document class from the 2_oop.py file we made earlier
from oop import Document

def test_document_summary():
    #  Create test data
    doc = Document("Test Doc", "One two three four five six seven.")
    
    # Run the method we want to test
    summary = doc.get_summary()
    
    # 3. Assert: Check if the result matches our expectations
    # here expect the first 5 words + "..."
    assert summary == "One two three four five..."
    