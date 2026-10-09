import { useEffect, useRef, useState } from "react";
import {Mic, Square, UploadCloud, Volume2, Sparkles, Loader2, AlertCircle,} from "lucide-react";
import { transcreverAudio, type AcordeDetectado } from "@/services/transcricao";

const BARS = Array.from({ length: 36 }, (_, i) => i);

export function AudioPanel() {
  const [recording, setRecording] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const [arquivo, setArquivo] = useState<File | null>(null);
  const [acordes, setAcordes] = useState<AcordeDetectado[]>([]);
  const [status, setStatus] = useState<"idle" | "loading" | "done" | "error">(
    "idle",
  );
  const [erro, setErro] = useState("");
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (!recording) return;
    timer.current = setInterval(() => {
      setSeconds((s) => {
        if (s >= 29) {
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

  const fmt = (s: number) => `00:${String(s).padStart(2, "0")}`;

  function selecionarArquivo(file: File | undefined) {
    if (!file) return;

    setArquivo(file);
    setAcordes([]);
    setErro("");
    setStatus("idle");
  }

  async function handleAnalise() {
    if (!arquivo || status === "loading") return;

    setStatus("loading");
    setErro("");
    setAcordes([]);

    try {
      const resultado = await transcreverAudio(arquivo);
      setAcordes(resultado);
      setStatus("done");
    } catch (error) {
      console.error("Erro ao transcrever áudio:", error);
      setErro(
        error instanceof Error
          ? error.message
          : "Ocorreu um erro ao analisar o áudio.",
      );
      setStatus("error");
    }
  }

  return (
    <div className="mx-auto w-full max-w-5xl space-y-6 px-4 pb-16 sm:px-6">
      <div className="glass flex flex-col items-center gap-6 rounded-2xl p-8">
        <div className="relative grid place-items-center">
          {recording && (
            <>
              <span className="absolute size-28 animate-mic-pulse rounded-full bg-destructive/40" />
              <span className="absolute size-28 rounded-full border border-destructive/60" />
            </>
          )}

          <button
            type="button"
            onClick={() => {
              if (recording) {
                setRecording(false);
              } else {
                setSeconds(0);
                setRecording(true);
              }
            }}
            aria-label={recording ? "Parar gravação" : "Iniciar gravação"}
            className={`relative grid size-24 place-items-center rounded-full transition-transform hover:scale-105 ${
              recording
                ? "bg-destructive text-destructive-foreground"
                : "bg-[image:var(--gradient-audio)] text-accent-foreground shadow-[var(--shadow-glow-audio)]"
            }`}
          >
            {recording ? (
              <Square className="size-8" />
            ) : (
              <Mic className="size-10" />
            )}
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
                height: recording
                  ? `${20 + Math.abs(Math.sin(i * 1.7 + seconds)) * 80}%`
                  : "12%",
              }}
            />
          ))}
        </div>

        <p className="flex items-center gap-2 text-xs text-muted-foreground">
          <Volume2 className="size-3.5" />
          {recording
            ? "O temporizador está ativo; a captura de áudio ainda não foi implementada."
            : "Selecione um arquivo de áudio para começar a análise."}
        </p>
      </div>

      <label
        onDragOver={(event) => event.preventDefault()}
        onDrop={(event) => {
          event.preventDefault();
          selecionarArquivo(event.dataTransfer.files?.[0]);
        }}
        className="flex cursor-pointer flex-col items-center gap-2 rounded-2xl border border-dashed border-border bg-background/40 px-6 py-8 text-center transition-colors hover:border-emerald"
      >
        <UploadCloud className="size-6 text-emerald" />
        <span className="text-sm">Envie um arquivo de áudio</span>
        <span className="text-xs text-muted-foreground">
          {arquivo?.name ?? "Arraste e solte aqui ou clique para selecionar"}
        </span>

        <input
          type="file"
          accept=".mp3,.wav,.flac,.ogg,.m4a,audio/*"
          className="hidden"
          onChange={(event) => selecionarArquivo(event.target.files?.[0])}
        />
      </label>

      <button
        type="button"
        onClick={handleAnalise}
        disabled={!arquivo || status === "loading"}
        className="flex w-full items-center justify-center gap-2 rounded-xl bg-[image:var(--gradient-audio)] px-6 py-3.5 font-display font-semibold text-accent-foreground shadow-[var(--shadow-glow-audio)] transition-transform hover:scale-[1.01] disabled:cursor-not-allowed disabled:opacity-50"
      >
        {status === "loading" ? (
          <Loader2 className="size-4 animate-spin" />
        ) : (
          <Sparkles className="size-4" />
        )}
        {status === "loading" ? "Analisando áudio..." : "Analisar Áudio"}
      </button>

      {status === "loading" && (
        <div className="glass flex items-center gap-3 rounded-2xl p-5 text-sm text-muted-foreground">
          <Loader2 className="size-4 animate-spin text-emerald" />
          Analisando o áudio e identificando acordes...
        </div>
      )}

      {status === "error" && (
        <div
          role="alert"
          className="flex items-center gap-3 rounded-2xl border border-destructive/30 bg-destructive/10 p-5 text-sm text-destructive"
        >
          <AlertCircle className="size-5 shrink-0" />
          {erro}
        </div>
      )}

      {status === "done" && (
        <div className="glass animate-rise space-y-4 rounded-2xl p-5">
          <div>
            <p className="mb-3 text-xs uppercase tracking-wide text-muted-foreground">
              Acordes detectados no áudio
            </p>

            {acordes.length === 0 ? (
              <p className="text-sm text-muted-foreground">
                Nenhum acorde foi identificado neste áudio.
              </p>
            ) : (
              <div className="flex flex-wrap gap-2">
                {acordes.map((item, i) => (
                  <span
                    key={`${item.inicio}-${item.fim}-${i}`}
                    title={`${item.inicio.toFixed(2)}s – ${item.fim.toFixed(2)}s`}
                    className="rounded-full bg-[image:var(--gradient-audio)] px-3 py-1.5 text-sm font-medium text-accent-foreground"
                  >
                    {item.acorde}
                    <span className="ml-2 text-xs opacity-80">
                      {item.inicio.toFixed(1)}s
                    </span>
                  </span>
                ))}
              </div>
            )}
          </div>

          <p className="text-xs text-muted-foreground">
            Os horários indicam o início de cada acorde detectado.
          </p>
        </div>
      )}
    </div>
  );
}

