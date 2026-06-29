import type { Metadata, Viewport } from 'next'
import { Inter, Outfit } from 'next/font/google'
import './globals.css'
import { Providers } from '@/components/providers'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const outfit = Outfit({
  subsets: ['latin'],
  variable: '--font-outfit',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Aide — AI Cybersecurity Mentor',
  description:
    'Aide is an AI-powered cybersecurity mentor for TryHackMe, Hack The Box, PortSwigger, bug bounty, and security learning. Learn through guided hints, explanations, and reasoning instead of spoilers.',
  keywords: [
    'cybersecurity',
    'AI mentor',
    'CTF',
    'Hack The Box',
    'TryHackMe',
    'bug bounty',
    'PortSwigger',
  ],
}

export const viewport: Viewport = {
  themeColor: '#0d1117',
  colorScheme: 'dark',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html
      lang="en"
      data-color-mode="dark"
      data-light-theme="light"
      data-dark-theme="dark"
      className={`${inter.variable} ${outfit.variable}`}
      suppressHydrationWarning
    >
      <body suppressHydrationWarning>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
