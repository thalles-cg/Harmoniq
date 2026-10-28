import { useEffect, useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowLeft, Music, User, Disc, Loader2, AlertCircle } from "lucide-react";
import type { Song } from "@/components/harmoniq/SongResults";

const API_URL = import.meta.env["VITE_API_URL"];

export const Route = createFileRoute("/musica/$id")({
  head: () => ({
    meta: [
      { title: "Cifra — HarmoniQ" },
      {
        name: "description",
        content: "Visualização de cifra e estrutura harmônica da música.",
      },
    ],
  }),
  component: MusicaPage,
});

function MusicaPage() {
  const { id } = Route.useParams();
  const [musica, setMusica] = useState<Song | null>(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  useEffect(() => {
    async function carregarMusica() {
      setCarregando(true);
      setErro("");

      try {
        const response = await fetch(`${API_URL}/musicas/${id}`);
        if (!response.ok) {
          throw new Error("Música não encontrada.");
        }
        const data: Song = await response.json();
        setMusica(data);
      } catch (err) {
        console.error("Erro ao carregar música:", err);
        setErro(
          err instanceof Error ? err.message : "Erro ao carregar a música."
        );
      } finally {
        setCarregando(false);
      }
    }

    carregarMusica();
  }, [id]);

  const nomeAlbum =
    typeof musica?.album === "object" ? musica.album?.titulo : musica?.album;

  return (
    <main className="min-h-dvh bg-background font-sans text-foreground pb-16">
      <div className="mx-auto flex w-full max-w-4xl flex-col px-4 py-6 sm:px-6">
        {/* Cabeçalho de Navegação */}
        <div className="mb-8 flex items-center justify-between">
          <Link
            to="/"
            className="flex items-center gap-2 rounded-full bg-background/50 px-4 py-2 backdrop-blur-md transition-colors hover:bg-background/70 border border-border"
          >
            <ArrowLeft className="size-4" />
            <span className="text-sm font-medium">Voltar</span>
          </Link>

          <div className="flex items-center gap-2 rounded-full bg-background/50 px-4 py-2 backdrop-blur-md border border-border">
            <Music className="size-4 text-emerald" />
            <span className="font-display text-sm font-semibold tracking-tight">
              HarmoniQ
            </span>
          </div>
        </div>

        {/* Estado de Carregamento */}
        {carregando && (
          <div className="glass flex items-center justify-center gap-3 rounded-2xl p-12 text-muted-foreground">
            <Loader2 className="size-6 animate-spin text-emerald" />
            Carregando cifra...
          </div>
        )}

        {/* Estado de Erro */}
        {erro && (
          <div className="flex items-center gap-3 rounded-2xl border border-destructive/30 bg-destructive/10 p-6 text-destructive">
            <AlertCircle className="size-5 shrink-0" />
            {erro}
          </div>
        )}

        {/* Detalhes da Música e Cifra */}
        {!carregando && !erro && musica && (
          <article className="space-y-6">
            <div className="glass rounded-2xl p-6 sm:p-8 space-y-3">
              <h1 className="font-display text-3xl sm:text-4xl font-bold tracking-tight">
                {musica.titulo}
              </h1>

              {(musica.artista || nomeAlbum) && (
                <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
                  {musica.artista && (
                    <div className="flex items-center gap-1.5">
                      <User className="size-4 text-emerald shrink-0" />
                      <span>{musica.artista}</span>
                    </div>
                  )}

                  {nomeAlbum && (
                    <div className="flex items-center gap-1.5">
                      <Disc className="size-4 text-emerald shrink-0" />
                      <span>{nomeAlbum}</span>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Container da Cifra */}
            <div className="glass rounded-2xl p-6 sm:p-8 overflow-x-auto">
              {musica.letra ? (
                <pre className="font-mono text-sm sm:text-base leading-relaxed text-foreground/90 whitespace-pre overflow-x-auto">
                  {musica.letra}
                </pre>
              ) : (
                <p className="text-muted-foreground text-sm">
                  Nenhuma cifra/letra cadastrada para esta música.
                </p>
              )}
            </div>
          </article>
        )}
      </div>
    </main>
  );
}