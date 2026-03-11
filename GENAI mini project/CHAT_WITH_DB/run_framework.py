import os
import sys
from db_chatbot import DatabaseChatbot

def main():
    print("=== Database Chatbot Framework ===")
    
    # Hardcoded folder path as requested
    folder_path = r"c:\Users\acer\OneDrive - ELCOT\mcp 1"
    
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        return
            
    print(f"\nInitializing chatbot for folder: {os.path.abspath(folder_path)}...")
    print("This may take a moment to discover databases and tables...")
    
    try:
        # Initialize the framework
        bot = DatabaseChatbot(db_directory=folder_path)
        
        session_id = input("ENTER YOUR SESSION ID (or press Enter for 'default'): ").strip() or "default"
        
        print("\nChatbot Ready! Type 'exit' to quit.")
        
        while True:
            query = input(f"\n[{session_id}] YOU: ").strip()
            
            if query.lower() == 'exit':
                print("GOOD BYE")
                break
                
            if not query:
                continue
                
            try:
                response = bot.chat(query, session_id)
                print(f"AI: {response}")
            except Exception as e:
                print(f"Error during chat: {e}")
                
    except Exception as e:
        print(f"Failed to initialize framework: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
