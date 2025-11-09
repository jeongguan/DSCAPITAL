import type { Metadata } from "next";
import { Cormorant_Garamond, Inter } from "next/font/google";
import "./globals.css";

const cormorant = Cormorant_Garamond({
  weight: ['300', '400', '500', '600', '700'],
  subsets: ["latin"],
  variable: '--font-cormorant',
});

const inter = Inter({
  weight: ['300', '400', '500', '600'],
  subsets: ["latin"],
  variable: '--font-inter',
});

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
      <body className={`${cormorant.variable} ${inter.variable} antialiased bg-cream text-charcoal`}>
        {children}
      </body>
    </html>
  );
}
