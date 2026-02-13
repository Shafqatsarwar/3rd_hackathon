"use client";

import { useState, useRef, useEffect } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
  agent?: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState<"checking" | "online" | "offline">("checking");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Check backend health
    const checkBackend = async () => {
      try {
        const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";
        const response = await fetch(`${backendUrl}/health`);
        if (response.ok) {
          setBackendStatus("online");
        } else {
          setBackendStatus("offline");
        }
      } catch {
        setBackendStatus("offline");
      }
    };
    checkBackend();
  }, []);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";
      const response = await fetch(`${backendUrl}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input, context: messages }),
      });

      if (!response.ok) throw new Error("Failed to get response");

      const data = await response.json();
      const assistantMessage: Message = {
        role: "assistant",
        content: data.response,
        agent: data.agent,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Chat error:", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, I'm having trouble connecting to the server. Please ensure the backend is running.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white overflow-hidden relative selection:bg-purple-500 selection:text-white">

      {/* Animated Background Mesh */}
      <div className="absolute inset-0 z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-purple-600/30 blur-[120px] animate-pulse-glow" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-blue-600/20 blur-[120px] animate-pulse-glow" style={{ animationDelay: "1s" }} />
        <div className="absolute top-[20%] right-[10%] w-[30%] h-[30%] rounded-full bg-pink-600/20 blur-[100px] animate-float" />
      </div>

      {/* Header */}
      <header className="relative z-50 border-b border-white/5 backdrop-blur-md bg-slate-900/50">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center shadow-lg shadow-purple-500/30">
              <span className="text-white font-bold text-xl">L</span>
            </div>
            <div>
              <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-white/70">LearnFlow</h1>
              <p className="text-xs text-purple-400 font-medium tracking-wide">AI PYTHON TUTOR</p>
            </div>
          </div>
          <div className="flex items-center gap-3 bg-white/5 px-4 py-2 rounded-full border border-white/5 backdrop-blur-sm">
            <span
              className={`w-2.5 h-2.5 rounded-full shadow-[0_0_10px_currentColor] ${backendStatus === "online"
                ? "bg-emerald-400 text-emerald-400"
                : backendStatus === "checking"
                  ? "bg-amber-400 text-amber-400"
                  : "bg-rose-500 text-rose-500"
                }`}
            />
            <span className="text-xs font-medium text-white/70 uppercase tracking-wider">
              {backendStatus === "online" ? "System Online" : backendStatus === "checking" ? "Connecting..." : "Offline"}
            </span>
          </div>
        </div>
      </header>

      <main className="relative z-10 max-w-5xl mx-auto px-4 py-8 flex flex-col min-h-[calc(100vh-80px)]">

        {/* Welcome Hero - Only show when no messages */}
        {messages.length === 0 && (
          <div className="flex-1 flex flex-col items-center justify-center animate-fade-in mb-10">
            <div className="relative mb-8">
              <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 blur-[60px] opacity-20" />
              <h2 className="relative text-5xl md:text-7xl font-bold text-center leading-tight tracking-tight">
                Master Python with
                <span className="block mt-2 bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent animate-gradient-x">
                  Intelligent Agents
                </span>
              </h2>
            </div>

            <p className="text-lg text-slate-400 max-w-2xl mx-auto text-center mb-12 leading-relaxed">
              Experience the future of coding education. Our specialized AI agents collaborate to help you learn, debug, and build faster than ever.
            </p>

            {/* Agent Grid */}
            <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 w-full max-w-4xl">
              {[
                { name: "Concepts", desc: "Master fundamentals", icon: "📚", gradient: "from-blue-500 to-cyan-400" },
                { name: "Debug", desc: "Fix complex errors", icon: "🔧", gradient: "from-orange-500 to-amber-400" },
                { name: "Exercise", desc: "Hands-on practice", icon: "🚀", gradient: "from-emerald-500 to-teal-400" },
                { name: "Progress", desc: "Track milestones", icon: "📈", gradient: "from-violet-500 to-purple-400" },
                { name: "Review", desc: "Code quality check", icon: "✨", gradient: "from-pink-500 to-rose-400" },
                { name: "Triage", desc: "Get directed help", icon: "🎯", gradient: "from-indigo-500 to-blue-500" },
              ].map((agent, i) => (
                <button
                  key={agent.name}
                  onClick={() => setInput(`Help me with ${agent.name.toLowerCase()}`)}
                  className="group relative overflow-hidden rounded-2xl glass-card p-6 text-left transition-all duration-300 hover:scale-[1.02] hover:-translate-y-1 hover:shadow-2xl hover:shadow-purple-500/10 border-white/5 hover:border-white/10"
                  style={{ animationDelay: `${i * 100}ms` }}
                >
                  <div className={`absolute top-0 right-0 w-24 h-24 bg-gradient-to-br ${agent.gradient} opacity-5 blur-2xl group-hover:opacity-20 transition-opacity`} />

                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${agent.gradient} mb-4 flex items-center justify-center text-2xl shadow-lg group-hover:scale-110 transition-transform`}>
                    {agent.icon}
                  </div>
                  <h3 className="text-lg font-bold text-white mb-1 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-white/70 transition-colors">
                    {agent.name}
                  </h3>
                  <p className="text-sm text-slate-400 group-hover:text-slate-300 transition-colors">
                    {agent.desc}
                  </p>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Chat Area */}
        <div className={`flex-1 overflow-y-auto mb-6 space-y-6 pr-2 scrollbar-thin ${messages.length > 0 ? 'min-h-[400px]' : ''}`}>
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[85%] lg:max-w-[70%] p-6 rounded-3xl relative shadow-lg ${message.role === "user"
                  ? "bg-gradient-to-br from-indigo-600 to-purple-600 text-white rounded-tr-md"
                  : "glass-card text-slate-200 rounded-tl-md border-white/10"
                  }`}
              >
                {message.agent && (
                  <div className="absolute -top-3 left-4 px-3 py-1 bg-slate-900 rounded-full border border-purple-500/30 shadow-lg shadow-purple-900/20 flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-purple-400 animate-pulse" />
                    <span className="text-[10px] font-bold tracking-wider text-purple-300 uppercase">
                      {message.agent.replace("-", " ")}
                    </span>
                  </div>
                )}
                <div className="prose prose-invert prose-sm max-w-none">
                  <p className="whitespace-pre-wrap leading-relaxed">{message.content}</p>
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="glass-card px-6 py-4 rounded-3xl rounded-tl-md border-white/10 flex items-center gap-3 shadow-lg">
                <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                <div className="w-2 h-2 bg-pink-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="relative z-50 mt-auto">
          <form onSubmit={sendMessage} className="relative group">
            <div className="absolute -inset-0.5 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-2xl opacity-30 group-hover:opacity-100 blur transition duration-1000 group-hover:duration-200" />

            <div className="relative flex items-center bg-slate-900 rounded-2xl p-1.5 ring-1 ring-white/10">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about Python concepts, debug code, or request exercises..."
                disabled={isLoading || backendStatus !== "online"}
                className="flex-1 bg-transparent px-6 py-4 text-white placeholder-slate-500 focus:outline-none disabled:opacity-50"
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim() || backendStatus !== "online"}
                className="px-6 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-medium hover:from-indigo-500 hover:to-purple-500 transition-all shadow-lg hover:shadow-purple-500/25 disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none min-w-[100px]"
              >
                {isLoading ? (
                  <span className="flex items-center justify-center gap-2">
                    <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                  </span>
                ) : (
                  "Send 🚀"
                )}
              </button>
            </div>
            {backendStatus === "offline" && (
              <div className="absolute -bottom-8 left-0 right-0 text-center animate-fade-in">
                <span className="bg-red-500/10 text-red-400 text-xs px-3 py-1 rounded-full border border-red-500/20">
                  ⚠️ Backend disconnected. Start local server.
                </span>
              </div>
            )}
          </form>
        </div>

      </main>

      <style jsx global>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
          animation: fade-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
      `}</style>
    </div>
  );
}
