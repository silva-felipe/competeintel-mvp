import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CompeteIntel | Inteligência Competitiva para o Mercado Brasileiro",
  description: "Análise competitiva inteligente que revela quem são seus concorrentes, onde estão localizados e como você pode superá-los.",
  keywords: "análise competitiva, concorrentes, inteligência de mercado, Brasil, CNPJ",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
