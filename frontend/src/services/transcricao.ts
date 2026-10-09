const API_URL = import.meta.env["VITE_API_URL"];

export type AcordeDetectado = {
  inicio: number;
  fim: number;
  acorde: string;
};

export async function transcreverAudio(arquivo: File): Promise<AcordeDetectado[]> {
  const formulario = new FormData();
  formulario.append("arquivo", arquivo);

  const response = await fetch(`${API_URL}/transcricoes/`, {
    method: "POST",
    body: formulario,
  });

  if (!response.ok) {
    throw new Error("Não foi possível transcrever o áudio.");
  }

  return response.json();
}

