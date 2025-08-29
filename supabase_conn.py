from supabase import create_client

# Replace with your Supabase project details
SUPABASE_URL = "https://gkfhogmpnblnzrargtjc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdrZmhvZ21wbmJsbnpyYXJndGpjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjM4OTc1MywiZXhwIjoyMDcxOTY1NzUzfQ.Vzl0PuEh94V6iP20-UVi9Gt4axnSa0g0mgMT-vjWJGk"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
# Fetch all users (should return empty initially)
response = supabase.table("users").select("*").execute()
print(response.data)
