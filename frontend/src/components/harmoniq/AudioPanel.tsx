import { useEffect, useRef, useState } from "react";
import { Mic, Square, UploadCloud, Volume2, Sparkles, Loader2 } from "lucide-react";
import { AUDIO_SONGS, SongResults } from "./SongResults";

const BARS = Array.from({ length: 36 }, (_, i) => i);
const DETECTED = ["G", "D", "Em", "C", "G", "D", "C", "C"];

export function AudioPanel() {
  const [recording, setRecording] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const [fileName, setFileName] = useState<string | null>(null);
  const [status, setStatus] = useState<"idle" | "loading" | "done">("idle");
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (!recording) return;
    timer.current = setInterval(() => {
      setSeconds((s) => {
        if (s >= 30) {
          setRecording(false);
          return 30;
        }
        return s + 1;
      });
    }, 1000);
    return () => {
      if (timer.current) clearInterval(timer.current);
    };
  }, [recording]);

  useEffect(() => {
    if (status !== "loading") return;
    const t = setTimeout(() => setStatus("done"), 2400);
    return () => clearTimeout(t);
  }, [status]);

  const fmt = (s: number) => `00:${String(s).padStart(2, "0")}`;

  return (
    <div className="mx-auto w-full max-w-5xl space-y-6 px-4 pb-16 sm:px-6">
      <div className="glass flex flex-col items-center gap-6 rounded-2xl p-8">
        <div className="relative grid place-items-center">
          {recording && (
            <>
              <span className="absolute size-28 rounded-full bg-destructive/40 animate-mic-pulse" />
              <span className="absolute size-28 rounded-full border border-destructive/60" />
            </>
          )}
          <button
            onClick={() => {
              setSeconds(0);
              setRecording((r) => !r);
            }}
            aria-label={recording ? "Parar gravação" : "Iniciar gravação"}
            className={`relative grid size-24 place-items-center rounded-full transition-transform hover:scale-105 ${
              recording
                ? "bg-destructive text-destructive-foreground"
                : "bg-[image:var(--gradient-audio)] text-accent-foreground shadow-[var(--shadow-glow-audio)]"
            }`}
          >
            {recording ? <Square className="size-8" /> : <Mic className="size-10" />}
          </button>
        </div>

        <p className="font-display text-2xl tabular-nums">
          {fmt(seconds)} <span className="text-muted-foreground">/ 00:30</span>
        </p>

        <div className="flex h-16 w-full items-center justify-center gap-1">
          {BARS.map((i) => (
            <span
              key={i}
              className={`w-1.5 rounded-full transition-all duration-300 ${
                recording ? "bg-[image:var(--gradient-audio)]" : "bg-muted"
              }`}
              style={{
                height: recording ? `${20 + Math.abs(Math.sin(i * 1.7 + seconds)) * 80}%` : "12%",
              }}
            />
          ))}
        </div>
        <p className="flex items-center gap-2 text-xs text-muted-foreground">
          <Volume2 className="size-3.5" />
          {recording ? "Gravando… toque seu instrumento perto do microfone" : "Pronto para gravar 30s"}
        </p>
      </div>

      <label
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          setFileName(e.dataTransfer.files?.[0]?.name ?? null);
        }}
        className="flex cursor-pointer flex-col items-center gap-2 rounded-2xl border border-dashed border-border bg-background/40 px-6 py-8 text-center transition-colors hover:border-emerald"
      >
        <UploadCloud className="size-6 text-emerald" />
        <span className="text-sm">Ou envie um arquivo .mp3 ou .wav</span>
        <span className="text-xs text-muted-foreground">
          {fileName ?? "Arraste e solte aqui ou clique para selecionar"}
        </span>
        <input
          type="file"
          accept=".mp3,.wav,audio/*"
          className="hidden"
          onChange={(e) => setFileName(e.target.files?.[0]?.name ?? null)}
        />
      </label>

      <button
        onClick={() => setStatus("loading")}
        className="flex w-full items-center justify-center gap-2 rounded-xl bg-[image:var(--gradient-audio)] px-6 py-3.5 font-display font-semibold text-accent-foreground shadow-[var(--shadow-glow-audio)] transition-transform hover:scale-[1.01]"
      >
        <Sparkles className="size-4" />
        Analisar Áudio e Buscar
      </button>

      {status === "loading" && (
        <div className="glass flex items-center gap-3 rounded-2xl p-5 text-sm text-muted-foreground">
          <Loader2 className="size-4 animate-spin text-emerald" />
          IA analisando notas e extraindo acordes com Basic Pitch…
        </div>
      )}

      {status === "done" && (
        <div className="animate-rise space-y-6">
          <div className="glass rounded-2xl p-5">
            <p className="mb-3 text-xs tracking-wide text-muted-foreground uppercase">
              Acordes detectados no áudio
            </p>
            <div className="flex flex-wrap gap-2">
              {DETECTED.map((chord, i) => (
                <span
                  key={`${chord}-${i}`}
                  className="rounded-full bg-[image:var(--gradient-audio)] px-3 py-1.5 text-sm font-medium text-accent-foreground"
                >
                  {chord}
                </span>
              ))}
            </div>
          </div>
          <SongResults songs={AUDIO_SONGS} tone="audio" />
        </div>
      )}
    </div>
  );
}
