import { useState, useRef, useEffect, type FormEvent } from 'react';
import arrow from "../assets/Arrow 1.svg";

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

/**
 * ChatPanel
 * -----------------------------------------------------------------------
 * Persistent, self-contained chat sidebar for the App Shell.
 *
 * Usage — mount once at the shell level, as a sibling of <Outlet/>, so it
 * survives route changes and keeps its own state (input text, message
 * history, scroll position):
 *
 *   <div className="flex h-screen">
 *     <Sidebar />
 *     <main className="min-w-0 flex-1 overflow-y-auto"><Outlet /></main>
 *     <ChatPanel />
 *   </div>
 *
 * Do NOT mount this inside a route element — it must live above the
 * <Outlet/> in the tree so React never unmounts it on navigation.
 *
 * Responsive behavior:
 *  - md and up: static flex column, fixed width, docked to the right.
 *  - below md: collapses into a slide-out drawer, opened via a floating
 *    action button. No absolute positioning is used for layout — only
 *    `fixed` for the mobile overlay itself, which is the standard,
 *    accessible pattern for slide-out drawers.
 */

type ChatMessage = {
  id: string;
  role: 'user' | 'assistant';
  text: string;
};

const WIDTH_CLASS = 'w-full sm:w-[373px]';

export default function ChatPanel() {
  const [isOpen, setIsOpen] = useState(false); // mobile/tablet drawer state
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Keep the view pinned to the latest message, mirroring native chat UX.
  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight });
  }, [messages]);

  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;

    setMessages((prev) => [...prev, { id: crypto.randomUUID(), role: 'user', text: trimmed }]);
    setInput('');
    // Wire up your assistant call here, then append the response with
    // role: 'assistant'.
  }

  return (
    <>
      {/* Mobile floating action button — opens the drawer. Hidden once open
          and hidden entirely at md+ where the panel is always visible. */}
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

      {/* Backdrop for the mobile drawer */}
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
          // Desktop: normal flex sibling, always in flow.
          'md:static md:h-full md:border-l md:border-[#D7D7D7]',
          // Mobile/tablet: fixed slide-out drawer.
          'fixed inset-y-0 right-0 z-50 h-full transition-transform duration-300 ease-out md:transition-none',
          isOpen ? 'translate-x-0' : 'translate-x-full md:translate-x-0',
        ].join(' ')}
      >
        {/* Header */}
        <div className="flex h-14 shrink-0 items-center justify-between px-4">
          <button
            type="button"
            aria-label={isOpen ? 'Close chat' : 'Chat menu'}
            onClick={() => setIsOpen(false)}
            className="flex h-8 w-8 items-center justify-center rounded-md text-neutral-700 hover:bg-black/5 md:hidden"
          >
            <CloseIcon className="h-5 w-5" />
          </button>
          <button
            type="button"
            aria-label="Chat menu"
            className="hidden h-8 w-8 items-center justify-center rounded-md text-neutral-700 hover:bg-black/5 md:flex"
          >
            <MenuIcon className="h-5 w-5" />
          </button>
        </div>

        {/* Message history */}
        <div ref={scrollRef} className="flex-1 overflow-y-auto px-4">
          {messages.length === 0 ? (
            <div className="flex h-full items-center justify-center px-6 text-center">
              <p className="font-heading text-lg text-neutral-400">
                What would you like to know?
              </p>
            </div>
          ) : (
            <ul className="flex flex-col gap-3 py-4">
              {messages.map((m) => (
                <li
                  key={m.id}
                  className={[
                    'max-w-[85%] rounded-2xl px-4 py-2.5 text-[15px] leading-snug',
                    m.role === 'user'
                      ? 'ml-auto bg-notebook-ink text-white'
                      : 'mr-auto bg-white text-notebook-ink',
                  ].join(' ')}
                >
                  {m.text}
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Input dock — just the prompt and a send button */}
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
              placeholder="What would you like to know?"
              className="max-h-32 flex-1 resize-none bg-transparent font-body text-[15px] text-notebook-ink placeholder:text-neutral-400 focus:outline-none"
            />

            <button
              type="submit"
              disabled={!input.trim()}
              aria-label="Send message"
              className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-neutral-200 transition-colors disabled:opacity-60 enabled:hover:bg-notebook-ink/10"
            >
              <img src={arrow} alt="" className="h-4 w-4 -rotate-90 select-none" />
            </button>
          </div>
        </form>
      </aside>
    </>
  );
}