import { useState, useRef, useEffect, type FormEvent } from 'react';
import arrow from '../assets/Arrow 1.svg';
import { chatWithAgent } from '../services/Agent';

/** Minimal inline icons — no icon package dependency. These are plain UI
 * chrome (not Figma doodles), so they're written directly as SVG rather
 * than pulled in as an asset. */
function MenuIcon({ className = '' }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" className={className}>
      <line x1="4" y1="7" x2="20" y2="7" />
      <line x1="4" y1="12" x2="20" y2="12" />
      <line x1="4" y1="17" x2="20" y2="17" />
    </svg>
  );
}

function CloseIcon({ className = '' }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" className={className}>
      <line x1="6" y1="6" x2="18" y2="18" />
      <line x1="18" y1="6" x2="6" y2="18" />
    </svg>
  );
}

function SearchIcon({ className = '' }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" className={className}>
      <circle cx="11" cy="11" r="7" />
      <line x1="21" y1="21" x2="16.65" y2="16.65" />
    </svg>
  );
}

function PlusIcon({ className = '' }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" className={className}>
      <line x1="12" y1="5" x2="12" y2="19" />
      <line x1="5" y1="12" x2="19" y2="12" />
    </svg>
  );
}

/**
 * ChatPanel
 * -----------------------------------------------------------------------
 * Persistent, self-contained chat sidebar for the App Shell.
 */

type ChatMessage = {
  id: string;
  role: 'user' | 'assistant';
  text: string;
};

type ChatSession = {
  id: string;
  title: string;
  messages: ChatMessage[];
};

function createSession(): ChatSession {
  return { id: crypto.randomUUID(), title: 'New chat', messages: [] };
}

const WIDTH_CLASS = 'w-full sm:w-[373px]';

