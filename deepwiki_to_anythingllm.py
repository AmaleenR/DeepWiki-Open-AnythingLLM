from dotenv import load_dotenv
import os
import requests

load_dotenv()
 
# --- CONFIG ---
BASE_URL = os.getenv("ANYTHINGLLM_API_URL")
ANYTHINGLLM_API_UPLOAD = f"{BASE_URL}/document/upload"  # API endpoint
ANYTHINGLLM_API_LIST = f"{BASE_URL}/documents"
WORKSPACE_SLUG = "deepwiki-anythingllm-uob" 
ANYTHINGLLM_API_UPDATE_EMBEDS = f"{BASE_URL}/workspace/{WORKSPACE_SLUG}/update-embeddings"

API_KEY = os.getenv("ANYTHINGLLM_API_KEY")  # From AnythingLLM settings
LOCAL_FOLDER = r"C:\Users\aahmadridzuanullah\.adalflow\wikicache"  # Folder containing .md or .json files
 
headers = {
    "Authorization": f"Bearer {API_KEY}"
}
 
def get_existing_docs():
    """Fetch all files inside 'custom-documents' from AnythingLLM, returning both titles and full paths."""
    try:
        response = requests.get(ANYTHINGLLM_API_LIST, headers=headers)
        response.raise_for_status()
        data = response.json()
 
        titles = set()  # Unique titles
        names = []      # Full path names (custom-documents/<filename>)
 
        def extract_custom_docs(items, inside_custom=False):
            for item in items:
                if item["type"] == "folder":
                    # Check if this is the 'custom-documents' folder
                    if item["name"] == "custom-documents":
                        extract_custom_docs(item["items"], inside_custom=True)
                    else:
                        extract_custom_docs(item["items"], inside_custom=inside_custom)
                elif item["type"] == "file" and inside_custom:
                    full_name = f"custom-documents/{item['name']}"
                    titles.add(item["title"])
                    names.append(full_name)
 
        if "localFiles" in data:
            extract_custom_docs(data["localFiles"]["items"])
 
        return titles, names
 
    except Exception as e:
        print(f"⚠️ Failed to fetch existing documents: {e}")
        return set(), []
 
def upload_file(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        files = {
            "file": (filename, f, "application/octet-stream"),
        }
        data = {
            "addToWorkspaces": WORKSPACE_SLUG
        }
        # response = requests.post(ANYTHINGLLM_API_UPLOAD, headers=headers, files=files, data=data)
        response = requests.post(ANYTHINGLLM_API_UPLOAD, headers=headers, files=files)
    if response.status_code == 200:
        print(f"✅ Uploaded: {filename}")
    else:
        print(f"❌ Failed to upload {filename} — {response.status_code}: {response.text}")
 
def update_embeddings(file_names):
    """Send the list of file names to update embeddings."""
    payload = {
        "adds": file_names,
        "deletes": []  # not deleting anything for now
    }
    try:
        response = requests.post(ANYTHINGLLM_API_UPDATE_EMBEDS, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"🔄 Embeddings updated for {len(file_names)} files.")
            print(f"🔄 Embeddings updated for {(file_names)} files.")
        else:
            print(f"❌ Failed to update embeddings — {response.status_code}: {response.text}")
    except Exception as e:
        print(f"⚠️ Error updating embeddings: {e}")
 
def main():
    # Step 1: Get existing docs before upload
    existing_titles, _ = get_existing_docs()
    print(f"📄 Existing documents: {len(existing_titles)} found.")
 
    # Step 2: Upload new files
    for filename in os.listdir(LOCAL_FOLDER):
        filepath = os.path.join(LOCAL_FOLDER, filename)
        if os.path.isfile(filepath):
            if filename in existing_titles:
                print(f"⏩ Skipping duplicate: {filename}")
            else:
                upload_file(filepath)
 
    # Step 3: Get updated doc list
    _, all_doc_names = get_existing_docs()
 
    # Step 4: Update embeddings for ALL docs
    update_embeddings(all_doc_names)
 
if __name__ == "__main__":
    main()