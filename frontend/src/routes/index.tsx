import { useEffect, useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import {
  Keyboard,
  Mic,
  ChevronUp,
  ChevronDown,
  ArrowLeft,
  Music,
  LogIn,
  LogOut,
  User,
} from "lucide-react";
import { ManualPanel } from "@/components/harmoniq/ManualPanel";
import { AudioPanel } from "@/components/harmoniq/AudioPanel";
import { buscarUsuarioAutenticado, logout } from "@/services/auth";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "HarmoniQ — Descubra músicas pelos acordes ou pelo áudio" },
      {
        name: "description",
        content:
          "HarmoniQ encontra músicas a partir dos acordes que você conhece ou de uma gravação de 30s do seu instrumento.",
      },
      { property: "og:title", content: "HarmoniQ — Acordes e progressões" },
      {
        property: "og:description",
        content:
          "Busque músicas por progressão de acordes ou identifique acordes por áudio com IA.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Home,
});

type Mode = "split" | "manual" | "audio";

function Home() {
  const [mode, setMode] = useState<Mode>("split");
  const [autenticado, setAutenticado] = useState(false);

  useEffect(() => {
    async function verificarAutenticacao() {
      const usuario = await buscarUsuarioAutenticado();

      setAutenticado(usuario !== null);
    }

    verificarAutenticacao();
  }, []);

  const manualClass =
    mode === "manual"
      ? "h-[calc(100dvh-3.5rem)] md:h-[calc(100dvh-3.5rem)]"
      : mode === "audio"
        ? "h-14"
        : "h-[50dvh]";

  const audioClass =
    mode === "audio"
      ? "h-[calc(100dvh-3.5rem)] md:h-[calc(100dvh-3.5rem)]"
      : mode === "manual"
        ? "h-14"
        : "h-[50dvh]";

  return (
    <main className="min-h-dvh overflow-hidden bg-background font-sans text-foreground">
      <h1 className="sr-only">
        HarmoniQ - buscador de acordes e progressões musicais
      </h1>

      {/* Barra superior */}
      <header className="pointer-events-none absolute inset-x-0 top-0 z-10 flex items-center justify-between px-5 py-5">
        <div className="pointer-events-auto flex items-center gap-2 rounded-full bg-background/50 px-4 py-2 backdrop-blur-md">
          <Music className="size-4 text-emerald" />
          <span className="font-display text-sm font-semibold tracking-tight">
            HarmoniQ
          </span>
        </div>

        {autenticado ? (
          <div className="pointer-events-auto flex items-center gap-2">
            <Link
              to="/perfil"
              className="flex items-center gap-2 rounded-full bg-background/50 px-4 py-2 text-sm font-medium backdrop-blur-md transition-colors hover:bg-background/70"
            >
              <User className="size-4 text-emerald" />
              <span>Perfil</span>
            </Link>

            <button
              onClick={() => {
                logout();
                setAutenticado(false);
              }}
              className="flex items-center gap-2 rounded-full bg-background/50 px-4 py-2 text-sm font-medium backdrop-blur-md transition-colors hover:bg-background/70"
            >
              <LogOut className="size-4" />
              Sair
            </button>
          </div>
        ) : (
          <Link
            to="/login"
            className="pointer-events-auto flex items-center gap-2 rounded-full bg-background/50 px-4 py-2 text-sm font-medium backdrop-blur-md transition-colors hover:bg-background/70"
          >
            <LogIn className="size-4" />
            Entrar
          </Link>
        )}
      </header>

      {/* Manual section */}
      <section
        className={`surface-manual relative overflow-hidden transition-[height] duration-500 ease-[cubic-bezier(0.65,0,0.35,1)] ${manualClass}`}
      >
        {mode === "audio" ? (
          <button
            onClick={() => setMode("manual")}
            className="flex h-14 w-full items-center justify-between px-5"
          >
            <span className="flex items-center gap-2 text-sm font-medium">
              <Keyboard className="size-4" /> Busca por Acordes
            </span>

            <ChevronDown className="size-5 text-muted-foreground" />
          </button>
        ) : mode === "manual" ? (
          <div className="flex h-full flex-col">
            <header className="grid shrink-0 grid-cols-[auto_minmax(0,1fr)] items-center gap-3 px-5 pb-4 pt-16 sm:pt-20">
              <button
                onClick={() => setMode("split")}
                className="flex items-center gap-2 rounded-xl bg-background/40 px-3 py-2 text-sm backdrop-blur-md transition-colors hover:bg-background/70"
              >
                <ArrowLeft className="size-4" /> Voltar
              </button>

              <h2 className="truncate font-display text-lg font-semibold">
                Busca por Acordes
              </h2>
            </header>

            <div className="min-h-0 flex-1 overflow-y-auto pt-2">
              <ManualPanel />
            </div>
          </div>
        ) : (
          <button
            onClick={() => setMode("manual")}
            className="group flex h-full w-full flex-col items-center justify-center gap-4 px-6 text-center"
          >
            <span className="grid size-16 place-items-center rounded-2xl bg-[image:var(--gradient-manual)] shadow-[var(--shadow-glow-manual)] transition-transform group-hover:scale-110">
              <Keyboard className="size-8 text-primary-foreground" />
            </span>

            <h2 className="font-display text-3xl font-bold sm:text-4xl">
              Busca por Acordes
            </h2>

            <p className="max-w-sm text-sm text-muted-foreground">
              Escreva ou selecione seus acordes para encontrar músicas
            </p>

            <ChevronUp className="size-5 rotate-180 text-muted-foreground" />
          </button>
        )}
      </section>

      {/* Audio section */}
      <section
        className={`surface-audio relative overflow-hidden transition-[height] duration-500 ease-[cubic-bezier(0.65,0,0.35,1)] ${audioClass}`}
      >
        {mode === "manual" ? (
          <button
            onClick={() => setMode("audio")}
            className="flex h-14 w-full items-center justify-between px-5"
          >
            <span className="flex items-center gap-2 text-sm font-medium">
              <Mic className="size-4" /> Identificação por Áudio
            </span>

            <ChevronUp className="size-5 text-muted-foreground" />
          </button>
        ) : mode === "audio" ? (
          <div className="flex h-full flex-col">
            <header className="grid shrink-0 grid-cols-[auto_minmax(0,1fr)] items-center gap-3 px-5 pb-4 pt-16 sm:pt-20">
              <button
                onClick={() => setMode("split")}
                className="flex items-center gap-2 rounded-xl bg-background/40 px-3 py-2 text-sm backdrop-blur-md transition-colors hover:bg-background/70"
              >
                <ArrowLeft className="size-4" /> Voltar
              </button>

              <h2 className="truncate font-display text-lg font-semibold">
                Identificação por Áudio
              </h2>
            </header>

            <div className="min-h-0 flex-1 overflow-y-auto pt-2">
              <AudioPanel />
            </div>
          </div>
        ) : (
          <button
            onClick={() => setMode("audio")}
            className="group flex h-full w-full flex-col items-center justify-center gap-4 px-6 text-center"
          >
            <span className="relative grid size-16 place-items-center rounded-full bg-[image:var(--gradient-audio)] shadow-[var(--shadow-glow-audio)] transition-transform group-hover:scale-110">
              <span className="absolute inset-0 rounded-full bg-emerald/40 animate-mic-pulse" />
              <Mic className="relative size-8 text-accent-foreground" />
            </span>

            <h2 className="font-display text-3xl font-bold sm:text-4xl">
              Identificação por Áudio
            </h2>

            <p className="max-w-sm text-sm text-muted-foreground">
              Grave um áudio de 30s tocando um instrumento
            </p>

            <ChevronDown className="size-5 text-muted-foreground" />
          </button>
        )}
      </section>
    </main>
  );
}