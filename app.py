#!/usr/bin/env python3
from flask import Flask, request, jsonify, render_template_string
import chromadb
from ollama import Client
import time
import os

app = Flask(__name__, static_folder='static')

# Initialize ChromaDB
client_db = chromadb.PersistentClient(path="./chroma_db_education")
collection = client_db.get_or_create_collection("education_knowledge")

# Initialize Ollama
ollama_client = Client(host='http://localhost:11434')

# Quick responses
QUICK_RESPONSES = {
    'hi': 'Hello! Welcome to Africa Offline Education. Ask me about farming, digital skills, or anything!',
    'hello': 'Hello! Welcome to Africa Offline Education. Ask me about farming, digital skills, or anything!',
    'hey': 'Hi there! 👋 What would you like to learn about?',
    'thanks': 'You\'re welcome! Any other questions?',
    'thank you': 'You\'re welcome! Any other questions?',
    'help': 'I can help with: Agriculture & Farming, Digital Skills, and General Knowledge.',
    'bye': 'Goodbye! Keep learning! 👋',
}

def index_documents():
    """Index all documents in the documents folder"""
    print("📚 Indexing documents...")
    doc_folder = 'documents'
    
    if not os.path.exists(doc_folder):
        print("⚠️ No documents folder found")
        return
    
    all_chunks = []
    for file in os.listdir(doc_folder):
        if file.endswith('.txt'):
            filepath = os.path.join(doc_folder, file)
            with open(filepath, 'r') as f:
                content = f.read()
                # Split by double newlines
                chunks = content.split('\n\n')
                for chunk in chunks:
                    if chunk.strip():
                        all_chunks.append(chunk)
                print(f"   ✅ Indexed {file}: {len(chunks)} sections")
    
    if all_chunks:
        try:
            collection.add(
                documents=all_chunks,
                ids=[f"doc_{i}" for i in range(len(all_chunks))]
            )
            print(f"✅ Total: {len(all_chunks)} document sections indexed!\n")
        except Exception as e:
            print(f"⚠️ Indexing error: {e}\n")

