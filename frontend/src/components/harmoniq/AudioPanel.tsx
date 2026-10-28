import { useEffect, useRef, useState } from "react";
import {
  Mic,
  Square,
  UploadCloud,
  Volume2,
  Sparkles,
  Loader2,
  AlertCircle,
  Music2,
  ListMusic,
} from "lucide-react";
import { transcreverAudio, type AcordeDetectado } from "@/services/transcricao";

const BARS = Array.from({ length: 36 }, (_, i) => i);

const NOTAS_PITCH: Record<string, number> = {
  C: 0, "C#": 1, Db: 1, D: 2, "D#": 3, Eb: 3, E: 4, Fb: 4, "E#": 5,
  F: 5, "F#": 6, Gb: 6, G: 7, "G#": 8, Ab: 8, A: 9, "A#": 10, Bb: 10, B: 11, Cb: 11,
};

// Converte notações do BTC (ex: "A:min", "C:maj") para cifras padrão ("Am", "C")
export function formatarCifra(cifra: string): string {
  if (!cifra || cifra === "N") return "";
  const limpa = cifra.trim();

  const partes = limpa.split(":");
  const raiz = partes[0];
  const tipo = partes[1];

  if (!raiz) return "";
  if (!tipo) return raiz;

  if (tipo === "maj") return raiz;
  if (tipo === "min") return `${raiz}m`;
  if (tipo === "min7") return `${raiz}m7`;
  if (tipo === "maj7") return `${raiz}maj7`;

  return `${raiz}${tipo}`;
}