export default function ChatPanel() {
  const [isOpen, setIsOpen] = useState(false); // mobile/tablet drawer state
  const [view, setView] = useState<'chat' | 'history'>('chat');
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false); // loading state for API
  const [historySearch, setHistorySearch] = useState('');
  const [sessions, setSessions] = useState<ChatSession[]>(() => [createSession()]);
  const [activeSessionId, setActiveSessionId] = useState(() => sessions[0].id);
  const scrollRef = useRef<HTMLDivElement>(null);

  const activeSession = sessions.find((s) => s.id === activeSessionId) ?? sessions[0];

  useEffect(() => {
    if (!sessions.some((s) => s.id === activeSessionId)) {
      setActiveSessionId(sessions[0]?.id ?? '');
    }
  }, [sessions, activeSessionId]);

  // Keep the view pinned to the latest message, or when typing indicator appears
  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight });
  }, [activeSession?.messages, isTyping]);

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;

    // 1. Add user message to the active session immediately
    setSessions((prev) =>
      prev.map((s) =>
        s.id === activeSessionId
          ? {
              ...s,
              title: s.messages.length === 0 ? trimmed.slice(0, 40) : s.title,
              messages: [...s.messages, { id: crypto.randomUUID(), role: 'user', text: trimmed }],
            }
          : s,
      ),
    );
    
    setInput('');
    setIsTyping(true);

    try {
      const data = await chatWithAgent(trimmed);

      // 3. Append the assistant's response to the active session
      setSessions((prev) =>
        prev.map((s) =>
          s.id === activeSessionId
            ? {
                ...s,
                messages: [
                  ...s.messages,
                  {
                    id: crypto.randomUUID(),
                    role: 'assistant',
                    text: data.reply || "I've received your request.",
                  },
                ],
              }
            : s,
        ),
      );

      setIsTyping(false);
    } catch (error) {
      console.warn("Backend unreachable.", error);
      setSessions((prev) =>
        prev.map((s) =>
          s.id === activeSessionId
            ? {
                ...s,
                messages: [
                  ...s.messages,
                  {
                    id: crypto.randomUUID(),
                    role: 'assistant',
                    text: 'The planner is unreachable. Try again when the API is running.',
                  },
                ],
              }
            : s,
        ),
      );
      setIsTyping(false);
    }
  }

  function startNewChat() {
    const fresh = createSession();
    setSessions((prev) => [fresh, ...prev]);
    setActiveSessionId(fresh.id);
    setView('chat');
  }

  function selectSession(id: string) {
    setActiveSessionId(id);
    setView('chat');
  }

  function deleteSession(id: string, e: React.MouseEvent) {
    e.stopPropagation();
    setSessions((prev) => {
      const next = prev.filter((s) => s.id !== id);
      return next.length > 0 ? next : [createSession()];
    });
  }

  const filteredSessions = sessions.filter((s) =>
    s.title.toLowerCase().includes(historySearch.trim().toLowerCase()),
  );

  return (
    <>
      {!isOpen && (
        <button
          type="button"
          onClick={() => setIsOpen(true)}
          aria-label="Open chat"
          className="fixed bottom-6 right-6 z-40 flex h-14 w-14 items-center justify-center rounded-full bg-notebook-ink text-white shadow-lg md:hidden"
        >
          <MenuIcon className="h-6 w-6" />
        </button>
      )}

      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/30 md:hidden"
          onClick={() => setIsOpen(false)}
          aria-hidden="true"
        />
      )}

      <aside
        aria-label="Chat panel"
        className={[
          WIDTH_CLASS,
          'flex shrink-0 flex-col bg-[#F2F2F2] font-body',
          'md:static md:h-full md:border-l md:border-[#D7D7D7]',
          'fixed inset-y-0 right-0 z-50 h-full transition-transform duration-300 ease-out md:transition-none',
          isOpen ? 'translate-x-0' : 'translate-x-full md:translate-x-0',
        ].join(' ')}
      >
        <div className="flex h-14 shrink-0 items-center justify-between px-4">
          <button
            type="button"
            aria-label={view === 'history' ? 'Back to chat' : 'Chat history'}
            onClick={() => setView((v) => (v === 'history' ? 'chat' : 'history'))}
            className="flex h-8 w-8 items-center justify-center rounded-md text-neutral-700 hover:bg-black/5"
          >
            <MenuIcon className="h-5 w-5" />
          </button>

          <button
            type="button"
            aria-label="Close chat"
            onClick={() => setIsOpen(false)}
            className="flex h-8 w-8 items-center justify-center rounded-md text-neutral-700 hover:bg-black/5 md:hidden"
          >
            <CloseIcon className="h-5 w-5" />
          </button>
        </div>

        {view === 'history' ? (
          <div className="flex flex-1 flex-col overflow-hidden">
            <div className="px-4 pb-2">
              <div className="flex items-center gap-2 rounded-full bg-white px-3 py-2 ring-1 ring-black/5">
                <SearchIcon className="h-4 w-4 shrink-0 text-neutral-400" />
                <label htmlFor="chat-history-search" className="sr-only">
                  Search chats
                </label>
                <input
                  id="chat-history-search"
                  type="search"
                  value={historySearch}
                  onChange={(e) => setHistorySearch(e.target.value)}
                  placeholder="Search chats"
                  className="w-full bg-transparent font-body text-sm text-notebook-ink placeholder:text-neutral-400 focus:outline-none"
                />
              </div>
            </div>

            <button
              type="button"
              onClick={startNewChat}
              className="mx-4 mb-2 flex items-center justify-center gap-2 rounded-full bg-notebook-ink px-4 py-2 font-body text-sm text-white hover:opacity-90"
            >
              <PlusIcon className="h-4 w-4" />
              New chat
            </button>

            <ul className="flex-1 overflow-y-auto px-2 pb-4">
              {filteredSessions.map((session) => (
                <li key={session.id}>
                  <button
                    type="button"
                    onClick={() => selectSession(session.id)}
                    className={[
                      'group flex w-full items-center justify-between gap-2 rounded-lg px-3 py-2.5 text-left font-body text-sm',
                      session.id === activeSessionId ? 'bg-white' : 'hover:bg-black/5',
                    ].join(' ')}
                  >
                    <span className="truncate text-notebook-ink">{session.title}</span>
                    <span
                      role="button"
                      tabIndex={0}
                      onClick={(e) => deleteSession(session.id, e)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter' || e.key === ' ') deleteSession(session.id, e as unknown as React.MouseEvent);
                      }}
                      aria-label={`Delete ${session.title}`}
                      className="shrink-0 rounded p-1 text-neutral-400 opacity-0 hover:text-red-500 group-hover:opacity-100"
                    >
                      <CloseIcon className="h-3.5 w-3.5" />
                    </span>
                  </button>
                </li>
              ))}
              {filteredSessions.length === 0 && (
                <li className="px-3 py-6 text-center font-body text-sm text-neutral-400">
                  No chats found.
                </li>
              )}
            </ul>
          </div>
        ) : (
          <>
            <div ref={scrollRef} className="flex-1 overflow-y-auto px-4">
              {activeSession.messages.length === 0 ? (
                <div className="flex h-full items-center justify-center px-6 text-center">
                  <p className="font-heading text-lg text-neutral-400">
                    What would you like to know?
                  </p>
                </div>
              ) : (
                <ul className="flex flex-col gap-3 py-4">
                  {activeSession.messages.map((m) => (
                    <li
                      key={m.id}
                      className={[
                        'max-w-[85%] rounded-2xl px-4 py-2.5 text-[15px] leading-snug whitespace-pre-wrap',
                        m.role === 'user'
                          ? 'ml-auto bg-notebook-ink text-white'
                          : 'mr-auto bg-white text-notebook-ink',
                      ].join(' ')}
                    >
                      {m.text}
                    </li>
                  ))}
                  
                  {isTyping && (
                    <li className="mr-auto max-w-[85%] rounded-2xl bg-white px-4 py-2.5 text-[15px] leading-snug text-neutral-400 italic">
                      Typing...
                    </li>
                  )}
                </ul>
              )}
            </div>

            <form onSubmit={handleSubmit} className="shrink-0 p-3">
              <div className="flex items-end gap-2 rounded-2xl bg-white p-3 shadow-sm ring-1 ring-black/5">
                <label htmlFor="chat-panel-input" className="sr-only">
                  What would you like to know?
                </label>
                <textarea
                  id="chat-panel-input"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      e.currentTarget.form?.requestSubmit();
                    }
                  }}
                  rows={1}
                  disabled={isTyping}
                  placeholder={isTyping ? "Agent is typing..." : "What would you like to know?"}
                  className="max-h-32 flex-1 resize-none bg-transparent font-body text-[15px] text-notebook-ink placeholder:text-neutral-400 focus:outline-none disabled:opacity-50"
                />

                <button
                  type="submit"
                  disabled={!input.trim() || isTyping}
                  aria-label="Send message"
                  className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-neutral-200 transition-colors disabled:opacity-60 enabled:hover:bg-notebook-ink/10"
                >
                  <img src={arrow} alt="" className="h-4 w-4 -rotate-90 select-none" />
                </button>
              </div>
            </form>
          </>
        )}
      </aside>
    </>
  );
}