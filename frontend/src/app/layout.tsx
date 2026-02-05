import { AuthProvider } from '@/components/AuthProvider';
import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'TaskMaster - Your AI-Powered Task Management Solution',
  description: 'Manage your tasks efficiently with our intuitive dashboard and AI assistant',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        <AuthProvider>
          <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            {children}
          </div>
        </AuthProvider>
      </body>
    </html>
  )
}