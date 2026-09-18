import { Music4, Sparkles } from "lucide-react";

export type Song = {
  title: string;
  artist: string;
  key: string;
  progression: string;
  match: number;
};

export const MANUAL_SONGS: Song[] = [
  { title: "Wonderwall", artist: "Oasis", key: "F#m", progression: "Em – G – D – A", match: 98 },
  { title: "Trem-Bala", artist: "Ana Vilela", key: "D", progression: "C – G – Am – F", match: 95 },
  { title: "Let It Be", artist: "The Beatles", key: "C", progression: "C – G – Am – F", match: 93 },
  { title: "Sozinho", artist: "Caetano Veloso", key: "G", progression: "G – Em – C – D", match: 88 },
  { title: "Tempo Perdido", artist: "Legião Urbana", key: "E", progression: "C – G – Am – F", match: 84 },
  { title: "Anna Júlia", artist: "Los Hermanos", key: "A", progression: "G – D – Em – C", match: 79 },
];

export const AUDIO_SONGS: Song[] = [
  { title: "Além do Horizonte", artist: "Jota Quest", key: "G", progression: "G – D – Em – C", match: 96 },
  { title: "Toda Forma de Amor", artist: "Lulu Santos", key: "C", progression: "C – Am – F – G", match: 91 },
  { title: "Pais e Filhos", artist: "Legião Urbana", key: "D", progression: "D – A – Bm – G", match: 87 },
  { title: "Riptide", artist: "Vance Joy", key: "C", progression: "Am – G – C – C", match: 82 },
];

export function SongResults({ songs, tone }: { songs: Song[]; tone: "manual" | "audio" }) {
  const badge =
    tone === "manual"
      ? "bg-[image:var(--gradient-manual)] text-primary-foreground"
      : "bg-[image:var(--gradient-audio)] text-accent-foreground";

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
            key={song.title}
            className="glass group rounded-2xl p-4 transition-transform duration-200 hover:-translate-y-1"
          >
            <div className="grid grid-cols-[minmax(0,1fr)_auto] items-start gap-3">
              <div className="min-w-0">
                <h4 className="truncate font-display text-base font-semibold">{song.title}</h4>
                <p className="truncate text-sm text-muted-foreground">{song.artist}</p>
              </div>
              <span className={`shrink-0 rounded-full px-2.5 py-1 text-xs font-semibold ${badge}`}>
                {song.match}%
              </span>
            </div>
            <div className="mt-4 flex flex-wrap items-center gap-2 text-xs">
              <span className="rounded-lg bg-secondary px-2 py-1 text-secondary-foreground">
                Tom {song.key}
              </span>
              <span className="flex items-center gap-1.5 rounded-lg bg-secondary px-2 py-1 text-secondary-foreground">
                <Music4 className="size-3.5" />
                {song.progression}
              </span>
            </div>
            <p className="mt-3 text-[11px] text-muted-foreground">
              {song.match}% de compatibilidade com sua seleção
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}
