import { useEffect, useState } from "react";
import { Search, X, Sparkles, ListOrdered, LayoutGrid } from "lucide-react";
import { SongResults, type Song } from "./SongResults";

type Acorde = {
  id: number;
  nome_cifra: string;
  nome_extenso: string;
  nota_fundamental_id: number;
  nota_fundamental: string;
  qualidade: string;
  notas: number[];
};

const API_URL = import.meta.env["VITE_API_URL"];

export function ManualPanel() {
  const [acordes, setAcordes] = useState<Acorde[]>([]);

  const [mode, setMode] = useState<"exact" | "repertoire">("exact");
  const [query, setQuery] = useState("");

  const [exactChords, setExactChords] = useState<string[]>(["C", "G", "Am", "F",]);
  const [repertoireChords, setRepertoireChords] = useState<string[]>([]);

  const [exactSongs, setExactSongs] = useState<Song[]>([]);
  const [repertoireSongs, setRepertoireSongs] = useState<Song[]>([]);

  const [repertoireSearched, setRepertoireSearched] = useState(false);
  const [loading, setLoading] = useState(false);

  const [capo, setCapo] = useState(true);

  useEffect(() => {
    async function carregarAcordes() {
      try {
        const response = await fetch(`${API_URL}/acordes/`);

        if (!response.ok) {
          throw new Error("Erro ao buscar acordes.");
        }

        const data: Acorde[] = await response.json();

        setAcordes(data);
      } catch (error) {
        console.error("Erro ao carregar acordes:", error);
      }
    }

    carregarAcordes();
  }, []);

  const acordesPorFundamental = acordes.reduce<Record<string, Acorde[]>>(
    (grupos, acorde) => {
      const fundamental = acorde.nota_fundamental;

      const grupo = grupos[fundamental] ?? [];

      grupo.push(acorde);
      grupos[fundamental] = grupo;

      return grupos;
    },
    {},
  );

  const chords = mode === "exact" ? exactChords : repertoireChords;

  const addChord = (chord: string) => {
    if (mode === "exact") {
      setExactChords((prev) => [...prev, chord]);
    } else {
      setRepertoireChords((prev) => [...prev, chord]);
    }
  };

  const removeChord = (index: number) => {
    if (mode === "exact") {
      setExactChords((prev) => prev.filter((_, i) => i !== index));
    } else {
      setRepertoireChords((prev) => prev.filter((_, i) => i !== index));
    }
  };

  const handleSearch = async () => {
    if (mode === "exact") {
      return;
    }

    if (repertoireChords.length === 0) {
      return;
    }

    setLoading(true);

    try {
      const params = new URLSearchParams();

      repertoireChords.forEach((acorde) => {
        params.append("acordes", acorde);
      });

      const response = await fetch(
        `${API_URL}/musicas/busca/repertorio?${params.toString()}`,
      );

      if (!response.ok) {
        throw new Error("Erro ao buscar músicas.");
      }

      const data: Song[] = await response.json();

      setRepertoireSongs(data);
      setRepertoireSearched(true);
    } catch (error) {
      console.error("Erro ao buscar músicas:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto w-full max-w-5xl space-y-6 px-4 pb-16 sm:px-6">
      <div className="inline-flex rounded-2xl bg-secondary/70 p-1">
        {(
          [
            {
              id: "exact",
              label: "Sequência Exata",
              hint: "A ordem importa",
              icon: ListOrdered,
            },
            {
              id: "repertoire",
              label: "Meu Repertório",
              hint: "Acordes que eu sei",
              icon: LayoutGrid,
            },
          ] as const
        ).map((tab) => (
          <button
            key={tab.id}
            onClick={() => setMode(tab.id)}
            className={`flex items-center gap-2 rounded-xl px-4 py-2.5 text-sm font-medium transition-colors ${
              mode === tab.id
                ? "bg-[image:var(--gradient-manual)] text-primary-foreground shadow-[var(--shadow-glow-manual)]"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <tab.icon className="size-4" />
            <span className="hidden sm:inline">{tab.label}</span>
            <span className="sm:hidden">{tab.label.split(" ")[0]}</span>
          </button>
        ))}
      </div>

      <p className="text-sm text-muted-foreground">
        {mode === "exact"
          ? "Buscamos músicas com essa progressão na mesma ordem."
          : "Buscamos músicas que usem apenas os acordes do seu repertório."}
      </p>

      <div className="glass space-y-5 rounded-2xl p-5">
        <div className="relative">
          <Search className="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2 text-muted-foreground" />

          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && query.trim()) {
                addChord(query.trim());
                setQuery("");
              }
            }}
            placeholder="Digite um acorde (ex: Am7) e pressione Enter"
            className="w-full rounded-xl border border-border bg-background/60 py-3 pr-3 pl-9 text-sm outline-none focus:border-violet focus:ring-2 focus:ring-ring/40"
          />
        </div>

        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-7">
          {Object.entries(acordesPorFundamental).map(
            ([fundamental, acordesDaFundamental]) => (
              <div
                key={fundamental}
                className="rounded-xl border border-border bg-background/40 p-2"
              >
                <div className="rounded-lg bg-secondary py-2 text-center font-display text-lg font-semibold">
                  {fundamental}
                </div>

                <div className="mt-2 grid grid-cols-3 gap-1">
                  {acordesDaFundamental.map((acorde) => (
                    <button
                      key={acorde.id}
                      onClick={() => addChord(acorde.nome_cifra)}
                      className="rounded-md bg-muted py-1 text-[11px] text-muted-foreground transition-colors hover:bg-violet/30 hover:text-foreground"
                    >
                      {acorde.qualidade}
                    </button>
                  ))}
                </div>
              </div>
            ),
          )}
        </div>

        <div>
          <p className="mb-2 text-xs tracking-wide text-muted-foreground uppercase">
            {mode === "exact" ? "Sequência selecionada" : "Meus acordes"}
          </p>

          <div className="flex min-h-12 flex-wrap items-center gap-2 rounded-xl border border-dashed border-border p-3">
            {chords.length === 0 && (
              <span className="text-sm text-muted-foreground">
                Nenhum acorde selecionado ainda.
              </span>
            )}

            {chords.map((chord, i) => (
              <span
                key={`${chord}-${i}`}
                className="flex items-center gap-2 rounded-full bg-[image:var(--gradient-manual)] px-3 py-1.5 text-sm font-medium text-primary-foreground"
              >
                {chord}

                <button
                  onClick={() => removeChord(i)}
                  aria-label={`Remover ${chord}`}
                >
                  <X className="size-3.5 opacity-80 hover:opacity-100" />
                </button>
              </span>
            ))}
          </div>
        </div>

        {/* <label className="flex cursor-pointer items-center justify-between gap-4 rounded-xl bg-background/40 px-4 py-3">
          <span className="text-sm">Considerar sugestões com Capotraste</span>
          <button
            role="switch"
            aria-checked={capo}
            onClick={() => setCapo((v) => !v)}
            className={`relative h-6 w-11 shrink-0 rounded-full transition-colors ${
              capo ? "bg-[image:var(--gradient-manual)]" : "bg-muted"
            }`}
          >
            <span
              className={`absolute left-0.5 top-0.5 size-5 rounded-full bg-foreground transition-transform ${
                capo ? "translate-x-5" : "translate-x-0"
              }`}
            />
          </button>
        </label> */}

        <button
          onClick={handleSearch}
          disabled={loading || chords.length === 0}
          className="flex w-full items-center justify-center gap-2 rounded-xl bg-[image:var(--gradient-manual)] px-6 py-3.5 font-display font-semibold text-primary-foreground shadow-[var(--shadow-glow-manual)] transition-transform hover:scale-[1.01] disabled:cursor-not-allowed disabled:opacity-50"
        >
          <Sparkles className="size-4" />
          {loading ? "Buscando..." : "Buscar Músicas"}
        </button>
      </div>

      {mode === "repertoire" && repertoireSearched && (
        <SongResults songs={repertoireSongs} tone="manual" />
      )}
    </div>
  );
}


