import { SendHorizonal, Trash2 } from 'lucide-react';

export default function ChatInput({ value, onChange, onSend, onClear }) {
  return (
    <div className="glass-panel mt-5 rounded-3xl p-4 shadow-soft">
      <div className="flex flex-col gap-3 sm:flex-row">
        <textarea
          value={value}
          onChange={onChange}
          rows={3}
          placeholder="Ask about 3 BHK homes in Bangalore under 1 crore..."
          className="min-h-[92px] flex-1 rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none placeholder:text-slate-400"
        />
        <div className="flex gap-3 sm:flex-col">
          <button
            onClick={onSend}
            className="inline-flex items-center justify-center gap-2 rounded-2xl bg-primary px-5 py-3 font-semibold text-white transition hover:bg-blue-700"
          >
            <SendHorizonal size={16} />
            Send
          </button>
          <button
            onClick={onClear}
            className="inline-flex items-center justify-center gap-2 rounded-2xl bg-slate-100 px-5 py-3 font-semibold text-secondary transition hover:bg-slate-200"
          >
            <Trash2 size={16} />
            Clear chat
          </button>
        </div>
      </div>
    </div>
  );
}