class StatusPrinter:
    def __init__(self):
        pass
    
    def print_depth(self, depth):
        print(f"Current depth: {depth}")
        
    def print_url(self, url):
        print(f"Current URL: {url}")
        
    def print_file(self, file_path):
        print(f"Saving file: {file_path}")
        
    def print_error(self, error_msg):
        print(f"Error occurred: {error_msg}")

