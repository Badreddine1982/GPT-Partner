import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "GPT Partner",
  description: "A governed capability and execution layer for GPT.",
}

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
