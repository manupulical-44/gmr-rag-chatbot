import useChat from '../hooks/useChat';
import ChatWindow from '../components/ChatWindow';
import ChatInput from '../components/ChatInput';

export default function ChatAssistantPage() {
  const { messages, input, setInput, isTyping, sendMessage, clearChat } = useChat();

  return (
    <div>
      <ChatWindow messages={messages} isTyping={isTyping} />
      <ChatInput
        value={input}
        onChange={(event) => setInput(event.target.value)}
        onSend={sendMessage}
        onClear={clearChat}
      />
    </div>
  );
}