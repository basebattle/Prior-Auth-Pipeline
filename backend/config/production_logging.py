import logging

def setup_enterprise_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    print("Project 3: Enterprise logging initialized.")

if __name__ == "__main__":
    setup_enterprise_logging()
