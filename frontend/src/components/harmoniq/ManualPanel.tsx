import { useEffect, useState } from "react";
import { Search, X, Sparkles, ListOrdered, LayoutGrid } from "lucide-react";
import { SongResults, type Song, type SongSearchResult } from "./SongResults";

type Acorde = {
  id: number;
  nome_cifra: string;
  nome_extenso: string;
  nota_fundamental_id: number;
  nota_fundamental: string;
  qualidade: string;
  notas: number[];
};
const GRAUS_DISPONIVEIS = [
  "I", "ii", "iii", "IV", "V", "vi", "vii",
  "i", "II", "III", "iv", "v", "VI", "VII"
];

const API_URL = import.meta.env["VITE_API_URL"];

export function ManualPanel() {
  const [acordes, setAcordes] = useState<Acorde[]>([]);
  const [mode, setMode] = useState<"exact" | "repertoire">("exact");

  const [exactDegrees, setExactDegrees] = useState<string[]>(["I", "V", "VI", "IV"]);
  const [repertoireChords, setRepertoireChords] = useState<string[]>([]);

  const [exactSearched, setExactSearched] = useState(false);
  const [repertoireSearched, setRepertoireSearched] = useState(false);

  const [exactSongs, setExactSongs] = useState<SongSearchResult[]>([]);
  const [repertoireSongs, setRepertoireSongs] = useState<Song[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function carregarAcordes() {
      try {
        const response = await fetch(`${API_URL}/acordes/`);
        if (!response.ok) throw new Error("Erro ao buscar acordes.");
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
    {}
  );

  const addItem = (item: string) => {
    if (mode === "exact") {
      setExactDegrees((prev) => [...prev, item]);
    } else {
      setRepertoireChords((prev) => [...prev, item]);
    }
  };

  const removeItem = (index: number) => {
    if (mode === "exact") {
      setExactDegrees((prev) => prev.filter((_, i) => i !== index));
    } else {
      setRepertoireChords((prev) => prev.filter((_, i) => i !== index));
    }
  };

  const handleSearch = async () => {
    const items = mode === "exact" ? exactDegrees : repertoireChords;
    if (items.length === 0) return;

    setLoading(true);

    try {
      const params = new URLSearchParams();
      const paramName = mode === "exact" ? "graus" : "acordes";

      items.forEach((val) => {
        params.append(paramName, val);
      });

      const endpoint = mode === "exact" ? "sequencia" : "repertorio";

      const response = await fetch(
        `${API_URL}/musicas/busca/${endpoint}?${params.toString()}`
      );

      if (!response.ok) throw new Error("Erro ao buscar músicas.");

      if (mode === "exact") {
        const data: SongSearchResult[] = await response.json();
        setExactSongs(data);
        setExactSearched(true);
      } else {
        const data: Song[] = await response.json();
        setRepertoireSongs(data);
        setRepertoireSearched(true);
      }
    } catch (error) {
      console.error("Erro ao buscar músicas:", error);
    } finally {
      setLoading(false);
    }
  };

  const currentItems = mode === "exact" ? exactDegrees : repertoireChords;

  return (
    <div className="mx-auto w-full max-w-5xl space-y-6 px-4 pb-16 sm:px-6">
      <div className="inline-flex rounded-2xl bg-secondary/70 p-1">
        {(
          [
            {
              id: "exact",
              label: "Sequência Exata",
              hint: "Busca por graus independentes de tom",
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
          ? "Buscamos músicas com essa progressão de graus."
          : "Buscamos músicas que usem apenas os acordes do seu repertório."}
      </p>

      <div className="glass space-y-5 rounded-2xl p-5">
        <div className="sticky top-0 z-30 rounded-xl border-b border-border bg-[color-mix(in_oklab,var(--card)_85%,var(--background))] p-3 shadow-sm">
          <p className="mb-2 text-xs tracking-wide text-muted-foreground uppercase">
            {mode === "exact" ? "Sequência de Graus Selecionada" : "Meus acordes"}
          </p>

          <div className="flex min-h-12 flex-wrap items-center gap-2 rounded-xl border border-dashed border-border p-3">
            {currentItems.length === 0 && (
              <span className="text-sm text-muted-foreground">
                Nenhum item selecionado ainda.
              </span>
            )}

            {currentItems.map((item, i) => (
              <span
                key={`${item}-${i}`}
                className="flex items-center gap-2 rounded-full bg-[image:var(--gradient-manual)] px-3 py-1.5 text-sm font-medium text-primary-foreground"
              >
                {item}
                <button
                  onClick={() => removeItem(i)}
                  aria-label={`Remover ${item}`}
                >
                  <X className="size-3.5 opacity-80 hover:opacity-100" />
                </button>
              </span>
            ))}
          </div>
        </div>

        {/* Renderiza painel de Graus se for modo exact, ou painel de Acordes se for repertório */}
        {mode === "exact" ? (
          <div className="rounded-xl border border-border bg-background/40 p-4">
            <p className="mb-3 text-xs tracking-wide text-muted-foreground uppercase">
              Clique nos graus para montar a sequência:
            </p>
            <div className="flex flex-wrap gap-2">
              {GRAUS_DISPONIVEIS.map((grau) => (
                <button
                  key={grau}
                  onClick={() => addItem(grau)}
                  className="rounded-lg bg-secondary px-4 py-2 font-display text-sm font-semibold text-secondary-foreground transition-colors hover:bg-violet/40 hover:text-foreground"
                >
                  {grau}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
            {Object.entries(acordesPorFundamental).map(
              ([fundamental, acordesDaFundamental]) => (
                <div
                  key={fundamental}
                  className="rounded-xl border border-border bg-background/40 p-2"
                >
                  <div className="rounded-lg bg-secondary py-2 text-center font-display text-lg font-semibold">
                    {fundamental}
                  </div>
                  <div className="mt-2 grid grid-cols-2 gap-1.5">
                    {acordesDaFundamental.map((acorde) => (
                      <button
                        key={acorde.id}
                        onClick={() => addItem(acorde.nome_cifra)}
                        title={`Adicionar ${acorde.nome_cifra}`}
                        className="min-w-0 rounded-md bg-muted px-2 py-1.5 text-xs font-medium text-muted-foreground transition-colors hover:bg-violet/30 hover:text-foreground"
                      >
                        {acorde.nome_cifra}
                      </button>
                    ))}
                  </div>
                </div>
              )
            )}
          </div>
        )}

        <button
          onClick={handleSearch}
          disabled={loading || currentItems.length === 0}
          className="flex w-full items-center justify-center gap-2 rounded-xl bg-[image:var(--gradient-manual)] px-6 py-3.5 font-display font-semibold text-primary-foreground shadow-[var(--shadow-glow-manual)] transition-transform hover:scale-[1.01] disabled:cursor-not-allowed disabled:opacity-50"
        >
          <Sparkles className="size-4" />
          {loading ? "Buscando..." : "Buscar Músicas por Graus"}
        </button>
      </div>

      {mode === "exact" && exactSearched && (
        <SongResults songs={exactSongs} searchedSequence={exactDegrees} tone="manual" />
      )}

      {mode === "repertoire" && repertoireSearched && (
        <SongResults songs={repertoireSongs} tone="manual" />
      )}
    </div>
  );
}