function extrairRaizEQualidade(cifra: string): { raiz: string; pitch: number; eMenor: boolean } | null {
  const match = cifra.trim().match(/^([A-G][#b]?)(.*)$/);
  if (!match || !match[1]) return null;

  const raiz = match[1];
  const resto = match[2] || "";
  const pitch = NOTAS_PITCH[raiz];
  if (pitch === undefined) return null;

  const eMenor = /^m(?!aj)/i.test(resto);
  return { raiz, pitch, eMenor };
}

export function converterAcordesParaGraus(cifras: string[]): string[] {
  const parsed = cifras
    .map(extrairRaizEQualidade)
    .filter((item): item is NonNullable<typeof item> => item !== null);

  const primeiro = parsed[0];
  if (!primeiro) return [];

  let melhorTonalidade = { tonicaPitch: primeiro.pitch, eMenor: primeiro.eMenor, score: -1 };

  for (let t = 0; t < 12; t++) {
    for (const eMenor of [false, true]) {
      let score = 0;
      for (const item of parsed) {
        const interval = (item.pitch - t + 12) % 12;
        if (!eMenor) {
          if (
            (!item.eMenor && [0, 5, 7].includes(interval)) ||
            (item.eMenor && [2, 4, 9, 11].includes(interval))
          ) {
            score++;
          }
        } else {
          if (
            (item.eMenor && [0, 2, 5, 7].includes(interval)) ||
            (!item.eMenor && [3, 7, 8, 10].includes(interval))
          ) {
            score++;
          }
        }
      }

      const eTonalidadeDoPrimeiro = t === primeiro.pitch && eMenor === primeiro.eMenor;
      const scoreFinal = score + (eTonalidadeDoPrimeiro ? 0.5 : 0);

      if (scoreFinal > melhorTonalidade.score) {
        melhorTonalidade = { tonicaPitch: t, eMenor, score: scoreFinal };
      }
    }
  }

  const { tonicaPitch, eMenor: tomMenor } = melhorTonalidade;

  const grausMaior: Record<number, { maj: string; min: string }> = {
    0: { maj: "I", min: "i" },
    1: { maj: "bII", min: "bii" },
    2: { maj: "II", min: "ii" },
    3: { maj: "bIII", min: "biii" },
    4: { maj: "III", min: "iii" },
    5: { maj: "IV", min: "iv" },
    6: { maj: "#IV", min: "#iv" },
    7: { maj: "V", min: "v" },
    8: { maj: "bVI", min: "bvi" },
    9: { maj: "VI", min: "vi" },
    10: { maj: "bVII", min: "bvii" },
    11: { maj: "VII", min: "vii" },
  };

  const grausMenor: Record<number, { maj: string; min: string }> = {
    0: { maj: "I", min: "i" },
    1: { maj: "bII", min: "bii" },
    2: { maj: "II", min: "ii" },
    3: { maj: "III", min: "biii" },
    4: { maj: "#III", min: "iii" },
    5: { maj: "IV", min: "iv" },
    6: { maj: "#IV", min: "#iv" },
    7: { maj: "V", min: "v" },
    8: { maj: "VI", min: "bvi" },
    9: { maj: "#VI", min: "#iv" },
    10: { maj: "VII", min: "bvii" },
    11: { maj: "#VII", min: "vii" },
  };

  const tabela = tomMenor ? grausMenor : grausMaior;

  return parsed.map((item) => {
    const interval = (item.pitch - tonicaPitch + 12) % 12;
    const info = tabela[interval] ?? { maj: "I", min: "i" };
    return item.eMenor ? info.min : info.maj;
  });
}

type AudioPanelProps = {
  onBuscarRepertorio?: (acordes: string[]) => void;
  onBuscarSequencia?: (graus: string[]) => void;
};

export function AudioPanel({
  onBuscarRepertorio,
  onBuscarSequencia,
}: AudioPanelProps) {
  const [recording, setRecording] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const [arquivo, setArquivo] = useState<File | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [acordes, setAcordes] = useState<AcordeDetectado[]>([]);
  const [status, setStatus] = useState<"idle" | "loading" | "done" | "error">("idle");
  const [erro, setErro] = useState("");

  const timer = useRef<ReturnType<typeof setInterval> | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const streamRef = useRef<MediaStream | null>(null);

  useEffect(() => {
    if (!arquivo) {
      setAudioUrl(null);
      return;
    }

    const url = URL.createObjectURL(arquivo);
    setAudioUrl(url);

    return () => {
      URL.revokeObjectURL(url);
    };
  }, [arquivo]);

  async function iniciarGravacao() {
    setErro("");
    setArquivo(null);
    setAcordes([]);
    setStatus("idle");
    audioChunksRef.current = [];

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: false,
          noiseSuppression: false,
          autoGainControl: false,
        },
      });
      streamRef.current = stream;

      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const mimeType = mediaRecorder.mimeType || "audio/webm";
        const audioBlob = new Blob(audioChunksRef.current, { type: mimeType });
        const file = new File([audioBlob], "audio_capturado.webm", { type: mimeType });

        setArquivo(file);

        if (streamRef.current) {
          streamRef.current.getTracks().forEach((track) => track.stop());
          streamRef.current = null;
        }
      };

      mediaRecorder.start(250);
      setSeconds(0);
      setRecording(true);
    } catch (err) {
      console.error("Erro ao acessar microfone:", err);
      setErro("Permissão de microfone negada ou dispositivo indisponível.");
      setStatus("error");
    }
  }

  function pararGravacao() {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
      mediaRecorderRef.current.stop();
    }
    setRecording(false);
  }

  useEffect(() => {
    if (!recording) return;

    timer.current = setInterval(() => {
      setSeconds((s) => {
        if (s >= 29) {
          pararGravacao();
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
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

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
      const resultadoFormatado = resultado
        .map((item) => ({
          ...item,
          acorde: formatarCifra(item.acorde),
        }))
        .filter((item) => item.acorde.length > 0);

      setAcordes(resultadoFormatado);
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

  function obterSequenciaFormatada(): string[] {
    const listaRaw = acordes.map((item) => item.acorde.trim()).filter(Boolean);
    return listaRaw.filter((acorde, i) => i === 0 || acorde !== listaRaw[i - 1]);
  }

  function obterSequenciaEmGraus(): string[] {
    const seqCifras = obterSequenciaFormatada();
    return converterAcordesParaGraus(seqCifras);
  }

  function obterAcordesUnicos(): string[] {
    return Array.from(
      new Set(acordes.map((item) => item.acorde.trim()).filter(Boolean))
    );
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
                pararGravacao();
              } else {
                iniciarGravacao();
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
            ? "Gravando áudio do microfone..."
            : arquivo
              ? "Áudio pronto para análise."
              : "Clique no microfone para gravar ou selecione um arquivo abaixo."}
        </p>

        {audioUrl && (
          <div className="w-full max-w-md pt-2">
            <p className="mb-2 text-center text-xs text-muted-foreground">
              Pré-escuta do áudio capturado:
            </p>
            <audio controls src={audioUrl} className="w-full rounded-xl shadow-inner" />
          </div>
        )}
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
          {arquivo ? "Áudio selecionado" : "Arraste e solte aqui ou clique para selecionar"}
        </span>

        <input
          type="file"
          accept=".mp3,.wav,.flac,.ogg,.m4a,.webm,audio/*"
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
        <div className="glass animate-rise space-y-5 rounded-2xl p-5">
          <div>
            <p className="mb-3 text-xs uppercase tracking-wide text-muted-foreground">
              Acordes detectados no áudio
            </p>

            {acordes.length === 0 ? (
              <p className="text-sm text-muted-foreground">
                Nenhum acorde foi identificado neste áudio. Tente tocar um instrumento harmônico (violão, guitarra, piano) mais próximo do microfone.
              </p>
            ) : (
              <div className="space-y-4">
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

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                  <button
                    type="button"
                    onClick={() =>
                      onBuscarRepertorio && onBuscarRepertorio(obterAcordesUnicos())
                    }
                    className="flex items-center justify-center gap-2 rounded-xl bg-background/50 px-4 py-3 text-sm font-medium transition-colors hover:bg-background/80 border border-border"
                  >
                    <ListMusic className="size-4 text-emerald" />
                    Buscar por Repertório ({obterAcordesUnicos().join(", ")})
                  </button>

                  <button
                    type="button"
                    onClick={() =>
                      onBuscarSequencia && onBuscarSequencia(obterSequenciaEmGraus())
                    }
                    className="flex items-center justify-center gap-2 rounded-xl bg-emerald/15 px-4 py-3 text-sm font-medium text-emerald transition-colors hover:bg-emerald/20 border border-emerald/30"
                  >
                    <Music2 className="size-4" />
                    Buscar por Sequência ({obterSequenciaEmGraus().join(" → ")})
                  </button>
                </div>
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