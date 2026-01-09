import './globals.css';

export const metadata = {
  title: 'TaskMaster - Your Task Management Solution',
  description: 'Manage your tasks efficiently with our intuitive dashboard',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
      </head>
      <body>{children}</body>
    </html>
  )
}
