import { useEffect, useRef } from 'react';
import { Bot, User, LoaderCircle } from 'lucide-react';

export default function ChatWindow({ messages, isTyping }) {
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  return (
    <div className="glass-panel h-[70vh] overflow-hidden rounded-3xl shadow-soft">
      <div className="flex h-full flex-col">
        <div className="border-b border-slate-200 px-5 py-4">
          <p className="font-display text-xl font-bold">AI Property Assistant</p>
          <p className="text-sm text-muted">Ask about budgets, locations, and property recommendations.</p>
        </div>

        <div className="flex-1 space-y-4 overflow-y-auto px-5 py-6">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {message.role !== 'user' && (
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-primary text-white">
                  <Bot size={18} />
                </div>
              )}
              <div
                className={`max-w-[80%] rounded-3xl px-4 py-3 text-sm leading-6 shadow-sm ${
                  message.role === 'user'
                    ? 'bg-secondary text-white'
                    : 'bg-white text-secondary border border-slate-200'
                }`}
              >
                {message.content}
              </div>
              {message.role === 'user' && (
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-accent text-white">
                  <User size={18} />
                </div>
              )}
            </div>
          ))}

          {isTyping && (
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-primary text-white">
                <Bot size={18} />
              </div>
              <div className="rounded-3xl bg-white px-4 py-3 text-sm text-muted shadow-sm">
                <LoaderCircle size={16} className="mr-2 inline animate-spin" />
                Typing...
              </div>
            </div>
          )}
          <div ref={endRef} />
        </div>
      </div>
    </div>
  );
}