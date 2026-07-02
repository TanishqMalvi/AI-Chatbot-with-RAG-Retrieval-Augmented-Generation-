import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HealthTech RAG Assistant",
  description:
    "Enterprise HealthTech knowledge assistant with secure RAG chat, document ingestion, and audit-ready workflows.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
