export default function LoadingSkeleton({ count = 6 }) {
  return (
    <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
      {Array.from({ length: count }).map((_, index) => (
        <div key={index} className="animate-pulse rounded-3xl border border-slate-200 bg-white p-4 shadow-soft">
          <div className="h-52 rounded-2xl bg-slate-200" />
          <div className="mt-4 h-4 w-2/3 rounded-full bg-slate-200" />
          <div className="mt-3 h-3 w-1/2 rounded-full bg-slate-200" />
          <div className="mt-5 grid grid-cols-3 gap-3">
            <div className="h-10 rounded-2xl bg-slate-200" />
            <div className="h-10 rounded-2xl bg-slate-200" />
            <div className="h-10 rounded-2xl bg-slate-200" />
          </div>
        </div>
      ))}
    </div>
  );
}