import StickyNote from '../components/StickyNote';

/**
 * PlaceholderPage
 * -----------------------------------------------------------------------
 * Drop-in stub for a route that hasn't been built yet. Renders inside
 * AppShell's <Outlet/> like any real page, so Header/ChatPanel context
 * is visible during review even before the real screen exists.
 *
 * Usage — this is the whole file a page needs until someone builds it:
 *
 *   export default function AdvisorDashboardPage() {
 *     return <PlaceholderPage title="Advisor Dashboard" owner="@teammate" />;
 *   }
 */
type PlaceholderPageProps = {
  title: string;
  owner?: string;
  note?: string;
};

export default function PlaceholderPage({ title, owner, note }: PlaceholderPageProps) {
  return (
    <div className="flex min-h-full items-center justify-center p-10">
      <div className="flex flex-col items-center gap-4 text-center">
        <h1 className="font-heading text-3xl text-notebook-ink">{title}</h1>
        <p className="font-body text-neutral-500">Not built yet.</p>
        {(owner || note) && (
          <StickyNote rotation={-3} className="mt-2">
            {owner && <div className="font-heading text-sm">Owner: {owner}</div>}
            {note && <div className="mt-1 font-body text-sm">{note}</div>}
          </StickyNote>
        )}
      </div>
    </div>
  );
}