def get_videos():
    """Get list of available videos"""
    video_folder = 'static/videos'
    videos = {}
    if os.path.exists(video_folder):
        for file in os.listdir(video_folder):
            if file.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                videos[file] = f'/static/videos/{file}'
    return videos

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🌍 Africa Offline Education</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
            min-height: 100vh;
        }
        .navbar {
            background: linear-gradient(135deg, #1a472a 0%, #2d5a3d 100%);
            color: white;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .navbar h1 { font-size: 28px; margin-bottom: 5px; }
        .navbar p { font-size: 14px; opacity: 0.9; }
        
        .container { max-width: 800px; margin: 20px auto; padding: 0 20px; }
        
        .menu-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
            margin-top: 20px;
        }
        
        .menu-btn {
            padding: 20px;
            background: white;
            border: 3px solid #1a472a;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            color: #1a472a;
            transition: all 0.3s;
        }
        
        .menu-btn:hover {
            background: #1a472a;
            color: white;
            transform: translateY(-3px);
        }
        
        .chat-container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.2);
            display: none;
            flex-direction: column;
            height: 80vh;
        }
        .chat-container.active { display: flex; }
        
        .videos-container {
            display: none;
        }
        .videos-container.active { display: block; }
        
        .header {
            background: linear-gradient(135deg, #1a472a 0%, #2d5a3d 100%);
            color: white;
            padding: 20px;
            border-radius: 10px 10px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header h1 { font-size: 20px; }
        
        .back-btn {
            background: #FF6B35;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }
        .back-btn:hover { background: #F7931E; }
        
        .chat-box {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f9f9f9;
        }
        
        .message {
            margin-bottom: 15px;
            display: flex;
            gap: 10px;
        }
        .message.user { justify-content: flex-end; }
        .message.bot { justify-content: flex-start; }
        
        .message-text {
            max-width: 80%;
            padding: 12px;
            border-radius: 8px;
            word-wrap: break-word;
            font-size: 14px;
            line-height: 1.5;
        }
        .message.user .message-text {
            background: #FF6B35;
            color: white;
            border-radius: 8px 0 8px 8px;
        }
        .message.bot .message-text {
            background: #e0e0e0;
            color: #333;
            border-radius: 0 8px 8px 8px;
        }
        
        .timer {
            font-size: 11px;
            color: #999;
            margin-top: 5px;
            text-align: right;
        }
        
        .input-area {
            padding: 20px;
            border-top: 1px solid #ddd;
            display: flex;
            gap: 10px;
        }
        
        input {
            flex: 1;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
        }
        input:focus { outline: none; border-color: #FF6B35; }
        
        button {
            padding: 12px 20px;
            background: #FF6B35;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover { background: #F7931E; }
        
        .loading { 
            display: none;
            text-align: center;
            padding: 10px;
            color: #999;
        }
        
        .video-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
            margin-top: 20px;
        }
        
        .video-card {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        
        .video-card video {
            width: 100%;
            height: 300px;
            background: #000;
        }
        
        .video-title {
            padding: 15px;
            font-weight: bold;
            color: #1a472a;
            background: #f9f9f9;
        }
        
        .no-videos {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>🌍 Africa Offline Education</h1>
        <p>Learn without internet - Knowledge for African students & farmers</p>
    </div>

    <!-- Main Menu -->
    <div id="menu-section" class="container">
        <div class="menu-grid">
            <button class="menu-btn" onclick="showChat('agriculture')">
                🌾 Agriculture & Farming
            </button>
            <button class="menu-btn" onclick="showChat('digital')">
                📱 Digital Skills
            </button>
            <button class="menu-btn" onclick="showChat('general')">
                📚 General Knowledge
            </button>
            <button class="menu-btn" onclick="showVideos()">
                🎥 Watch Videos
            </button>
        </div>
    </div>

    <!-- Chat Section -->
    <div id="chat-section" class="chat-container">
        <div class="header">
            <h1 id="topic-title">Topic</h1>
            <button class="back-btn" onclick="backToMenu()">← Back</button>
        </div>
        <div class="chat-box" id="chatBox"></div>
        <div class="loading" id="loading">Thinking...</div>
        <div class="input-area">
            <input type="text" id="userInput" placeholder="Ask your question..." />
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <!-- Videos Section -->
    <div id="videos-section" class="videos-container">
        <div class="container">
            <button class="back-btn" onclick="backToMenu()" style="margin-bottom: 20px;">← Back to Menu</button>
            <h2>🎥 Educational Videos</h2>
            <div class="video-grid" id="videoGrid"></div>
        </div>
    </div>

    <script>
        let currentTopic = 'general';
        
        const topics = {
            agriculture: '🌾 Agriculture & Farming',
            digital: '📱 Digital Skills',
            general: '📚 General Knowledge'
        };
        
        function showChat(topic) {
            currentTopic = topic;
            document.getElementById('menu-section').style.display = 'none';
            document.getElementById('chat-section').classList.add('active');
            document.getElementById('videos-section').classList.remove('active');
            document.getElementById('topic-title').textContent = topics[topic];
            document.getElementById('chatBox').innerHTML = '';
            
            const welcomeMessages = {
                agriculture: 'Welcome to Agriculture! 🌾 Ask about maize farming, soil, irrigation, pests, fertilizer, etc.',
                digital: 'Welcome to Digital Skills! 📱 Ask about mobile money, internet safety, social media, etc.',
                general: 'Welcome to Learning! 📚 Ask anything you want to learn!'
            };
            
            addMessage(welcomeMessages[topic], 'bot');
        }
        
        function showVideos() {
            document.getElementById('menu-section').style.display = 'none';
            document.getElementById('chat-section').classList.remove('active');
            document.getElementById('videos-section').classList.add('active');
            
            fetch('/get-videos')
                .then(r => r.json())
                .then(data => {
                    const videos = data.videos;
                    let html = '';
                    
                    if (Object.keys(videos).length === 0) {
                        html = '<div class="no-videos">No videos available yet.</div>';
                    } else {
                        Object.entries(videos).forEach(([filename, filepath]) => {
                            html += `
                                <div class="video-card">
                                    <video controls>
                                        <source src="${filepath}" type="video/mp4">
                                    </video>
                                    <div class="video-title">🎥 ${filename.replace(/\.[^/.]+$/, '').replace(/_/g, ' ')}</div>
                                </div>
                            `;
                        });
                    }
                    
                    document.getElementById('videoGrid').innerHTML = html;
                });
        }
        
        function backToMenu() {
            document.getElementById('menu-section').style.display = 'block';
            document.getElementById('chat-section').classList.remove('active');
            document.getElementById('videos-section').classList.remove('active');
            document.getElementById('chatBox').innerHTML = '';
        }
        
        function sendMessage() {
            const input = document.getElementById('userInput').value.trim().toLowerCase();
            if (!input) return;
            
            addMessage(input, 'user');
            document.getElementById('userInput').value = '';
            document.getElementById('loading').style.display = 'block';
            
            const startTime = Date.now();
            
            fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    question: input,
                    topic: currentTopic
                })
            })
            .then(r => r.json())
            .then(data => {
                document.getElementById('loading').style.display = 'none';
                const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
                addMessage(data.answer, 'bot', elapsed);
            })
            .catch(e => {
                document.getElementById('loading').style.display = 'none';
                addMessage('Error: ' + e, 'bot');
            });
        }
        
        function addMessage(text, sender, responseTime) {
            const chatBox = document.getElementById('chatBox');
            const msgDiv = document.createElement('div');
            msgDiv.className = 'message ' + sender;
            
            let html = '<div class="message-text">' + text + '</div>';
            if (responseTime) {
                html += '<div class="timer">⏱️ ' + responseTime + 's</div>';
            }
            
            msgDiv.innerHTML = html;
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/get-videos')
def get_videos_list():
    videos = get_videos()
    return jsonify({'videos': videos})

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '').lower().strip()
    topic = data.get('topic', 'general')
    
    if not question:
        return jsonify({'answer': 'Please ask a question.'})
    
    # Check quick responses first
    for key, response in QUICK_RESPONSES.items():
        if key in question:
            return jsonify({'answer': response})
    
    try:
        start_time = time.time()
        
        # Search indexed documents
        results = collection.query(
            query_texts=[question],
            n_results=5
        )
        
        context = ""
        if results and results['documents'] and results['documents'][0]:
            context = "\n\n".join(results['documents'][0][:3])
        
        topic_context = {
            'agriculture': 'You are an expert agricultural advisor. Use the provided farming information to answer.',
            'digital': 'You are a digital skills trainer. Use the provided digital information to answer.',
            'general': 'You are an educational assistant. Use the provided information to answer.',
        }
        
        prompt = f"""{topic_context.get(topic, topic_context['general'])}

REFERENCE INFORMATION:
{context}

QUESTION: {question}

ANSWER: Provide a clear, practical answer based on the information above. If you have specific data, use it."""
        
        response = ollama_client.generate(
            model='qwen2.5:1.5b',
            prompt=prompt,
            stream=False
        )
        
        answer = response['response'].strip()
        elapsed_time = time.time() - start_time
        
        return jsonify({'answer': answer, 'time': f"{elapsed_time:.2f}"})
    
    except Exception as e:
        return jsonify({'answer': f'Error: {str(e)}'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌍 AFRICA OFFLINE EDUCATION")
    print("="*60)
    
    # Index documents
    index_documents()
    
    print("✅ Starting server...")
    print("🌐 Open: http://10.42.0.1:5000")
    print("📱 Connected to: BankingLLM WiFi\n")
    print("🎥 Available Videos:")
    for name, path in get_videos().items():
        print(f"   - {name}")
    print("\nPress Ctrl+C to stop\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
