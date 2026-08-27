import logging

# Configure logging to show time, level (INFO/ERROR), and the message
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def divide_numbers(a, b):
    logging.info(f"Attempting to divide {a} by {b}")
    
    # try/except block 
    try:
        result = a / b
        logging.info(f"Success! Result is {result}")
        return result
    except ZeroDivisionError as e:
        # We use logging.error instead of print to flag an issue
        logging.error(f"Failed to divide: {e}")
        return None

# Run the function
#divide_numbers(10, 2)
divide_numbers(10, 0) # for the error log