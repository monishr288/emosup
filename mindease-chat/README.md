## MindEase – AI Emotional Support Chat Application

MindEase is a React-based AI emotional support chat application designed to provide a safe, calm, and empathetic space for users to express their feelings. It uses an AI model to respond in a warm and supportive tone, helping reduce loneliness while clearly avoiding medical or crisis counseling.

### 🧠 Project Objective

#### The main goal of MindEase is to:

* Reduce feelings of loneliness

* Provide emotional support through empathetic AI conversations

* Offer a friendly, non-judgmental chat experience

* Maintain ethical boundaries by avoiding medical advice

### ✨ Features

💬 AI Chat Companion with empathetic responses

🎤 Voice Message Recording & Playback

📎 File Attachment Support

🌗 Light / Dark Theme Toggle (saved using LocalStorage)

💾 Chat History Persistence

🧠 Custom AI System Prompt for emotional safety

🎨 Modern 3D UI with Animations & Floating Effects

📱 Responsive Design (works on mobile & desktop)

### 🛠️ Tech Stack

* Frontend: React.js (Vite)

* Styling: Advanced CSS (3D effects, animations, themes)

* AI API: Google Gemini API

* HTTP Client: Axios

* Storage: Browser LocalStorage

* Audio: MediaRecorder Web API

### 📂 Project Structure
```
mindease/
├── src/
│   ├── components/
│   │   └── Chat.jsx
│   ├── App.jsx
│   ├── main.jsx
│   └── style.css
├── index.html
├── package.json
└── README.md
```

### 🚀 How to Run the Project Locally

Clone the repository

git clone https://github.com/monishr288/emosup


#### Navigate to the project folder

cd mindease


#### Install dependencies

npm install


#### Add Gemini API Key
Create a .env file in the root folder:

VITE_GEMINI_API_KEY=your_api_key_here


#### Run the development server

npm run dev


#### Open in browser:

http://localhost:5173

🔐 Ethical Disclaimer

* MindEase is intended only for emotional support.



### Screenshots of:

#### Chat interface


### Welcome screen
<img width="1899" height="863" alt="image" src="https://github.com/user-attachments/assets/750c74bf-808b-487d-b198-a75b3bf08b21" />
<img width="1893" height="855" alt="image" src="https://github.com/user-attachments/assets/5a5d0dbb-e61b-47a4-9569-38e8d54bc038" />

###  Light & Dark mode

<img width="1876" height="909" alt="image" src="https://github.com/user-attachments/assets/d9ddee2b-b48e-4444-9740-92925e24c592" />
<img width="1877" height="913" alt="image" src="https://github.com/user-attachments/assets/9f57065f-258e-4f91-b2ee-948523137b40" />





⭐ Acknowledgements

Google Gemini API

React.js Community

Open Web APIs# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
