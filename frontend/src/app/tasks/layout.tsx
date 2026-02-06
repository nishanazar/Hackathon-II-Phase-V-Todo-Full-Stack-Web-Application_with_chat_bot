import ConditionalFloatingChatProvider from '@/components/FloatingChat/ConditionalFloatingChatProvider';

export default function TasksLayout({
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