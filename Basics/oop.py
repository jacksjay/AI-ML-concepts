class Document:
    # The __init__ method runs when you create a new Document object
    def __init__(self, title, content):
        self.title = title       # Attribute
        self.content = content   # Attribute
        
    # A method (function inside a class)
    def get_summary(self):
        """Returns the first 5 words of the content."""
        words = self.content.split()
        summary_words = words[:5] # Slice the list to get first 5 items
        # Join them back into a single string
        return " ".join(summary_words) + "..."

# --- How to use the class ---
if __name__ == "__main__":
    # Create an "instance" of the Document class
    my_doc = Document("AI History", "Artificial intelligence began in the 1950s with Alan Turing.")
    
    print(f"Title: {my_doc.title}")
    print(f"Summary: {my_doc.get_summary()}")