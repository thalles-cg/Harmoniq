import { Music4, Sparkles } from "lucide-react";

export type Song = {
  id: number;
  titulo: string;
  letra: string | null;
  album_id: number | null;
  progressao_relativa: string | null;
};

export function SongResults({
  songs,
  tone,
}: {
  songs: Song[];
  tone: "manual" | "audio";
}) {
  return (
    <section className="animate-rise">
      <header className="mb-4 flex items-center gap-2">
        <Sparkles className="size-4 text-muted-foreground" />
        <h3 className="font-display text-sm font-semibold tracking-wide text-muted-foreground uppercase">
          {songs.length} músicas encontradas
        </h3>
      </header>

      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        {songs.map((song) => (
          <article
            key={song.id}
            className="glass group rounded-2xl p-4 transition-transform duration-200 hover:-translate-y-1"
          >
            <div className="grid grid-cols-[minmax(0,1fr)_auto] items-start gap-3">
              <div className="min-w-0">
                <h4 className="truncate font-display text-base font-semibold">
                  {song.titulo}
                </h4>

                <p className="text-sm text-muted-foreground">
                  Música
                </p>
              </div>
            </div>

            {song.progressao_relativa && (
              <div className="mt-4 flex flex-wrap items-center gap-2 text-xs">
                <span className="flex items-center gap-1.5 rounded-lg bg-secondary px-2 py-1 text-secondary-foreground">
                  <Music4 className="size-3.5" />
                  {song.progressao_relativa}
                </span>
              </div>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}