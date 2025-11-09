import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Nothing — The Ultimate Luxury",
  description: "Own nothing. Experience everything. The most exclusive offering in existence.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="antialiased bg-cream text-charcoal">
        {children}
      </body>
    </html>
  );
}
