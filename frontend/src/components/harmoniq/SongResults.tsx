import { Music4, Sparkles, Repeat } from "lucide-react";
import { Link } from "@tanstack/react-router";

export type Song = {
  id: number;
  titulo: string;
  letra: string | null;
  album_id: number | null;
  progressao_relativa: string | null;
  artista?: string | null;
  album?: string | { titulo: string } | null;
};

export type SongSearchResult = {
  musica: Song;
  similaridade: number;
  ocorrencias?: number; 
};

type SongResultsProps = {
  songs: Song[] | SongSearchResult[];
  searchedSequence?: string[];
  tone: "manual" | "audio";
};

export function SongResults({ songs, searchedSequence, tone }: SongResultsProps) {
  const resultados = songs.map((item) => {
    if ("musica" in item) {
      return item;
    }

    return {
      musica: item,
      similaridade: null,
      ocorrencias: undefined
    };
  });

  return (
    <section className="animate-rise">
      <header className="mb-4 flex items-center gap-2">
        <Sparkles className="size-4 text-muted-foreground" />
        <h3 className="font-display text-sm font-semibold tracking-wide text-muted-foreground uppercase">
          {songs.length}{" "}
          {songs.length === 1
            ? "música encontrada"
            : "músicas encontradas"}
        </h3>
      </header>

      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        {resultados.map(({ musica: song, similaridade, ocorrencias }) => (
          <Link
            key={song.id}
            to="/musica/$id"
            params={{ id: String(song.id) }}
            className="block cursor-pointer"
          >
            <article
              key={song.id}
              className="glass group rounded-2xl p-4 transition-transform duration-200 hover:-translate-y-1"
            >
              <div className="grid grid-cols-[minmax(0,1fr)_auto] items-start gap-3">
                <div className="min-w-0">
                  <h4 className="truncate font-display text-base font-semibold">
                    {song.titulo}
                  </h4>
                  <p className="text-sm text-muted-foreground">Música</p>

                  {ocorrencias !== undefined && ocorrencias > 0 && (
                    <div className="mt-2 inline-flex items-center gap-1 rounded-md bg-secondary/80 px-2 py-0.5 text-xs font-medium text-secondary-foreground">
                      <Repeat className="size-3 text-emerald" />
                      <span>
                        {ocorrencias} {ocorrencias === 1 ? "trecho encontrado" : "trechos encontrados"}
                      </span>
                    </div>
                  )}
                </div>

                {similaridade !== null && (
                  <div className="text-right">
                    <span className="text-lg font-semibold text-emerald">
                      {similaridade.toFixed(1)}%
                    </span>
                    <p className="text-xs text-muted-foreground">
                      Similaridade
                    </p>
                  </div>
                )}
              </div>

              {searchedSequence && searchedSequence.length > 0 && (
                <div className="mt-3 flex items-center gap-1.5 text-xs font-medium text-emerald">
                  <Music4 className="size-3.5 shrink-0" />
                  <span className="truncate">
                    Sequência buscada: {searchedSequence.join(" ")}
                  </span>
                </div>
              )}
            </article>
          </Link>
        ))}
      </div>
    </section>
  );
}