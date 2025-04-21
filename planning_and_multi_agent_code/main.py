from fastapi import FastAPI
from apply_leave_crew import applyleave
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow requests from any origin with any method (you can customize as needed)
origins = ["*"]  # Allow requests from any origin
# Add CORS middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/applyleave/")
def verify_leave(query: str):
    res = {"Agent Response": applyleave(query).raw}
    return res

@app.route('/')
def hello_world():
    return "hello world"

# @app.get(
#     "/verifypass",
#     summary="Blog Generator (Multi-Agent Pattern)",
#     description="Uses a Multi-Agent workflow: Project manager delegates to research, writer, editor, and publisher agents to create a concise blog post."
# )
# def verify_passport(request: VerificationQuestion):
#     response = get_passport_details(request.question)
#     return {"final_blog": response.raw}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)