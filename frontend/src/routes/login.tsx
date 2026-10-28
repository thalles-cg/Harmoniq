import { FormEvent, useState } from "react";
import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { ArrowLeft, LockKeyhole, LogIn, Music } from "lucide-react";

const API_URL = import.meta.env["VITE_API_URL"];

export const Route = createFileRoute("/login")({
  head: () => ({
    meta: [
      { title: "Entrar — HarmoniQ" },
      {
        name: "description",
        content: "Entre na sua conta do HarmoniQ.",
      },
    ],
  }),
  component: Login,
});

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setErro("");
    setCarregando(true);

    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          senha,
        }),
      });

      if (!response.ok) {
        if (response.status === 401) {
          setErro("E-mail ou senha inválidos.");
        } else {
          setErro("Não foi possível realizar o login.");
        }

        return;
      }

      const data = await response.json();

      localStorage.setItem("access_token", data.access_token);

      await navigate({
        to: "/",
      });
    } catch {
      setErro("Não foi possível conectar ao servidor.");
    } finally {
      setCarregando(false);
    }
  }

  return (
    <main className="min-h-dvh bg-background font-sans text-foreground">
      <div className="mx-auto flex min-h-dvh w-full max-w-md flex-col px-6 py-6">
        <div className="flex items-center justify-between">
          <Link
            to="/"
            className="flex items-center gap-2 rounded-full bg-background/50 px-4 py-2 backdrop-blur-md transition-colors hover:bg-background/70"
          >
            <ArrowLeft className="size-4" />
            <span className="text-sm font-medium">Voltar</span>
          </Link>

          <div className="flex items-center gap-2 rounded-full bg-background/50 px-4 py-2 backdrop-blur-md">
            <Music className="size-4 text-emerald" />
            <span className="font-display text-sm font-semibold tracking-tight">
              HarmoniQ
            </span>
          </div>
        </div>

        <div className="flex flex-1 flex-col justify-center">
          <div className="mb-8 text-center">

            <h1 className="font-display text-3xl font-bold">
              Entre no HarmoniQ
            </h1>

            <p className="mt-2 text-sm text-muted-foreground">
              Acesse seu repertório e suas músicas favoritas.
            </p>
          </div>

          <form
            onSubmit={handleSubmit}
            className="glass rounded-2xl p-6"
          >
            <div className="space-y-5">
              <div>
                <label
                  htmlFor="email"
                  className="mb-2 block text-sm font-medium"
                >
                  E-mail
                </label>

                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  placeholder="seu@email.com"
                  autoComplete="email"
                  required
                  className="w-full rounded-xl border border-border bg-background/50 px-4 py-3 text-sm outline-none transition focus:ring-2 focus:ring-ring"
                />
              </div>

              <div>
                <label
                  htmlFor="senha"
                  className="mb-2 block text-sm font-medium"
                >
                  Senha
                </label>

                <div className="relative">
                  <LockKeyhole className="pointer-events-none absolute left-4 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />

                  <input
                    id="senha"
                    type="password"
                    value={senha}
                    onChange={(event) => setSenha(event.target.value)}
                    placeholder="Sua senha"
                    autoComplete="current-password"
                    required
                    className="w-full rounded-xl border border-border bg-background/50 py-3 pl-11 pr-4 text-sm outline-none transition focus:ring-2 focus:ring-ring"
                  />
                </div>
              </div>

              {erro && (
                <p
                  role="alert"
                  className="rounded-xl border border-destructive/30 bg-destructive/10 px-4 py-3 text-sm text-destructive"
                >
                  {erro}
                </p>
              )}

              <button
                type="submit"
                disabled={carregando}
                className="flex w-full items-center justify-center gap-2 rounded-xl bg-primary px-4 py-3 text-sm font-semibold text-primary-foreground transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <LogIn className="size-4" />
                {carregando ? "Entrando..." : "Entrar"}
              </button>
            </div>
          </form>

          <div className="mt-6 text-center text-sm text-muted-foreground">
            Ainda não tem uma conta?{" "}
            <Link
              to="/cadastro"
              className="font-medium text-foreground underline-offset-4 hover:underline"
            >
              Criar conta
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}