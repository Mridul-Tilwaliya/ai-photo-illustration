# Pickabook AI Illustration Prototype

This is an end-to-end prototype for the Pickabook technical assignment. It allows users to upload a photo (child or adult) and generates a personalized illustration using generative AI, maintaining the identity of the subject while applying a specific artistic style.

## 🏗️ Architecture

The application follows a decoupled client-server architecture:

- **Frontend**: [Next.js](https://nextjs.org/) (React) with [Tailwind CSS](https://tailwindcss.com/).
  - Chosen for its speed, SEO capabilities, and modern developer experience.
  - Handles image upload, preview, and result display.
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python).
  - Chosen for its high performance, native async support, and seamless integration with Python's AI ecosystem.
  - Acts as a proxy and orchestrator between the client and the AI inference engine.
- **AI Inference**: [Replicate API](https://replicate.com/) running **InstantID**.
  - Chosen for its state-of-the-art identity preservation capabilities without requiring heavy local GPU resources for this prototype.

### Architecture Diagram
```mermaid
graph LR
    User[User] -->|Uploads Photo| Client[Next.js Frontend]
    Client -->|POST /generate| Server[FastAPI Backend]
    Server -->|API Call + Image| Replicate[Replicate (InstantID)]
    Replicate -->|Generated Image URL| Server
    Server -->|JSON Response| Client
    Client -->|Displays Illustration| User
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- A [Replicate](https://replicate.com/) API Token

### 1. Backend Setup
Navigate to the `backend` directory:
```bash
cd backend
```

Create a virtual environment and install dependencies:
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Set up environment variables:
Create a `.env` file in the `backend` folder (copy from `.env.example`) and add your Replicate API token:
```
REPLICATE_API_TOKEN=r8_...
```

Run the server:
```bash
python main.py
# Server starts at http://localhost:8000
```

### 2. Frontend Setup
Navigate to the `frontend` directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Run the development server:
```bash
npm run dev
# App runs at http://localhost:3000
```

## 📝 Design Decisions & Notes

### Model Choice: InstantID
I chose **InstantID** (via Replicate) for this prototype because:
1.  **Identity Preservation**: It is currently one of the best methods for keeping facial features consistent ("It looks like me!") while changing the style completely.
2.  **Zero-shot**: It doesn't require training a LoRA for every new user, making it instant and scalable.
3.  **Stylization**: It pairs well with ControlNets to enforce the "illustration" style and pose from the reference template.

### Limitations Encountered
-   **Latency**: Using an external API (Replicate) introduces network latency and cold-start times for the model.
-   **Cost**: Per-generation cost on Replicate.
-   **Privacy**: Sending user photos to a third-party API.
-   **Template**: Currently uses a hardcoded or generic prompt/style. A production version would handle the "provided template" more robustly (e.g., extracting pose/depth maps from the template).

### Future Improvements (v2)
1.  **Local Inference**: Deploying the model on a dedicated GPU instance (e.g., AWS g5.xlarge) to reduce cost at scale and improve privacy.
2.  **Template Management**: A CMS to manage and select different story templates.
3.  **Face Quality**: Implementing a face restoration step (like CodeFormer) on the output for sharper eyes/features.
4.  **Queue System**: For high traffic, implementing a task queue (Celery/Redis) instead of holding the HTTP connection open.

---
*Built for Pickabook*
