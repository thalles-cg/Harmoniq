import { useEffect, useState } from "react";
import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { ArrowLeft, LogOut, Music } from "lucide-react";

import { buscarUsuarioAutenticado, logout } from "@/services/auth";

export const Route = createFileRoute("/perfil")({
  head: () => ({
    meta: [
      { title: "Meu perfil — HarmoniQ" },
      {
        name: "description",
        content: "Visualize os dados da sua conta no HarmoniQ.",
      },
    ],
  }),
  component: Perfil,
});

type Usuario = {
  id: number;
  nome: string;
  email: string;
};

function Perfil() {
  const navigate = useNavigate();

  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    async function carregarUsuario() {
      const dados = await buscarUsuarioAutenticado();

      if (dados === null) {
        await navigate({
          to: "/login",
        });

        return;
      }

      setUsuario(dados);
      setCarregando(false);
    }

    carregarUsuario();
  }, [navigate]);

  function handleLogout() {
    logout();

    navigate({
      to: "/",
    });
  }

  if (carregando) {
    return (
      <main className="grid min-h-dvh place-items-center bg-background font-sans text-foreground">
        <p className="text-sm text-muted-foreground">
          Carregando perfil...
        </p>
      </main>
    );
  }

  if (!usuario) {
    return null;
  }

  return (
    <main className="min-h-dvh bg-background font-sans text-foreground">
      <div className="mx-auto flex min-h-dvh w-full max-w-2xl flex-col px-6 py-6">
        <header className="flex items-center justify-between">
          <Link
            to="/"
            className="flex items-center gap-2 rounded-full bg-background/50 px-4 py-2 text-sm font-medium backdrop-blur-md transition-colors hover:bg-background/70"
          >
            <ArrowLeft className="size-4" />
            Voltar
          </Link>

          <div className="flex items-center gap-2 rounded-full bg-background/50 px-4 py-2 backdrop-blur-md">
            <Music className="size-4 text-emerald" />
            <span className="font-display text-sm font-semibold tracking-tight">
              HarmoniQ
            </span>
          </div>
        </header>

        <section className="flex flex-1 flex-col justify-center">
          <div className="mb-8">
            <h1 className="font-display text-3xl font-bold">
              Meu perfil
            </h1>

            <p className="mt-2 text-sm text-muted-foreground">
              Informações da sua conta no HarmoniQ.
            </p>
          </div>

          <div className="glass rounded-2xl p-6">
            <div className="space-y-5">
              <div>
                <p className="text-sm text-muted-foreground">Nome</p>
                <p className="mt-1 font-medium">{usuario.nome}</p>
              </div>

              <div>
                <p className="text-sm text-muted-foreground">E-mail</p>
                <p className="mt-1 font-medium">{usuario.email}</p>
              </div>
              
              <button
                type="button"
                onClick={handleLogout}
                className="flex w-full items-center justify-center gap-2 rounded-xl bg-primary px-4 py-3 text-sm font-semibold text-primary-foreground transition-opacity hover:opacity-90"
              >
                <LogOut className="size-4" />
                Sair da conta
              </button>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}