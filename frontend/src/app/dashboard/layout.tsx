import ConditionalFloatingChatProvider from '@/components/FloatingChat/ConditionalFloatingChatProvider';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ConditionalFloatingChatProvider>
      {children}
    </ConditionalFloatingChatProvider>
  );
}