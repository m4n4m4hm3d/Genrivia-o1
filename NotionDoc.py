NOTION_TOKEN = 'enter your notion Token' 
DATABASE_ID = 'enter your notion Database id'

from notion_client import Client

notion = Client(auth=NOTION_TOKEN) 


def find_page_by_user_id(database_id, user_id):
    query = notion.databases.query(
        **{
            "database_id": database_id,
            "filter": {
                "property": "User ID",
                "rich_text": {
                    "equals": str(user_id)
                }
            }
        }
    )
    results = query.get("results")
    if results:
        return results[0] 
    return None


def append_chat_to_page(page_id, message, output):
    page = notion.pages.retrieve(page_id=page_id)
    chat_data = page["properties"]["Chat Data"]["rich_text"]
    
  
    existing_messages = "".join([entry["text"]["content"] for entry in chat_data])
    message_count = existing_messages.count("q") + 1  
    
    
    formatted_message = f"\nq{message_count}: {message}\nAI: {output}"
    updated_chat_data = existing_messages + formatted_message


    notion.pages.update(
        page_id=page_id,
        properties={
            "Chat Data": {
                "rich_text": [
                    {"text": {"content": updated_chat_data}}
                ]
            }
        }
    )


# Main function to save or update chat data
def save_chat(database_id, user_id, message, output):
    # Check if a page already exists for the user ID
    existing_page = find_page_by_user_id(database_id, user_id)
    
    if existing_page:
        # Update the existing page
        append_chat_to_page(existing_page["id"], message, output)
    else:
        # Create a new page if no existing page is found
        data = {
            "User ID": {  
                "title": [
                    {"text": {"content": str(user_id)}}
                ]
            },
            "Chat Data": {  
                "rich_text": [
                    {"text": {"content": f"q1: {message}\nAI: {output}"}}
                ]
            }
        }
        notion.pages.create(
            parent={"database_id": database_id},
            properties=data
        )


save_chat(DATABASE_ID, user_id, message, output)
